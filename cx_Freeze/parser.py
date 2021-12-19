"""
Implements `Parser` interface to create an abstraction to parse binary files.
"""

from abc import ABC, abstractmethod
import os
from pathlib import Path
import sys
from typing import Dict, List, Set, Union

WIN32 = sys.platform == "win32"

if WIN32:
    from .util import BindError, GetDependentFiles

PE_EXT = (".exe", ".dll", ".pyd")


class Parser(ABC):
    """`Parser` interface."""

    def __init__(self) -> None:
        self.dependent_files: Dict[Path, Set[Path]] = {}
        self.silent: int = 0

    @abstractmethod
    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        """Return the file's dependencies using platform-specific tools (the
        imagehlp library on Windows, otool on Mac OS X and ldd on Linux);
        limit this list by the exclusion lists as needed.
        (Implemented separately for each platform.)"""


class PEParser(Parser):
    """`PEParser` is based on the cx_Freeze.util extension module."""

    def is_PE(self, path: Union[str, Path]) -> bool:
        """Determines whether the file is a PE file."""
        if isinstance(path, str):
            path = Path(path)
        return path.suffix.lower().endswith(PE_EXT) and path.is_file()

    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        if isinstance(path, str):
            path = Path(path)
        try:
            return self.dependent_files[path]
        except KeyError:
            pass
        dependent_files: Set[Path] = set()
        if not self.is_PE(path):
            return dependent_files
        orig_path = os.environ["PATH"]
        os.environ["PATH"] = orig_path + os.pathsep + os.pathsep.join(sys.path)
        try:
            files: List[str] = GetDependentFiles(path)
        except BindError as exc:
            # Sometimes this gets called when path is not actually
            # a library (See issue 88).
            if self.silent < 3:
                print("WARNING: ignoring error during ", end="")
                print(f"GetDependentFiles({path}):", exc)
        else:
            dependent_files = {Path(dep) for dep in files}
        os.environ["PATH"] = orig_path
        self.dependent_files[path] = dependent_files
        return dependent_files
