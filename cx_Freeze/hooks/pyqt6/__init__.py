"""A collection of functions which are triggered automatically by finder when
PyQt6 package is included.
"""
from __future__ import annotations

import os
import sys
from textwrap import dedent

from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import copy_qt_files
from .._qthooks import load_qt_qtdesigner as load_pyqt6_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyqt6_qtgui
from .._qthooks import load_qt_qtmultimedia as load_pyqt6_qtmultimedia
from .._qthooks import load_qt_qtnetwork as load_pyqt6_qtnetwork
from .._qthooks import load_qt_qtopengl as load_pyqt6_qtopengl
from .._qthooks import load_qt_qtopenglwidgets as load_pyqt6_qtopenglwidgets
from .._qthooks import load_qt_qtpositioning as load_pyqt6_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyqt6_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyqt6_qtqml
from .._qthooks import load_qt_qtquick as load_pyqt6_qtquick
from .._qthooks import load_qt_qtsql as load_pyqt6_qtsql
from .._qthooks import load_qt_qtsvg as load_pyqt6_qtsvg
from .._qthooks import load_qt_qtwebenginecore as load_pyqt6_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyqt6_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwidgets as load_pyqt6_qtwidgets_base


def load_pyqt6(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt6 __init__ to locate and load plugins and
    resources.
    """
    # Activate an optimized mode when PyQt6 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyqt6", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PyQt6._cx_freeze_qt_debug")

    # Include a qt.conf in the module path (Prefix = lib/PyQt6)
    qt_conf = get_resource_file_path("hooks/pyqt6", "qt", ".conf")
    finder.include_files(qt_conf, qt_conf.name)

    # Include a copy of qt.conf (used by QtWebEngine)
    copy_qt_files(finder, "PyQt6", "LibraryExecutablesPath", "qt.conf")

    # Inject code to init
    code_string = module.file.read_text(encoding="utf_8")
    code_string += dedent(
        """
        # cx_Freeze patch start
        import PyQt6._cx_freeze_qt_debug
        # cx_Freeze patch end
        """
    )
    module.code = compile(code_string, os.fspath(module.file), "exec")


def load_pyqt6_qtwidgets(finder: ModuleFinder, module: Module) -> None:
    """Include module dependency."""
    load_pyqt6_qtwidgets_base(finder, module)
    if sys.platform == "linux":
        copy_qt_files(finder, "PyQt6", "LibrariesPath", "libQt6Widgets.so.6")


__all__ = [
    "load_pyqt6",
    "load_pyqt6_qtdesigner",
    "load_pyqt6_qtgui",
    "load_pyqt6_qtmultimedia",
    "load_pyqt6_qtnetwork",
    "load_pyqt6_qtopengl",
    "load_pyqt6_qtopenglwidgets",
    "load_pyqt6_qtpositioning",
    "load_pyqt6_qtprintsupport",
    "load_pyqt6_qtquick",
    "load_pyqt6_qtqml",
    "load_pyqt6_qtsql",
    "load_pyqt6_qtsvg",
    "load_pyqt6_qtwebenginecore",
    "load_pyqt6_qtwebenginewidgets",
    "load_pyqt6_qtwidgets",
]
