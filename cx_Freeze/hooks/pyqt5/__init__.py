"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included."""

from __future__ import annotations

import os

from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import load_qt_qt as load_pyqt5_qt
from .._qthooks import load_qt_qtcharts as load_pyqt5_qtcharts
from .._qthooks import (
    load_qt_qtdatavisualization as load_pyqt5_qtdatavisualization,
)
from .._qthooks import load_qt_qtdesigner as load_pyqt5_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyqt5_qtgui
from .._qthooks import load_qt_qthelp as load_pyqt5_qthelp
from .._qthooks import load_qt_qtlocation as load_pyqt5_qtlocation
from .._qthooks import load_qt_qtmultimedia as load_pyqt5_qtmultimedia
from .._qthooks import (
    load_qt_qtmultimediawidgets as load_pyqt5_qtmultimediawidgets,
)
from .._qthooks import load_qt_qtopengl as load_pyqt5_qtopengl
from .._qthooks import load_qt_qtpositioning as load_pyqt5_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyqt5_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyqt5_qtqml
from .._qthooks import load_qt_qtscripttools as load_pyqt5_qtscripttools
from .._qthooks import load_qt_qtsql as load_pyqt5_qtsql
from .._qthooks import load_qt_qtsvg as load_pyqt5_qtsvg
from .._qthooks import load_qt_qttest as load_pyqt5_qttest
from .._qthooks import load_qt_qtuitools as load_pyqt5_qtuitools
from .._qthooks import load_qt_qtwebengine as load_pyqt5_qtwebengine
from .._qthooks import load_qt_qtwebenginecore as load_pyqt5_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyqt5_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwebkit as load_pyqt5_qtwebkit
from .._qthooks import load_qt_qtwebsockets as load_pyqt5_qtwebsockets
from .._qthooks import load_qt_qtwidgets as load_pyqt5_qtwidgets
from .._qthooks import load_qt_qtxmlpatterns as load_pyqt5_qtxmlpatterns
from .._qthooks import load_qt_uic as load_pyqt5_uic


def load_pyqt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5 __init__ to locate and load plugins and
    resources. Also, this fixes issues with conda-forge versions."""

    # Include QtCore module needed by all modules
    finder.include_module("PyQt5.QtCore")

    # Activate an optimized mode when PyQt5 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
    qt_patch = get_resource_file_path("hooks/pyqt5", "add_library", ".py")
    finder.include_file_as_module(qt_patch, "PyQt5._cx_freeze_add_library")

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyqt5", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_qt_debug")

    # Inject code to init
    code_string = module.file.read_text()
    code_string += """
# cx_Freeze patch start
import PyQt5._cx_freeze_add_library
import PyQt5._cx_freeze_qt_debug
# cx_Freeze patch end
"""
    module.code = compile(code_string, os.fspath(module.file), "exec")


# pylint: disable-next=unused-argument
def load_pyqt5_qtcore(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module."""
    try:
        finder.include_module("PyQt5.sip")  # PyQt5 >= 5.11
    except ImportError:
        finder.include_module("sip")
    try:
        finder.include_module("PyQt5._qt")
    except ImportError:
        pass


__all__ = [
    "load_pyqt5",
    "load_pyqt5_qt",
    "load_pyqt5_qtcharts",
    "load_pyqt5_qtcore",
    "load_pyqt5_qtdatavisualization",
    "load_pyqt5_qtdesigner",
    "load_pyqt5_qtgui",
    "load_pyqt5_qthelp",
    "load_pyqt5_qtlocation",
    "load_pyqt5_qtmultimedia",
    "load_pyqt5_qtmultimediawidgets",
    "load_pyqt5_qtopengl",
    "load_pyqt5_qtpositioning",
    "load_pyqt5_qtprintsupport",
    "load_pyqt5_qtqml",
    "load_pyqt5_qtscripttools",
    "load_pyqt5_qtsql",
    "load_pyqt5_qtsvg",
    "load_pyqt5_qttest",
    "load_pyqt5_qtuitools",
    "load_pyqt5_qtwebengine",
    "load_pyqt5_qtwebenginecore",
    "load_pyqt5_qtwebenginewidgets",
    "load_pyqt5_qtwebkit",
    "load_pyqt5_qtwebsockets",
    "load_pyqt5_qtwidgets",
    "load_pyqt5_qtxmlpatterns",
    "load_pyqt5_uic",
]
