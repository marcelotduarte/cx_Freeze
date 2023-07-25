"""Base class for Module and ConstantsModule."""

from __future__ import annotations

import ast
import datetime
import socket
from collections.abc import Sequence
from contextlib import suppress
from keyword import iskeyword
from pathlib import Path
from types import CodeType

from ._compat import importlib_metadata
from .common import TemporaryPath
from .exception import OptionError

__all__ = ["ConstantsModule", "Module"]


class DistributionCache(importlib_metadata.PathDistribution):
    """Cache the distribution package."""

    _cachedir = TemporaryPath()

    @staticmethod
    def at(path: str | Path):
        return DistributionCache(Path(path))

    at.__doc__ = importlib_metadata.PathDistribution.at.__doc__

    @classmethod
    def from_name(cls, name: str):
        """Return the Distribution for the given package name.

        :param name: The name of the distribution package to search for.
        :return: The Distribution instance (or subclass thereof) for the named
            package, if found.
        :raises PackageNotFoundError: When the named package's distribution
            metadata cannot be found.
        :raises ValueError: When an invalid value is supplied for name.
        """
        distribution = super().from_name(name)

        # Cache dist-info files in a temporary directory
        normalized_name = getattr(distribution, "_normalized_name", None)
        if normalized_name is None:
            normalized_name = importlib_metadata.Prepared.normalize(name)
        source_path = getattr(distribution, "_path", None)
        if source_path is None:
            mask = f"{normalized_name}-{distribution.version}*-info"
            source_path = next(iter(distribution.locate_file("").glob(mask)))
        if not source_path.exists():
            raise importlib_metadata.PackageNotFoundError(name)

        target_name = f"{normalized_name}-{distribution.version}.dist-info"
        target_path = cls._cachedir.path / target_name
        target_path.mkdir(exist_ok=True)

        purelib = None
        if source_path.name.endswith(".dist-info"):
            for source in source_path.rglob("*"):  # type: Path
                target = target_path / source.relative_to(source_path)
                if source.is_dir():
                    target.mkdir(exist_ok=True)
                else:
                    target.write_bytes(source.read_bytes())
        elif source_path.is_file():
            # old egg-info file is converted to dist-info
            target = target_path / "METADATA"
            target.write_bytes(source_path.read_bytes())
            purelib = (source_path.parent / (normalized_name + ".py")).exists()
        else:
            # Copy minimal data from egg-info directory into dist-info
            source = source_path / "PKG-INFO"
            if source.is_file():
                target = target_path / "METADATA"
                target.write_bytes(source.read_bytes())
            source = source_path / "top_level.txt"
            if source.is_file():
                target = target_path / "top_level.txt"
                target.write_bytes(source.read_bytes())
            purelib = not source_path.joinpath("not-zip-safe").is_file()

        cls._write_wheel_distinfo(target_path, purelib)
        cls._write_record_distinfo(target_path)

        return cls.at(target_path)

    @staticmethod
    def _write_wheel_distinfo(target_path: Path, purelib: bool):
        """Create a WHEEL file if it doesn't exist."""
        target = target_path / "WHEEL"
        if not target.exists():
            project = Path(__file__).parent.name
            version = importlib_metadata.version(project)
            root_is_purelib = "true" if purelib else "false"
            text = [
                "Wheel-Version: 1.0",
                f"Generator: {project} ({version})",
                f"Root-Is-Purelib: {root_is_purelib}",
                "Tag: py3-none-any",
            ]
            with target.open(mode="w", encoding="utf_8", newline="") as file:
                file.write("\n".join(text))

    @staticmethod
    def _write_record_distinfo(target_path: Path):
        """Recreate a minimal RECORD file."""
        target_name = target_path.name
        record = []
        for file in target_path.iterdir():
            record.append(f"{target_name}/{file.name},,")
        record.append(f"{target_name}/RECORD,,")
        target = target_path / "RECORD"
        with target.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(record))


class Module:
    """The Module class."""

    def __init__(
        self,
        name: str,
        path: Sequence[Path | str] | None = None,
        filename: Path | str | None = None,
        parent: Module | None = None,
    ):
        self.name: str = name
        self.path: list[Path] | None = list(map(Path, path)) if path else None
        self._file: Path | None = Path(filename) if filename else None
        self.parent: Module | None = parent
        self.code: CodeType | None = None
        self.distribution: DistributionCache | None = None
        self.exclude_names: set[str] = set()
        self.global_names: set[str] = set()
        self.ignore_names: set[str] = set()
        self.in_import: bool = True
        self.source_is_string: bool = False
        self.source_is_zip_file: bool = False
        self._in_file_system: int = 1
        # cache the dist-info files (metadata)
        self.update_distribution(name)

    def __repr__(self) -> str:
        parts = [f"name={self.name!r}"]
        if self.file is not None:
            parts.append(f"file={self.file!r}")
        if self.path is not None:
            parts.append(f"path={self.path!r}")
        join_parts = ", ".join(parts)
        return f"<Module {join_parts}>"

    @property
    def file(self) -> Path | None:
        """Module filename."""
        return self._file

    @file.setter
    def file(self, filename: Path | str | None):
        self._file = Path(filename) if filename else None

    @property
    def in_file_system(self) -> int:
        """Returns a value indicating where the module/package will be stored:
        0. in a zip file (not directly in the file system)
        1. in the file system, package with modules and data
        2. in the file system, only detected modules.
        """
        if self.parent is not None:
            return self.parent.in_file_system
        if self.path is None or self.file is None:
            return 0
        return self._in_file_system

    @in_file_system.setter
    def in_file_system(self, value: int) -> None:
        self._in_file_system: int = value

    def update_distribution(self, name: str) -> None:
        """Update the distribution cache based on its name.
        This method may be used to link an distribution's name to a module.

        Example: ModuleFinder cannot detects the distribution of _cffi_backend
        but in a hook we can link it to 'cffi'.
        """
        try:
            distribution = DistributionCache.from_name(name)
        except (importlib_metadata.PackageNotFoundError, ValueError):
            distribution = None
        if distribution is None:
            return
        try:
            requires = importlib_metadata.requires(distribution.name) or []
        except (importlib_metadata.PackageNotFoundError, ValueError):
            requires = []
        for req in requires:
            req_name = req.partition(" ")[0]
            with suppress(importlib_metadata.PackageNotFoundError, ValueError):
                DistributionCache.from_name(req_name)
        self.distribution = distribution


class ConstantsModule:
    """Base ConstantsModule class."""

    def __init__(
        self,
        release_string: str | None = None,
        copyright_string: str | None = None,
        module_name: str = "BUILD_CONSTANTS",
        time_format: str = "%B %d, %Y %H:%M:%S",
        constants: list[str] | None = None,
    ):
        self.module_name: str = module_name
        self.time_format: str = time_format
        self.values: dict[str, str] = {}
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
                    value = ast.literal_eval(string_value)
                if (not name.isidentifier()) or iskeyword(name):
                    raise OptionError(
                        f"Invalid constant name in ConstantsModule ({name!r})"
                    )
                self.values[name] = value
        self.module_path: TemporaryPath = TemporaryPath("constants.py")

    def create(self, modules: list[Module]) -> tuple[Path, str]:
        """Create the module which consists of declaration statements for each
        of the values.
        """
        today = datetime.datetime.today()
        source_timestamp = 0
        for module in modules:
            if module.file is None or module.source_is_string:
                continue
            if module.source_is_zip_file:
                continue
            if not module.file.exists():
                raise OptionError(
                    f"No file named {module.file!s} (for module {module.name})"
                )
            timestamp = module.file.stat().st_mtime
            source_timestamp = max(source_timestamp, timestamp)
        stamp = datetime.datetime.fromtimestamp(source_timestamp)
        self.values["BUILD_TIMESTAMP"] = today.strftime(self.time_format)
        self.values["BUILD_HOST"] = socket.gethostname().split(".")[0]
        self.values["SOURCE_TIMESTAMP"] = stamp.strftime(self.time_format)
        parts = []
        names = list(self.values.keys())
        names.sort()
        for name in names:
            value = self.values[name]
            parts.append(f"{name} = {value!r}")
        with self.module_path.path.open(
            mode="w", encoding="utf_8", newline=""
        ) as file:
            file.write("\n".join(parts))
        return self.module_path.path, self.module_name
