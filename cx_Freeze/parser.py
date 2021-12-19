"""
Implements `Parser` interface to create an abstraction to parse binary files.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Set, Union


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
