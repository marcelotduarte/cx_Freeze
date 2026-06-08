"""Base class for Module and ConstantsModule."""

from __future__ import annotations

import ast
import socket
from contextlib import suppress
from datetime import datetime, timezone
from functools import cached_property, partial
from importlib.machinery import EXTENSION_SUFFIXES
from keyword import iskeyword
from pathlib import Path
from pkgutil import resolve_name
from typing import TYPE_CHECKING, Any, Literal

from cx_Freeze._compat import IS_MACOS
from cx_Freeze._metadata import DistributionCache
from cx_Freeze.exception import ModuleError, OptionError

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence
    from importlib.abc import Loader
    from types import CodeType

    from cx_Freeze._typing import StrPath
    from cx_Freeze.finder import ModuleFinder

__all__ = ["ConstantsModule", "Module", "ModuleHook"]


class Module:
    """The Module class."""

    def __init__(
        self,
        name: str,
        path: Sequence[StrPath] | None = None,
        filename: StrPath | None = None,
        parent: Module | None = None,
    ) -> None:
        self.name: str = name
        self.path: list[Path] | None = list(map(Path, path)) if path else None
        self._file: Path | None = self._file_validate(filename)
        self.parent: Module | None = parent
        self.root: Module = parent.root if parent else self

        self.code: CodeType | None = None
        self.cache_path: Path | None = None
        self.distribution: DistributionCache | None = None
        self.error_exc: BaseException | None = None
        self.error_msg: str | None = None
        self.hook: ModuleHook | Callable | None = None
        self.lazy: bool = False
        self.loader: Loader | None = None

        self.exclude_names: set[str] = set()
        self.global_names: set[str] = set()
        self.ignore_names: set[str] = set()
        self.in_import: bool = True
        self.source_is_zip_file: bool = False
        self._in_file_system: Literal[0, 1, 2] = 1
        # add the load hook
        self.load_hook()

    def __repr__(self) -> str:
        parts = [f"name={self.name!r}"]
        if self.distribution is not None:
            parts.append(f"distribution={self.distribution.name!r}")
        if self.file is not None:
            parts.append(f"file={self.file.as_posix()!r}")
        if self.path is not None:
            parts.append(f"path={self.path}")
        if self.parent is not None:
            parts.append(f"parent.name={self.parent.name!r}")
        join_parts = ", ".join(parts)
        return f"<Module {join_parts}>"

    @property
    def file(self) -> Path | None:
        """Module filename."""
        return self._file

    @file.setter
    def file(self, filename: StrPath | None) -> None:
        self._file = self._file_validate(filename)

    def _file_validate(self, filename: StrPath | None) -> Path | None:
        if "stub_code" in self.__dict__:
            del self.__dict__["stub_code"]  # clear the cache
        if not filename:
            return None
        return Path(filename)

    @property
    def in_file_system(self) -> Literal[0, 1, 2]:
        """Returns a value indicating where the module/package will be stored.

        Possible values:
        0. in a zip file (not directly in the file system);
        1. in the file system, package with modules and data;
        2. in the file system, only detected modules.
        """
        if self.parent is not None:
            return self.parent.in_file_system
        if self.path is None:
            return 0
        return self._in_file_system

    @in_file_system.setter
    def in_file_system(self, value: Literal[0, 1, 2]) -> None:
        self._in_file_system = value

    @cached_property
    def root_dir(self) -> Path | None:
        file = self.root.file
        if file is None:
            # Attempt finding implicit namespace package in path
            for path in self.root.path or ():
                root_dir = next(path.glob(self.root.name), None)
                if root_dir is not None:
                    return root_dir
            return None
        return file.parent

    @cached_property
    def stub_code(self) -> CodeType | None:
        cache_path: Path | None = self.cache_path
        filename = self._file
        if filename is None:
            return None

        if self.root_dir is None:
            return None
        try:
            package = filename.parent.relative_to(self.root_dir.parent)
        except ValueError:
            return None

        ext = "".join(filename.suffixes)
        if ext not in EXTENSION_SUFFIXES and not self.root.lazy:
            return None
        stem = filename.name.removesuffix(ext)
        stub_name = f"{stem}.pyi"

        # search for the stub file already parsed in the distribution
        importshed = Path(__file__).resolve().parent / "importshed"
        source_file = importshed / package / stub_name
        imports_only = None
        if source_file.exists():
            imports_only = source_file.read_text(encoding="utf_8")
        if not imports_only:
            # search for a stub file along side the python extension module
            source_file = filename.parent / stub_name
            if source_file.exists():
                imports_only = self.get_imports_from_file(source_file)
            if not imports_only and cache_path:
                target_file = cache_path / package / stub_name
                if target_file.exists():
                    # a parsed stub exists in the cache
                    imports_only = target_file.read_text(encoding="utf_8")
                else:
                    imports_only = self.get_imports_from_file(source_file)
                    if imports_only:
                        # cache the parsed stub
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        target_file.write_text(
                            "# Generated by cx_Freeze\n\n" + imports_only,
                            encoding="utf_8",
                        )
        if imports_only:
            return compile(imports_only, stub_name, "exec", dont_inherit=True)
        return None

    def get_imports_from_file(self, source_file: Path) -> str | None:
        """Get the implicit imports in a stub file."""
        if not source_file.is_file():
            return None
        ignore = {
            "__future__",
            "builtins",
            "_typeshed",
            "typing",
            "typing_extensions",
        }
        source = source_file.read_text(encoding="utf_8")
        try:
            rootnode = ast.parse(source, source_file.name)
        except SyntaxError:
            return None
        lines = []
        for node in ast.walk(rootnode):
            if isinstance(node, ast.Import):
                names = {name.name for name in node.names}
                names.difference_update(ignore)
                if names:
                    lines.append("import " + ", ".join(sorted(names)))
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module in ignore:
                    continue
                names = {name.name for name in node.names}
                line = "from "
                if node.level > 0:
                    line += "." * node.level
                if node.module:
                    line += node.module
                line += " import " + ", ".join(sorted(names))
                lines.append(line)
        return "\n".join([*lines, ""]) if lines else None

    def libs(self) -> Iterator[tuple[Path, str]]:
        """Dynamic libraries distributed along with the package."""
        distribution = self.distribution
        if distribution:
            if self.in_file_system == 0:
                # the module is in zip file and binary files are
                for file in distribution.binary_files:
                    source = distribution.locate_file(file)
                    # .. not in library directories
                    if not source.parent.name.endswith((".libs", ".dylibs")):
                        target = f"lib/{source.name}"
                    else:
                        target = f"lib/{file}"
                    yield source, target
            else:
                # the module is in file system, so consider
                # mirroring the binary files to the lib directory
                for file in distribution.binary_files:
                    source = distribution.locate_file(file)
                    target = f"lib/{file}"
                    yield source, target
        else:
            module_path = self.path
            if module_path is None:
                if self.file is None:
                    return
                module_path = [self.file.parent]
            for name in self.libs_dirs():
                for module_dir in module_path:
                    for source in module_dir.parent.joinpath(name).iterdir():
                        target = f"lib/{name}/{source.name}"
                        yield source, target

    def libs_dirs(self) -> list[str]:
        """Return the directories where shared library files are stored."""
        distribution = self.distribution
        if distribution:
            return list(
                {
                    distribution.locate_file(file).parent.as_posix()
                    for file in distribution.binary_files
                }
            )

        module_path = self.path
        if module_path is None:
            if self.file is None:
                return []
            module_path = [self.file.parent]

        names = {
            f"../{self.name}.libs",  # numpy >=1.26.0, scipy >=1.9.2
            f"{self.name}/.libs",  # old numpy, scipy <1.9.2
            f"{self.name}/lib",  # torch
        }
        if IS_MACOS:
            names.add(f"{self.name}/.dylibs")  # scipy, pillow, etc on macos
        if distribution:
            names.update(
                [
                    f"../{distribution.normalized_name}.libs",  # pillow >=10.2
                    f"../{distribution.name}.libs",  # Pillow <10.2
                ]
            )
        valid_dirs = []
        for module_dir in module_path:
            for name in names:
                source_dir = module_dir.joinpath(name).resolve()
                if source_dir.exists():
                    valid_dirs.append(
                        source_dir.relative_to(module_dir.parent).as_posix()
                    )
        return valid_dirs

    def load_hook(self) -> None:
        """Load hook for the given module if one is present.

        For instance, to load a hook for PIL.Image:
        - Using ModuleHook class:
            # module and hook methods are lowercased.
            from cx_Freeze.hooks import _pil_ as pil
            hook = pil.Hook()
            hook.pil_image(...)
        - For functions present in hooks.__init__:
            # module and load hook functions use the original case.
            from cx_Freeze.hooks import load_PIL_Image
            load_PIL_Image(...)
        """
        if not isinstance(self.root.hook, ModuleHook):
            try:
                # new style hook using ModuleHook class - top-level call
                root_name = self.root.name.lower()
                hook_cls = resolve_name(f"cx_Freeze.hooks._{root_name}_:Hook")
                if issubclass(hook_cls, ModuleHook):
                    self.root.hook = hook_cls(self.root)
            except (AttributeError, ValueError, ImportError):
                # old style hook with functions at hooks.__init__
                name = self.name.replace(".", "_")
                try:
                    func = resolve_name(f"cx_Freeze.hooks:load_{name}")
                except (AttributeError, ValueError):
                    pass
                else:
                    self.hook = partial(func, module=self)
                return
        # new style hook using ModuleHook class - lower level call
        root_hook = self.root.hook
        if isinstance(root_hook, ModuleHook) and self.parent is not None:
            name = "_".join(self.name.lower().split(".")[1:])
            func = getattr(root_hook, f"{root_hook.name}_{name}", None)
            self.hook = partial(func, module=self) if func else None

    def update_distribution(self, name: str | None = None) -> None:
        """Update the distribution cache based on its name.

        This method may be used to link an distribution's name to a module.

        Example: ModuleFinder cannot detects the distribution of _cffi_backend
        but in a hook we can link it to 'cffi'.
        """
        cache_path: Path | None = self.cache_path
        if cache_path is None:
            return
        if name is None:
            name = self.name
        try:
            distribution = DistributionCache(cache_path, name)
        except ModuleError:
            return
        for req_name in distribution.requires:
            with suppress(ModuleError):
                DistributionCache(cache_path, req_name)
        self.distribution = distribution


class ModuleHook:
    """The Module Hook class."""

    def __init__(self, module: Module) -> None:
        self.module = module  # the root module
        self.name = module.name.replace(".", "_").lower()

    def __call__(self, finder: ModuleFinder) -> None:
        # redirect to the top level hook
        method = getattr(self, self.name, None)
        if method:
            method(finder, self.module)


class ConstantsModule:
    """Base ConstantsModule class."""

    def __init__(
        self,
        release_string: str | None = None,
        copyright_string: str | None = None,
        module_name: str = "BUILD_CONSTANTS",
        time_format: str = "%B %d, %Y %H:%M:%S",
        constants: list[str] | None = None,
    ) -> None:
        self.module_name: str = module_name
        self.time_format: str = time_format
        self.values: dict[str, Any] = {}
        self.values["BUILD_RELEASE_STRING"] = release_string
        self.values["BUILD_COPYRIGHT"] = copyright_string
        if constants:
            for constant in constants:
                parts = constant.split("=", maxsplit=1)
                if len(parts) == 1:
                    name = constant
                    value = None
                else:
                    name, string_value = parts
                    if string_value:
                        value = ast.literal_eval(string_value)
                    else:
                        value = string_value
                if not name.isidentifier() or iskeyword(name):
                    msg = f"Invalid constant name ({name!r})"
                    raise OptionError(msg)
                self.values[name] = value

    def create(self, tmp_path: Path, modules: list[Module]) -> Path:
        """Create the constants module.

        It consists of declaration statements for each of the values.
        """
        today = datetime.now(tz=timezone.utc)
        source_timestamp = 0
        for module in modules:
            if (
                module.file is None
                or not module.file.exists()
                or module.source_is_zip_file
            ):
                continue
            timestamp = module.file.stat().st_mtime
            source_timestamp = max(source_timestamp, timestamp)
        stamp = datetime.fromtimestamp(source_timestamp, tz=timezone.utc)
        self.values["BUILD_TIMESTAMP"] = today.strftime(self.time_format)
        self.values["BUILD_HOST"] = socket.gethostname().split(".")[0]
        self.values["SOURCE_TIMESTAMP"] = stamp.strftime(self.time_format)
        parts = []
        for name in sorted(self.values.keys()):
            value = self.values[name]
            parts.append(f"{name} = {value!r}")
        module_path = tmp_path.joinpath(self.module_name).with_suffix(".py")
        with module_path.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(parts))
        return module_path
