"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included.
"""
from __future__ import annotations

import os
from contextlib import suppress
from textwrap import dedent

from ..._compat import IS_CONDA
from ...common import get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import copy_qt_files
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
    resources. Also, this fixes issues with conda-forge versions.
    """
    # Include QtCore module needed by all modules
    finder.include_module("PyQt5.QtCore")

    # Activate an optimized mode when PyQt5 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include a module that fix an issue and inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyqt5", "_append_to_init", ".py")
    finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_append_to_init")

    # Include a resource with qt.conf (Prefix = lib/PyQt5) for conda-forge
    if IS_CONDA:
        resource = get_resource_file_path("hooks/pyqt5", "resource", ".py")
        finder.include_file_as_module(resource, "PyQt5._cx_freeze_resource")

    # Include the optional qt.conf used by QtWebEngine (Prefix = ..)
    copy_qt_files(finder, "PyQt5", "LibraryExecutablesPath", "qt.conf")

    # Inject code to the end of init
    code_string = module.file.read_text(encoding="utf_8")
    code_string += dedent(
        f"""
        # cx_Freeze patch start
        if {IS_CONDA}:
            import PyQt5._cx_freeze_resource
        else:
            # Support for QtWebEngine
            import os
            os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
        import PyQt5._cx_freeze_append_to_init
        # cx_Freeze patch end
        """
    )
    module.code = compile(code_string, os.fspath(module.file), "exec")


def load_pyqt5_qtcore(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module.
    """
    try:
        finder.include_module("PyQt5.sip")  # PyQt5 >= 5.11
    except ImportError:
        finder.include_module("sip")
    with suppress(ImportError):
        finder.include_module("PyQt5._qt")


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
