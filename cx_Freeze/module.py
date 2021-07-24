"""
Base class for module.
"""

from contextlib import suppress
import datetime
from keyword import iskeyword
import os
from pathlib import Path
import shutil
import socket
from tempfile import TemporaryDirectory
from types import CodeType
from typing import Dict, List, Optional, Set, Tuple, Union

import importlib_metadata

from .exception import ConfigError


__all__ = ["ConstantsModule", "Module"]


class DistributionCache(importlib_metadata.PathDistribution):
    """Cache the distribution package."""

    _cachedir = TemporaryDirectory(prefix="cxfreeze-")

    @staticmethod
    def at(path):
        return DistributionCache(Path(path))

    at.__doc__ = importlib_metadata.PathDistribution.at.__doc__

    @classmethod
    def from_name(cls, name):
        distribution = super().from_name(name)
        # Cache dist-info files in a temporary directory
        temp_dir = Path(cls._cachedir.name)
        dist_dir = None
        files = distribution.files or []
        prep = importlib_metadata.Prepared(distribution.name)
        normalized = prep.normalized
        legacy_normalized = prep.legacy_normalized
        for file in files:
            # only existing dist-info files
            if (
                not file.match(f"{name}-*.dist-info/*")
                and not file.match(f"{distribution.name}-*.dist-info/*")
                and not file.match(f"{normalized}-*.dist-info/*")
                and not file.match(f"{legacy_normalized}-*.dist-info/*")
            ):
                continue
            src_path = file.locate()
            if not src_path.exists():
                continue
            dst_path = temp_dir / file.as_posix()
            if dist_dir is None:
                dist_dir = dst_path.parent
                dist_dir.mkdir(exist_ok=True)
            shutil.copy2(src_path, dst_path)
        if dist_dir is None:
            raise importlib_metadata.PackageNotFoundError(name)
        return cls.at(dist_dir)

    from_name.__doc__ = importlib_metadata.PathDistribution.from_name.__doc__


class Module:
    """
    The Module class.
    """

    _file: Optional[Path]

    def __init__(
        self,
        name: str,
        path: Optional[List[Union[Path, str]]] = None,
        file_name: Optional[Union[Path, str]] = None,
        parent: Optional["Module"] = None,
    ):
        self.name: str = name
        self.path: Optional[List[Path]] = (
            [Path(p) for p in path] if path else None
        )
        self.file = file_name
        self.parent: Optional["Module"] = parent
        self.code: Optional[CodeType] = None
        self.distribution: Optional[DistributionCache] = None
        self.exclude_names: Set[str] = set()
        self.global_names: Set[str] = set()
        self.ignore_names: Set[str] = set()
        self.in_import: bool = True
        self.source_is_zip_file: bool = False
        self._in_file_system: bool = True
        # cache the dist-info files (metadata)
        self.update_distribution(name)

    @property
    def file(self) -> Optional[Path]:
        """Module filename"""
        return self._file

    @file.setter
    def file(self, file_name: Optional[Union[Path, str]]):
        self._file = Path(file_name) if file_name else None

    def update_distribution(self, name: str) -> None:
        """Update the distribution cache based on its name.
        This method may be used to link an distribution's name to a module.

        Example: ModuleFinder cannot detects the distribution of _cffi_backend
        but in a hook we can link it to 'cffi'.
        """
        try:
            distribution = DistributionCache.from_name(name)
        except importlib_metadata.PackageNotFoundError:
            distribution = None
        if distribution is None:
            return
        try:
            requires = importlib_metadata.requires(distribution.name) or []
        except importlib_metadata.PackageNotFoundError:
            requires = []
        for req in requires:
            req_name = req.partition(" ")[0]
            with suppress(importlib_metadata.PackageNotFoundError):
                DistributionCache.from_name(req_name)
        self.distribution = distribution

    def __repr__(self) -> str:
        parts = [f"name={self.name!r}"]
        if self.file is not None:
            parts.append(f"file={self.file!r}")
        if self.path is not None:
            parts.append(f"path={self.path!r}")
        return "<Module {}>".format(", ".join(parts))

    @property
    def in_file_system(self) -> bool:
        """Returns a boolean indicating if the module will be stored in the
        file system or not."""
        if self.parent is not None:
            return self.parent.in_file_system
        if self.path is None or self.file is None:
            return False
        return self._in_file_system

    @in_file_system.setter
    def in_file_system(self, value) -> None:
        self._in_file_system = value


class ConstantsModule:
    """
    Base ConstantsModule class.
    """

    def __init__(
        self,
        release_string: Optional[str] = None,
        copyright_string: Optional[str] = None,
        module_name: str = "BUILD_CONSTANTS",
        time_format: str = "%B %d, %Y %H:%M:%S",
        constants: Optional[List[str]] = None,
    ):
        self.module_name: str = module_name
        self.time_format: str = time_format
        self.values: Dict[str, str] = {}
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
                    value = eval(string_value)
                if (not name.isidentifier()) or iskeyword(name):
                    raise ConfigError(
                        f"Invalid constant name in ConstantsModule ({name!r})"
                    )
                self.values[name] = value
        self._dir: TemporaryDirectory = TemporaryDirectory(prefix="cxfreeze")
        self.module_path: str = os.path.join(self._dir.name, "constants.py")

    def create(self, modules: List[Module]) -> Tuple[str, str]:
        """
        Create the module which consists of declaration statements for each
        of the values.
        """
        today = datetime.datetime.today()
        source_timestamp = 0
        for module in modules:
            if module.file is None:
                continue
            if module.source_is_zip_file:
                continue
            if not module.file.exists():
                raise ConfigError(
                    f"No file named {module.file!s} (for module {module.name})"
                )
            timestamp = module.file.stat().st_mtime
            source_timestamp = max(source_timestamp, timestamp)
        stamp = datetime.datetime.fromtimestamp(source_timestamp)
        self.values["BUILD_TIMESTAMP"] = today.strftime(self.time_format)
        self.values["BUILD_HOST"] = socket.gethostname().split(".")[0]
        self.values["SOURCE_TIMESTAMP"] = stamp.strftime(self.time_format)
        source_parts = []
        names = list(self.values.keys())
        names.sort()
        for name in names:
            value = self.values[name]
            source_parts.append(f"{name} = {value!r}")
        with open(self.module_path, "w", encoding="UTF-8") as file:
            file.write("\n".join(source_parts))
        return self.module_path, self.module_name
