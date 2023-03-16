"""Module used to inject a debug code to show QLibraryInfo paths if environment
variable QT_DEBUG is set.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def qt_debug():
    """Show QLibraryInfo paths."""
    qtcore = __import__("PyQt6", fromlist=["QtCore"]).QtCore
    lib = qtcore.QLibraryInfo
    source_paths: dict[str, Path] = {}
    if hasattr(lib.LibraryPath, "__members__"):
        for key, value in lib.LibraryPath.__members__.items():
            source_paths[key] = Path(lib.path(value))
    else:
        for key, value in lib.__dict__.items():
            if isinstance(value, lib.LibraryPath):
                source_paths[key] = Path(lib.path(value))
    print("QLibraryInfo:", file=sys.stderr)
    for key, value in source_paths.items():
        print(" ", key, value, file=sys.stderr)
    print("LibraryPaths:", file=sys.stderr)
    print(" ", qtcore.QCoreApplication.libraryPaths(), file=sys.stderr)


if os.environ.get("QT_DEBUG"):
    qt_debug()
