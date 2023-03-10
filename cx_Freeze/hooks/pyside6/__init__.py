"""A collection of functions which are triggered automatically by finder when
PySide6 package is included."""

from __future__ import annotations

import os

from ..._compat import IS_MINGW
from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import load_qt_qaxcontainer as load_pyside6_qaxcontainer
from .._qthooks import load_qt_qt as load_pyside6_qt
from .._qthooks import load_qt_qtcharts as load_pyside6_qtcharts
from .._qthooks import (
    load_qt_qtdatavisualization as load_pyside6_qtdatavisualization,
)
from .._qthooks import load_qt_qtdesigner as load_pyside6_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyside6_qtgui
from .._qthooks import load_qt_qthelp as load_pyside6_qthelp
from .._qthooks import load_qt_qtlocation as load_pyside6_qtlocation
from .._qthooks import load_qt_qtmultimedia as load_pyside6_qtmultimedia
from .._qthooks import (
    load_qt_qtmultimediawidgets as load_pyside6_qtmultimediawidgets,
)
from .._qthooks import load_qt_qtnetwork as load_pyside6_qtnetwork
from .._qthooks import load_qt_qtopengl as load_pyside6_qtopengl
from .._qthooks import load_qt_qtopenglwidgets as load_pyside6_qtopenglwidgets
from .._qthooks import load_qt_qtpositioning as load_pyside6_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyside6_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyside6_qtqml
from .._qthooks import load_qt_qtquick as load_pyside6_qtquick
from .._qthooks import load_qt_qtquickwidgets as load_pyside6_qtquickwidgets
from .._qthooks import load_qt_qtscripttools as load_pyside6_qtscripttools
from .._qthooks import load_qt_qtsql as load_pyside6_qtsql
from .._qthooks import load_qt_qtsvg as load_pyside6_qtsvg
from .._qthooks import load_qt_qtsvgwidgets as load_pyside6_qtsvgwidgets
from .._qthooks import load_qt_qttest as load_pyside6_qttest
from .._qthooks import load_qt_qtuitools as load_pyside6_qtuitools
from .._qthooks import load_qt_qtwebengine as load_pyside6_qtwebengine
from .._qthooks import load_qt_qtwebenginecore as load_pyside6_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyside6_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwebsockets as load_pyside6_qtwebsockets
from .._qthooks import load_qt_qtwidgets as load_pyside6_qtwidgets


def load_pyside6(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PySide6 __init__ to locate and load plugins and
    resources."""

    # Include QtCore module needed by all modules
    finder.include_module("PySide6.QtCore")

    # Activate an optimized mode when PySide6 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyside6", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PySide6._cx_freeze_qt_debug")

    # Include a copy of qt.conf (works for pyside6 6.4.0 mingw)
    if IS_MINGW:
        qt_conf = get_resource_file_path("hooks/pyside6", "qt", ".conf")
        if qt_conf:
            finder.include_files(qt_conf, "qt.conf")

    # Inject code to init
    code_string = module.file.read_text()
    code_string += """
# cx_Freeze patch start
import PySide6._cx_freeze_qt_debug
# cx_Freeze patch end
"""
    module.code = compile(code_string, os.fspath(module.file), "exec")


__all__ = [
    "load_pyside6",
    "load_pyside6_qt",
    "load_pyside6_qaxcontainer",
    "load_pyside6_qtcharts",
    "load_pyside6_qtdatavisualization",
    "load_pyside6_qtdesigner",
    "load_pyside6_qtgui",
    "load_pyside6_qthelp",
    "load_pyside6_qtlocation",
    "load_pyside6_qtmultimedia",
    "load_pyside6_qtmultimediawidgets",
    "load_pyside6_qtnetwork",
    "load_pyside6_qtopengl",
    "load_pyside6_qtopenglwidgets",
    "load_pyside6_qtpositioning",
    "load_pyside6_qtprintsupport",
    "load_pyside6_qtquick",
    "load_pyside6_qtquickwidgets",
    "load_pyside6_qtqml",
    "load_pyside6_qtscripttools",
    "load_pyside6_qtsql",
    "load_pyside6_qtsvg",
    "load_pyside6_qtsvgwidgets",
    "load_pyside6_qttest",
    "load_pyside6_qtuitools",
    "load_pyside6_qtwebengine",
    "load_pyside6_qtwebenginecore",
    "load_pyside6_qtwebenginewidgets",
    "load_pyside6_qtwebsockets",
    "load_pyside6_qtwidgets",
]
