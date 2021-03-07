"""
Base class for module.
"""

import os
import shutil
from types import CodeType
from typing import List, Optional

import importlib_metadata


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
        dist_cachedir: str,
    ):
        self.name: str = name
        self.path: Optional[str] = path
        self.file: Optional[str] = file_name
        self.parent: Optional["Module"] = parent
        self.dist_cachedir = dist_cachedir
        self.code: Optional[CodeType] = None
        self.global_names: set = set()
        self.exclude_names: set = set()
        self.ignore_names: set = set()
        self.source_is_zip_file: bool = False
        self.in_import: bool = True
        self.store_in_file_system: bool = True
        # dist-info files (metadata)
        self.dist_files: List[str] = []
        self._cache_dist_info(name)
        try:
            requires = importlib_metadata.requires(name)
        except importlib_metadata.PackageNotFoundError:
            requires = None
        if requires is not None:
            for req in requires:
                req_name = req.partition(" ")[0]
                self._cache_dist_info(req_name)

    def _cache_dist_info(self, package_name) -> None:
        """Cache the dist-info files."""
        try:
            files = importlib_metadata.files(package_name)
        except importlib_metadata.PackageNotFoundError:
            files = None
        if files is None:
            return
        # select only dist-info files
        files = [file for file in files if file.match("*.dist-info/*")]
        if files:
            for file in files:
                dist_path = os.path.join(
                    self.dist_cachedir.name, os.path.normpath(file.as_posix())
                )
                os.makedirs(os.path.dirname(dist_path), exist_ok=True)
                shutil.copyfile(str(file.locate()), dist_path)
                self.dist_files.append(file.as_posix())

    def __repr__(self) -> str:
        parts = [f"name={self.name!r}"]
        if self.file is not None:
            parts.append(f"file={self.file!r}")
        if self.path is not None:
            parts.append(f"path={self.path!r}")
        return "<Module {}>".format(", ".join(parts))

    def AddGlobalName(self, name: str) -> None:
        self.global_names.add(name)

    def ExcludeName(self, name: str) -> None:
        self.exclude_names.add(name)

    def IgnoreName(self, name: str) -> None:
        self.ignore_names.add(name)

    @property
    def in_file_system(self) -> bool:
        if self.parent is not None:
            return self.parent.in_file_system
        if self.path is None or self.file is None:
            return False
        return self.store_in_file_system
