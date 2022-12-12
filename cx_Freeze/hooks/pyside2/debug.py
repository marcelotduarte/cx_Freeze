"""
This module is used to inject a debug code to show QLibraryInfo paths
if environment variable QT_DEBUG is set.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def qt_debug():
    """Show QLibraryInfo paths."""

    qtcore = __import__("PySide2", fromlist=["QtCore"]).QtCore
    data = {}
    for key, value in qtcore.QLibraryInfo.__dict__.items():
        if isinstance(value, qtcore.QLibraryInfo.LibraryLocation):
            data[key] = Path(qtcore.QLibraryInfo.location(value))
    print("QLibraryInfo:", file=sys.stderr)
    for key, value in sorted(data.items()):
        print(" ", key, value, file=sys.stderr)
    print("LibraryPaths:", file=sys.stderr)
    print(" ", qtcore.QCoreApplication.libraryPaths(), file=sys.stderr)


if os.environ.get("QT_DEBUG"):
    qt_debug()
