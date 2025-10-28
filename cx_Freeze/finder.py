"""Module Finder - discovers what modules are required by the code."""

from __future__ import annotations

import importlib.machinery
import logging
import os
import sys
from contextlib import suppress
from functools import cached_property
from pathlib import Path, PurePath
from pkgutil import resolve_name
from sysconfig import get_config_var
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from cx_Freeze._bytecode import (
    code_object_replace,
    code_object_replace_package,
    scan_code,
)
from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.common import process_path_specs, resource_path
from cx_Freeze.hooks.unused_modules import (
    DEFAULT_EXCLUDES,
    DEFAULT_IGNORE_NAMES,
)
from cx_Freeze.module import ConstantsModule, Module

if TYPE_CHECKING:
    from collections.abc import Sequence
    from importlib.abc import ExecutionLoader
    from types import CodeType

    from cx_Freeze._typing import (
        DeferredList,
        IncludesList,
        InternalIncludesList,
    )

ALL_SUFFIXES = importlib.machinery.all_suffixes()


__all__ = ["ModuleFinder"]

logger = logging.getLogger(__name__)


class ModuleFinder:
    """ModuleFinder base class."""

    def __init__(
        self,
        constants_module: ConstantsModule,
        excludes: list[str] | None = None,
        include_files: IncludesList | None = None,
        path: list[str | Path] | None = None,
        replace_paths: list[tuple[str, str]] | None = None,
        zip_exclude_packages: Sequence[str] | None = None,
        zip_include_packages: Sequence[str] | None = None,
        zip_include_all_packages: bool = False,
        zip_includes: IncludesList | None = None,
    ) -> None:
        self.included_files: InternalIncludesList = process_path_specs(
            include_files
        )
        self.excludes: set[str] = set(excludes or [])
        self.optimize = 0
        self.path: list[str] = list(map(os.fspath, path or sys.path))
        self.replace_paths = replace_paths or []
        self.zip_include_all_packages = zip_include_all_packages
        self.zip_exclude_packages: set = set(zip_exclude_packages or [])
        self.zip_include_packages: set = set(zip_include_packages or [])
        self.constants_module: ConstantsModule = constants_module
        self.zip_includes: InternalIncludesList = process_path_specs(
            zip_includes
        )
        self.namespaces = []
        self.modules = []
        self.aliases = {}
        self.excluded_dependent_files: set[Path] = set()
        self._bad_modules = {}
        # add the unused modules in the current platform
        self.excludes.update(DEFAULT_EXCLUDES)
        self._modules: dict[str, Module | None] = dict.fromkeys(
            self.excludes or []
        )
        self._tmp_dir = TemporaryDirectory(prefix="cxfreeze-")
        self.cache_path = Path(self._tmp_dir.name)
        self.lib_files: dict[Path, str] = {}
        self.packages_distributions = (
            importlib.metadata.packages_distributions()
        )

    def cleanup(self) -> None:
        self._tmp_dir.cleanup()

    def _add_module(
        self,
        name: str,
        path: Sequence[Path | str] | None = None,
        filename: Path | None = None,
        parent: Module | None = None,
    ) -> Module:
        """Add a module to the list of modules but if one is already found,
        then return it instead; this is done so that packages can be
        handled properly.
        """
        module = self._modules.get(name)
        if module is None:
            module = Module(name, path, filename, parent)
            self._modules[name] = module
            self.modules.append(module)
            if name in self._bad_modules:
                logger.debug(
                    "Removing module [%s] from list of bad modules", name
                )
                del self._bad_modules[name]
            if (
                self.zip_include_all_packages
                and module.name not in self.zip_exclude_packages
            ) or module.name in self.zip_include_packages:
                module.in_file_system = 0
            module.cache_path = self.cache_path
            module.update_distribution()
        if module.path is None and path is not None:
            module.path = list(map(Path, path))
        if module.file is None and filename is not None:
            module.file = filename
        return module

    @cached_property
    def _builtin_modules(self) -> set[str]:
        """The built-in modules are determined based on the cx_Freeze build."""
        builtin_modules: set[str] = set(sys.builtin_module_names)
        core_lib = resource_path("lib")
        if core_lib and core_lib.is_dir():
            # discard modules that exist in freeze-core 'lib'
            ext_suffix = get_config_var("EXT_SUFFIX")
            for file in core_lib.glob(f"*{ext_suffix}"):
                builtin_modules.discard(file.name.removesuffix(ext_suffix))
        return builtin_modules

    def _determine_parent(self, caller: Module | None) -> Module | None:
        """Determine the parent to use when searching packages."""
        if caller is not None:
            if caller.path is not None:
                return caller
            return self._get_parent_by_name(caller.name)
        return None

    def _ensure_from_list(
        self,
        caller: Module,
        package_module: Module,
        from_list: list[str],
        deferred_imports: DeferredList,
    ) -> None:
        """Ensure that the from list is satisfied. This is only necessary for
        package modules. If the package module has not been completely
        imported yet, defer the import until it has been completely imported
        in order to avoid spurious errors about missing modules.
        """
        if package_module.in_import and caller is not package_module:
            deferred_imports.append((caller, package_module, from_list))
        else:
            for name in from_list:
                if name in package_module.global_names:
                    continue
                sub_module_name = f"{package_module.name}.{name}"
                self._import_module(sub_module_name, deferred_imports, caller)

    def _get_parent_by_name(self, name: str) -> Module | None:
        """Return the parent module given the name of a module."""
        pos = name.rfind(".")
        if pos > 0:
            parent_name = name[:pos]
            return self._modules[parent_name]
        return None

    def _import_all_sub_modules(
        self,
        module: Module,
        deferred_imports: DeferredList,
        recursive: bool = True,
    ) -> None:
        """Import all sub modules to the given package."""
        for path in module.path:
            for fullname in path.iterdir():
                if fullname.is_dir():
                    if not fullname.joinpath("__init__.py").exists():
                        continue
                    name = fullname.name
                else:
                    # We need to run through these in order to correctly pick
                    # up PEP 3149 library names
                    # (e.g. .cpython-39-x86_64-linux-gnu.so).
                    for suffix in ALL_SUFFIXES:
                        if fullname.name.endswith(suffix):
                            name = fullname.name.removesuffix(suffix)

                            # Skip modules whose names appear to contain '.',
                            # as we may be using the wrong suffix, and even if
                            # we're not, such module names will break the
                            # import code.
                            if "." not in name:
                                break

                    else:
                        continue
                    if name == "__init__":
                        continue

                sub_module_name = f"{module.name}.{name}"
                sub_module = self._internal_import_module(
                    sub_module_name, deferred_imports
                )
                if sub_module is None:
                    if sub_module_name not in self.excludes:
                        msg = f"No module named {sub_module_name!r}"
                        raise ImportError(msg)
                else:
                    module.global_names.add(name)
                    if sub_module.path and recursive:
                        self._import_all_sub_modules(
                            sub_module, deferred_imports, recursive
                        )

    def _import_deferred_imports(
        self, deferred_imports: DeferredList, skip_in_import: bool = False
    ) -> None:
        """Import any sub modules that were deferred, if applicable."""
        while deferred_imports:
            new_deferred_imports: DeferredList = []
            for caller, package_module, sub_module_names in deferred_imports:
                if package_module.in_import and skip_in_import:
                    continue
                self._ensure_from_list(
                    caller,
                    package_module,
                    sub_module_names,
                    new_deferred_imports,
                )
            deferred_imports = new_deferred_imports
            skip_in_import = True

    def _import_module(
        self,
        name: str,
        deferred_imports: DeferredList,
        caller: Module | None = None,
        relative_import_index: int = 0,
    ) -> Module:
        """Attempt to find the named module and return it or None if no module
        by that name could be found.
        """
        # absolute import (available in Python 2.5 and up)
        # the name given is the only name that will be searched
        if relative_import_index == 0:
            module = self._internal_import_module(name, deferred_imports)

        # old style relative import (regular 'import foo' in Python 2)
        # the name given is tried in the current package, and if no match
        # is found, self.path is searched for a top-level module/pockage
        elif relative_import_index < 0:
            parent = self._determine_parent(caller)
            if parent is not None:
                fullname = f"{parent.name}.{name}"
                module = self._internal_import_module(
                    fullname, deferred_imports
                )
                if module is not None:
                    parent.global_names.add(name)
                    return module

            module = self._internal_import_module(name, deferred_imports)

        # new style relative import (available in Python 2.5 and up)
        # the index indicates how many levels to traverse and only that level
        # is searched for the named module
        elif relative_import_index > 0:
            parent = caller
            if parent.path is not None:
                relative_import_index -= 1
            while parent is not None and relative_import_index > 0:
                parent = self._get_parent_by_name(parent.name)
                relative_import_index -= 1
            if parent is None:
                module = None
            elif not name:
                module = parent
            else:
                name = f"{parent.name}.{name}"
                module = self._internal_import_module(name, deferred_imports)

        # if module not found, track that fact
        if module is None:
            if caller is None:
                msg = f"No module named {name!r}"
                raise ImportError(msg)
            self._missing_hook(caller, name)

        return module

    def _internal_import_module(
        self, name: str, deferred_imports: DeferredList
    ) -> Module | None:
        """Internal method used for importing a module which assumes that the
        name given is an absolute name. None is returned if the module
        cannot be found.
        """
        with suppress(KeyError):
            # Check in module cache before trying to import it again.
            return self._modules[name]

        if name in self._builtin_modules:
            module = self._add_module(name)
            logger.debug("Adding module [%s] [C_BUILTIN]", name)
            if module.hook:
                module.hook(self)
            module.in_import = False
            return module

        pos = name.rfind(".")
        if pos < 0:  # Top-level module
            path = self.path
            parent_module = None
        else:  # Dotted module name - look up the parent module
            parent_name = name[:pos]
            parent_module = self._internal_import_module(
                parent_name, deferred_imports
            )
            if parent_module is None:
                return None
            path = parent_module.path
            path = self.path if path is None else list(map(os.fspath, path))

        if name in self.aliases:
            actual_name = self.aliases[name]
            module = self._internal_import_module(
                actual_name, deferred_imports
            )
            self._modules[name] = module
            return module

        try:
            module = self._load_module(
                name, path, deferred_imports, parent_module
            )
        except ImportError:
            logger.debug("Module [%s] cannot be imported", name)
            self._modules[name] = None
            return None
        return module

    def _find_editable_spec(
        self, name: str, path: Sequence[str] | None
    ) -> importlib.machinery.ModuleSpec | None:
        """Find the spec for a module installed as an editable package."""
        # the distribution name may vary from the module name (eg may
        # include '-'). packages_distributions returns the mapping
        for dist_name in self.packages_distributions.get(name, []):
            dist = importlib.metadata.distribution(dist_name)
            if not dist:
                continue
            for f in dist.files:
                if f.name.startswith("__editable__") and f.name.endswith(
                    "_finder.py"
                ):
                    try:
                        mod = importlib.import_module(f.stem)
                        spec = mod._EditableFinder.find_spec(  # noqa: SLF001
                            name, path
                        )
                        if spec:
                            return spec
                    except (ImportError, AttributeError) as e:
                        logger.warning(
                            "Find editable spec failed for [%s]: %s", name, e
                        )
                        break
        return None

    def _load_module(
        self,
        name: str,
        path: Sequence[str] | None,
        deferred_imports: DeferredList,
        parent: Module | None = None,
    ) -> Module | None:
        """Load the module, searching the module spec."""
        spec: importlib.machinery.ModuleSpec | None = None
        loader: ExecutionLoader | None = None
        module: Module | None = None

        # Find modules to load
        try:
            # It's recommended to clear the caches first.
            importlib.machinery.PathFinder.invalidate_caches()
            spec = importlib.machinery.PathFinder.find_spec(name, path)
        except KeyError:
            if parent:
                # some packages use a directory with vendor modules without
                # an __init__.py, thus, are called nested namespace packages
                module = self._add_module(
                    name,
                    path=[Path(path[0], name.rpartition(".")[-1])],
                    parent=parent,
                )
                logger.debug("Adding module [%s] [NESTED NAMESPACE]", name)
                self.namespaces.append(module)
                with suppress(ValueError):
                    self.modules.remove(module)
                module.in_import = False
                return module

        if not spec:
            spec = self._find_editable_spec(name, path)

        if spec:
            loader = spec.loader
            # Ignore built-in importers
            if loader is importlib.machinery.BuiltinImporter:
                return None
            if loader is importlib.machinery.FrozenImporter:
                return None
            # Load package or namespace package
            if spec.submodule_search_locations:
                module = self._add_module(
                    name,
                    path=list(spec.submodule_search_locations),
                    parent=parent,
                )
                if spec.origin is None:
                    logger.debug("Adding module [%s] [NAMESPACE]", name)
                    self.namespaces.append(module)
                    with suppress(ValueError):
                        self.modules.remove(module)
                    module.in_import = False
                    return module
                logger.debug("Adding module [%s] [PACKAGE]", name)
                module.file = Path(spec.origin)  # path of __init__.py
            else:
                module = self._add_module(
                    name, filename=Path(spec.origin), parent=parent
                )

        if module is not None:
            self._load_module_code(module, loader, deferred_imports)
        return module

    def _load_module_code(
        self,
        module: Module,
        loader: ExecutionLoader | None,
        deferred_imports: DeferredList,
    ) -> Module | None:
        name = module.name
        path = os.fspath(module.file)

        if isinstance(loader, importlib.machinery.SourceFileLoader):
            logger.debug("Adding module [%s] [SOURCE]", name)
            # Load & compile Python source code
            source_bytes = loader.get_data(path)
            try:
                module.code = loader.source_to_code(
                    source_bytes, path, _optimize=self.optimize
                )
            except SyntaxError:
                logger.debug("Invalid syntax in [%s]", name)
                msg = f"Invalid syntax in {path}"
                raise ImportError(msg, name=name) from None
        elif isinstance(loader, importlib.machinery.SourcelessFileLoader):
            logger.debug("Adding module [%s] [BYTECODE]", name)
            # Load Python bytecode
            module.code = loader.get_code(name)
            if module.code is None:
                msg = f"Bad magic number in {path}"
                raise ImportError(msg, name=name)
        elif isinstance(loader, importlib.machinery.ExtensionFileLoader):
            logger.debug("Adding module [%s] [EXTENSION]", name)
        else:
            msg = f"Unknown module loader in {path}"
            raise ImportError(msg, name=name)  # noqa: TRY004

        # Run custom hook for the module
        if module.hook:
            module.hook(self)

        # Add dynamic libraries (dependencies) of the package
        if module is module.root:
            for source, target in module.libs():
                self.lib_files.setdefault(source, target)
                # use include_files on windows
                if IS_WINDOWS:
                    self.include_files(source, target)
            if IS_WINDOWS and module.in_file_system == 0:
                # Save the directory "module.libs" to be used in __startup__
                # to simulate what is patched by delvewheel. Using zip file
                # the value of __file__ is in the zip, not in the "lib".
                dirs = module.libs_dirs()
                if dirs:
                    libs = self.constants_module.values.get("__LIBS__")
                    libs_dirs = (libs.split(os.pathsep) if libs else []) + dirs
                    self.add_constant("__LIBS__", os.pathsep.join(libs_dirs))

        if module.code is not None:
            if self.replace_paths:
                module.code = self._replace_paths_in_code(module)

            # Scan the module code for import statements
            self._scan_code(module, deferred_imports)

            # Verify __package__ in use
            module.code = code_object_replace_package(module)
        elif module.stub_code is not None:
            self._scan_code(module, deferred_imports, module.stub_code)

        # using lazy loader
        if module.root.lazy and module.stub_code:
            self._scan_code(module, deferred_imports, module.stub_code)

        module.in_import = False
        return module

    def _load_module_from_file(
        self, name: str, filename: Path, deferred_imports: DeferredList
    ) -> Module | None:
        """Load the module from the filename."""
        loader: ExecutionLoader | None = None

        ext = filename.suffix
        path = os.fspath(filename)
        if not ext or ext in importlib.machinery.SOURCE_SUFFIXES:
            loader = importlib.machinery.SourceFileLoader(name, path)
        elif ext in importlib.machinery.BYTECODE_SUFFIXES:
            loader = importlib.machinery.SourcelessFileLoader(name, path)
        elif ext in importlib.machinery.EXTENSION_SUFFIXES:
            loader = importlib.machinery.ExtensionFileLoader(name, path)

        module = self._add_module(name, filename=filename)
        self._load_module_code(module, loader, deferred_imports)
        return module

    def _missing_hook(self, caller: Module, module_name: str) -> None:
        """Run hook for missing module."""
        if module_name in DEFAULT_IGNORE_NAMES:
            return
        normalized_name = module_name.replace(".", "_")
        try:
            method = resolve_name(f"cx_Freeze.hooks:missing_{normalized_name}")
        except (AttributeError, ValueError):
            pass
        else:
            method(self, caller)
        if module_name not in caller.ignore_names:
            callers = self._bad_modules.setdefault(module_name, {})
            callers[caller.name] = None

    def _replace_paths_in_code(
        self, module: Module, code: CodeType | None = None
    ) -> CodeType:
        """Replace paths in the code as directed, returning a new code object
        with the modified paths in place.
        """
        top_level_module: Module = module.root
        if code is None:
            code = module.code
        # Prepare the new filename.
        original_filename = Path(code.co_filename)
        for search_value, replace_value in self.replace_paths:
            if search_value == "*":
                if top_level_module.file is None:
                    continue
                if top_level_module.path:
                    search_dir = top_level_module.file.parent.parent
                else:
                    search_dir = top_level_module.file.parent
            else:
                search_dir = Path(search_value)
            with suppress(ValueError):
                relative = original_filename.relative_to(search_dir)
                new_filename = replace_value / relative
                break
        else:
            new_filename = original_filename

        # Run on subordinate code objects from function & class definitions.
        consts = list(code.co_consts)
        for i, const in enumerate(consts):
            if isinstance(const, type(code)):
                consts[i] = self._replace_paths_in_code(
                    top_level_module, const
                )

        return code_object_replace(
            code, co_consts=consts, co_filename=os.fspath(new_filename)
        )

    def _scan_code(
        self,
        module: Module,
        deferred_imports: DeferredList,
        code: CodeType | None = None,
        top_level: bool = True,
    ) -> None:
        """Scan code, looking for imported modules and keeping track of the
        constants that have been created in order to better tell which
        modules are truly missing.
        """
        if code is None:
            code = module.code

        imported_module = None
        for opc, args in scan_code(code):
            # import statement: attempt to import module
            if "import" in opc:
                name, relative_import_index, from_list = args
                if opc in ("__import__", "import_module"):
                    logger.debug("Scan code detected %s(%r)", opc, name)
                if name not in module.exclude_names:
                    imported_module = self._import_module(
                        name, deferred_imports, module, relative_import_index
                    )
                    if imported_module is not None and (
                        from_list
                        and from_list != ("*",)
                        and imported_module.path is not None
                    ):
                        self._ensure_from_list(
                            module,
                            imported_module,
                            from_list,
                            deferred_imports,
                        )

            # import * statement: copy all global names
            elif opc == "star" and top_level and imported_module is not None:
                module.global_names.update(imported_module.global_names)

            # store operation: track only top level
            elif opc == "store" and top_level:
                (name,) = args
                module.global_names.add(name)

        # Scan the code objects from function & class definitions
        for constant in code.co_consts:
            if isinstance(constant, type(code)):
                self._scan_code(
                    module, deferred_imports, code=constant, top_level=False
                )

    def add_alias(self, name: str, alias_for: str) -> None:
        """Add an alias for a particular module; when an attempt is made to
        import a module using the alias name, import the actual name instead.
        """
        self.aliases[name] = alias_for

    def add_base_modules(self) -> None:
        """Add the base modules to the finder. These are the modules that
        Python imports itself during initialization and, if not found,
        can result in behavior that differs from running from source;
        also include modules used within the bootstrap code.

        When cx_Freeze is built, these modules (and modules they load) are
        included in the startup zip file.
        """
        self.include_module("collections")
        self.include_package("encodings")
        self.include_module("importlib.abc")
        self.include_module("io")
        self.include_module("os")
        self.include_module("sys")
        self.include_module("traceback")
        self.include_module("unicodedata")
        self.include_module("warnings")
        self.include_module("zlib")

    def add_constant(self, name: str, value: str) -> None:
        """Makes available a constant in the module BUILD_CONSTANTS which is
        used in the initscripts.
        """
        self.constants_module.values[name] = value

    def exclude_dependent_files(self, filename: Path | str) -> None:
        """Exclude the dependent files of the named file from the resulting
        frozen executable.
        """
        self.excluded_dependent_files.add(Path(filename))

    def exclude_module(self, name: str) -> None:
        """Exclude the named module and its submodules from the resulting
        frozen executable.
        """
        modules_to_discard = [
            mod for mod in self.excludes if mod.startswith(f"{name}.")
        ]
        self.excludes.difference_update(modules_to_discard)
        self.excludes.add(name)

        modules_to_discard = [
            mod for mod in self._modules if mod.startswith(f"{name}.")
        ]
        for mod in modules_to_discard:
            self._modules.pop(mod, None)
        self._modules[name] = None

        modules_to_discard = [
            mod
            for mod in self.modules
            if mod.name == name or mod.name.startswith(f"{name}.")
        ]
        for mod in modules_to_discard:
            self.modules.remove(mod)

    def include_file_as_module(
        self, path: Path | str, name: str | None = None
    ) -> Module:
        """Include the named file as a module in the frozen executable."""
        path = Path(path)
        if name is None:
            name = path.stem
        deferred_imports: DeferredList = []
        module = self._load_module_from_file(name, path, deferred_imports)
        if module is not None:
            parent = self._get_parent_by_name(name)
            if parent is not None:
                parent.global_names.add(module.name)
                module.parent = parent
        self._import_deferred_imports(deferred_imports)
        return module

    def include_files(
        self,
        source_path: Path | str,
        target_path: Path | str,
        copy_dependent_files: bool = True,
    ) -> None:
        """Include the files in the given directory in the target build."""
        self.included_files += process_path_specs([(source_path, target_path)])
        if not copy_dependent_files:
            self.exclude_dependent_files(source_path)

    def include_module(self, name: str) -> Module:
        """Include the named module in the frozen executable."""
        # Includes has priority over excludes.
        self.excludes.discard(name)
        # Remove the module in the module cache before trying to import it.
        if self._modules.get(name) is None:
            self._modules.pop(name, None)
        # Include the module.
        deferred_imports: DeferredList = []
        module = self._import_module(name, deferred_imports)
        self._import_deferred_imports(deferred_imports, skip_in_import=True)
        return module

    def include_package(self, name: str) -> Module:
        """Include the named package and any submodules in the frozen
        executable.
        """
        # Includes has priority over excludes.
        self.excludes.discard(name)
        # Remove the module in the module cache before trying to import it.
        if self._modules.get(name) is None:
            self._modules.pop(name, None)
        # Include the package.
        deferred_imports: DeferredList = []
        module = self._import_module(name, deferred_imports)
        if module.path:
            self._import_all_sub_modules(module, deferred_imports)
        self._import_deferred_imports(deferred_imports, skip_in_import=True)
        return module

    def report_missing_modules(self) -> None:
        """Display a list of modules that weren't found."""
        if self._bad_modules:
            print("Missing modules:")
            for name in sorted(self._bad_modules.keys()):
                callers = sorted(self._bad_modules[name].keys())
                print(f"? {name} imported from", ", ".join(callers))
            print("This is not necessarily a problem - the modules ", end="")
            print("may not be needed on this platform.\n")

    @property
    def optimize(self) -> int:
        """The value of optimize flag propagated according to the user's
        choice.
        """
        return self._optimize_flag

    @optimize.setter
    def optimize(self, value: int) -> None:
        # The value of optimize is checked in '.command.build_exe' or '.cli'.
        # This value is unlikely to be wrong, yet we check and ignore any
        # divergent value.
        if -1 <= value <= 2:
            self._optimize_flag = value

    def zip_include_files(
        self,
        source_path: str | Path,
        target_path: str | Path | PurePath | None = None,
    ) -> None:
        """Include files or all of the files in a directory to the zip file."""
        self.zip_includes.extend(
            process_path_specs([(source_path, target_path)])
        )
