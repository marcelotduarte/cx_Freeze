"""
This module is used to inject a code to guessing and set the plugins directory.
"""
from __future__ import annotations

import sys
from pathlib import Path


def add_path():
    """Add library path."""

    executable_dir = Path(sys.executable).parent
    qt_root_dir = executable_dir / "lib" / "PyQt5"
    plugins_dir = qt_root_dir / "Qt5" / "plugins"  # PyQt5 5.15.4
    if not plugins_dir.is_dir():
        plugins_dir = qt_root_dir / "Qt" / "plugins"
    if not plugins_dir.is_dir():
        plugins_dir = qt_root_dir / "plugins"
    if plugins_dir.is_dir():
        qtcore = __import__("PyQt5", fromlist=["QtCore"]).QtCore
        qtcore.QCoreApplication.addLibraryPath(plugins_dir.as_posix())


add_path()
