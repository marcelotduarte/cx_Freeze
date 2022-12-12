"""A collection of functions which are triggered automatically by finder when
PyQt6 package is included."""

from __future__ import annotations

import os
import sys

from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import copy_qt_files
from .._qthooks import load_qt_qt as load_pyqt6_qt
from .._qthooks import load_qt_qtcharts as load_pyqt6_qtcharts
from .._qthooks import (
    load_qt_qtdatavisualization as load_pyqt6_qtdatavisualization,
)
from .._qthooks import load_qt_qtdesigner as load_pyqt6_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyqt6_qtgui
from .._qthooks import load_qt_qthelp as load_pyqt6_qthelp
from .._qthooks import load_qt_qtlocation as load_pyqt6_qtlocation
from .._qthooks import load_qt_qtmultimedia as load_pyqt6_qtmultimedia
from .._qthooks import (
    load_qt_qtmultimediawidgets as load_pyqt6_qtmultimediawidgets,
)
from .._qthooks import load_qt_qtopengl as load_pyqt6_qtopengl
from .._qthooks import load_qt_qtpositioning as load_pyqt6_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyqt6_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyqt6_qtqml
from .._qthooks import load_qt_qtscripttools as load_pyqt6_qtscripttools
from .._qthooks import load_qt_qtsql as load_pyqt6_qtsql
from .._qthooks import load_qt_qtsvg as load_pyqt6_qtsvg
from .._qthooks import load_qt_qttest as load_pyqt6_qttest
from .._qthooks import load_qt_qtuitools as load_pyqt6_qtuitools
from .._qthooks import load_qt_qtwebengine as load_pyqt6_qtwebengine
from .._qthooks import load_qt_qtwebenginecore as load_pyqt6_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyqt6_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwebsockets as load_pyqt6_qtwebsockets
from .._qthooks import load_qt_qtwidgets
from .._qthooks import load_qt_qtxmlpatterns as load_pyqt6_qtxmlpatterns
from .._qthooks import load_qt_uic as load_pyqt6_uic


def load_pyqt6(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt6 __init__ to locate and load plugins and
    resources."""

    # Include QtCore module and sip module needed by all modules
    finder.include_module("PyQt6.QtCore")
    finder.include_module("PyQt6.sip")

    # Activate an optimized mode when PyQt6 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyqt6", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PyQt6._cx_freeze_qt_debug")

    # Inject code to init
    code_string = module.file.read_text()
    code_string += """
# cx_Freeze patch start
import PyQt6._cx_freeze_qt_debug
# cx_Freeze patch end
"""
    module.code = compile(code_string, os.fspath(module.file), "exec")


def load_pyqt6_qtwidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    load_qt_qtwidgets(finder, module)
    if sys.platform == "linux":
        copy_qt_files(finder, "PyQt6", "LibrariesPath", "libQt6Widgets.so.6")


__all__ = [
    "load_pyqt6",
    "load_pyqt6_qt",
    "load_pyqt6_qtcharts",
    "load_pyqt6_qtdatavisualization",
    "load_pyqt6_qtdesigner",
    "load_pyqt6_qtgui",
    "load_pyqt6_qthelp",
    "load_pyqt6_qtlocation",
    "load_pyqt6_qtmultimedia",
    "load_pyqt6_qtmultimediawidgets",
    "load_pyqt6_qtopengl",
    "load_pyqt6_qtpositioning",
    "load_pyqt6_qtprintsupport",
    "load_pyqt6_qtqml",
    "load_pyqt6_qtscripttools",
    "load_pyqt6_qtsql",
    "load_pyqt6_qtsvg",
    "load_pyqt6_qttest",
    "load_pyqt6_qtuitools",
    "load_pyqt6_qtwebengine",
    "load_pyqt6_qtwebenginecore",
    "load_pyqt6_qtwebenginewidgets",
    "load_pyqt6_qtwebsockets",
    "load_pyqt6_qtwidgets",
    "load_pyqt6_qtxmlpatterns",
    "load_pyqt6_uic",
]
