"""
Base class for module.
"""

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

    @staticmethod
    def at(path):
        return DistributionCache(Path(path))

    at.__doc__ = importlib_metadata.PathDistribution.at.__doc__


class Module:
    """
    The Module class.
    """

    def __init__(
        self,
        name: str,
        path: Optional[str] = None,
        file_name: Optional[str] = None,
        parent: Optional["Module"] = None,
        *,
        rootcachedir: Union[str, Path],
    ):
        self.name: str = name
        self.path: Optional[str] = path
        self.file: Optional[str] = file_name
        self.parent: Optional["Module"] = parent
        self.rootcachedir: Path = Path(rootcachedir)
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

    def update_distribution(self, name: str) -> None:
        """Update the distribution cache. This method may be used to when the
        name of the distribution is different of the import name.

        Example: ModuleFinder detects the name yaml (the package name), but
        the distribution name is PyYAML. So, a hook can use this method.
        """
        dist = self._cache_dist_info(name)
        if dist is None:
            return
        try:
            requires = importlib_metadata.requires(name)
        except importlib_metadata.PackageNotFoundError:
            requires = None
        if requires is not None:
            for req in requires:
                req_name = req.partition(" ")[0]
                self._cache_dist_info(req_name)
        self.distribution = dist

    def _cache_dist_info(self, name: str) -> Optional[DistributionCache]:
        """Cache the dist-info files in a temporary directory."""
        dist_dir = None
        try:
            files = importlib_metadata.files(name) or []
        except importlib_metadata.PackageNotFoundError:
            files = []
        # select only dist-info files
        files = [file for file in files if file.match("*.dist-info/*")]
        for file in files:
            src_path = file.locate()
            if not src_path.exists():
                continue
            dst_path = self.rootcachedir / file.as_posix()
            if dist_dir is None:
                dist_dir = dst_path.parent
                dist_dir.mkdir(exist_ok=True)
            shutil.copy2(src_path, dst_path)
        if dist_dir is None:
            return None
        return DistributionCache.at(dist_dir)

    def __repr__(self) -> str:
        parts = [f"name={self.name!r}"]
        if self.file is not None:
            parts.append(f"file={self.file!r}")
        if self.path is not None:
            parts.append(f"path={self.path!r}")
        return "<Module {}>".format(", ".join(parts))

    @property
    def in_file_system(self) -> bool:
        """
        Returns a boolean indicating if the module will be stored in the
        file system or not.
        """
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
            if not os.path.exists(module.file):
                raise ConfigError(
                    f"No file named {module.file} (for module {module.name})"
                )
            timestamp = os.stat(module.file).st_mtime
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
