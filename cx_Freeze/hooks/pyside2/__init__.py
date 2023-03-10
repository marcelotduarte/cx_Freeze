"""A collection of functions which are triggered automatically by finder when
PySide2 package is included."""

from __future__ import annotations

import os

from ..._compat import IS_CONDA, IS_WINDOWS
from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import load_qt_qt as load_pyside2_qt
from .._qthooks import load_qt_qtcharts as load_pyside2_qtcharts
from .._qthooks import (
    load_qt_qtdatavisualization as load_pyside2_qtdatavisualization,
)
from .._qthooks import load_qt_qtdesigner as load_pyside2_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyside2_qtgui
from .._qthooks import load_qt_qthelp as load_pyside2_qthelp
from .._qthooks import load_qt_qtlocation as load_pyside2_qtlocation
from .._qthooks import load_qt_qtmultimedia as load_pyside2_qtmultimedia
from .._qthooks import (
    load_qt_qtmultimediawidgets as load_pyside2_qtmultimediawidgets,
)
from .._qthooks import load_qt_qtopengl as load_pyside2_qtopengl
from .._qthooks import load_qt_qtpositioning as load_pyside2_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyside2_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyside2_qtqml
from .._qthooks import load_qt_qtscripttools as load_pyside2_qtscripttools
from .._qthooks import load_qt_qtsql as load_pyside2_qtsql
from .._qthooks import load_qt_qtsvg as load_pyside2_qtsvg
from .._qthooks import load_qt_qttest as load_pyside2_qttest
from .._qthooks import load_qt_qtuitools as load_pyside2_qtuitools
from .._qthooks import load_qt_qtwebengine as load_pyside2_qtwebengine
from .._qthooks import load_qt_qtwebenginecore as load_pyside2_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyside2_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwebkit as load_pyside2_qtwebkit
from .._qthooks import load_qt_qtwebsockets as load_pyside2_qtwebsockets
from .._qthooks import load_qt_qtwidgets as load_pyside2_qtwidgets
from .._qthooks import load_qt_qtxmlpatterns as load_pyside2_qtxmlpatterns
from .._qthooks import load_qt_uic as load_pyside2_uic


def load_pyside2(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PySide2 __init__ to locate and load plugins and
    resources. Also, this fixes issues with conda-forge versions."""

    # Include QtCore module needed by all modules
    finder.include_module("PySide2.QtCore")

    # Activate an optimized mode when PySide2 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyside2", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PySide2._cx_freeze_qt_debug")

    # Include a resource with qt.conf for conda-forge windows/linux
    if IS_CONDA:
        resource = get_resource_file_path("hooks/pyside2", "resource", ".py")
        finder.include_file_as_module(resource, "PySide2._cx_freeze_resource")

    # Include a copy of qt.conf (works for pyside2 wheels on windows)
    if IS_WINDOWS:
        qt_conf = get_resource_file_path("hooks/pyside2", "qt", ".conf")
        if qt_conf:
            finder.include_files(qt_conf, "qt.conf")

    # Inject code to init
    code_string = module.file.read_text()
    code_string += """
# cx_Freeze patch start
try:
    import PySide2._cx_freeze_resource
except ImportError:
    pass
import PySide2._cx_freeze_qt_debug
# cx_Freeze patch end
"""
    module.code = compile(code_string, os.fspath(module.file), "exec")


__all__ = [
    "load_pyside2",
    "load_pyside2_qt",
    "load_pyside2_qtcharts",
    "load_pyside2_qtdatavisualization",
    "load_pyside2_qtdesigner",
    "load_pyside2_qtgui",
    "load_pyside2_qthelp",
    "load_pyside2_qtlocation",
    "load_pyside2_qtmultimedia",
    "load_pyside2_qtmultimediawidgets",
    "load_pyside2_qtopengl",
    "load_pyside2_qtpositioning",
    "load_pyside2_qtprintsupport",
    "load_pyside2_qtqml",
    "load_pyside2_qtscripttools",
    "load_pyside2_qtsql",
    "load_pyside2_qtsvg",
    "load_pyside2_qttest",
    "load_pyside2_qtuitools",
    "load_pyside2_qtwebengine",
    "load_pyside2_qtwebenginecore",
    "load_pyside2_qtwebenginewidgets",
    "load_pyside2_qtwebkit",
    "load_pyside2_qtwebsockets",
    "load_pyside2_qtwidgets",
    "load_pyside2_qtxmlpatterns",
    "load_pyside2_uic",
]
