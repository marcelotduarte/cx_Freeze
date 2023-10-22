"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included.
"""
from __future__ import annotations

from textwrap import dedent

from cx_Freeze._compat import IS_CONDA
from cx_Freeze.common import get_resource_file_path
from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module

from .._qthooks import copy_qt_files
from .._qthooks import load_qt_qtdesigner as load_pyqt5_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyqt5_qtgui
from .._qthooks import load_qt_qtmultimedia as load_pyqt5_qtmultimedia
from .._qthooks import load_qt_qtnetwork as load_pyqt5_qtnetwork
from .._qthooks import load_qt_qtopengl as load_pyqt5_qtopengl
from .._qthooks import load_qt_qtpositioning as load_pyqt5_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyqt5_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyqt5_qtqml
from .._qthooks import load_qt_qtsql as load_pyqt5_qtsql
from .._qthooks import load_qt_qtsvg as load_pyqt5_qtsvg
from .._qthooks import load_qt_qtwebenginecore as load_pyqt5_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyqt5_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwidgets as load_pyqt5_qtwidgets
from .._qthooks import load_qt_uic as load_pyqt5_uic


def load_pyqt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5 __init__ to locate and load plugins and
    resources. Also, this fixes issues with conda-forge versions.
    """
    # Activate an optimized mode when PyQt5 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include a module that fix an issue
    qt_debug = get_resource_file_path("hooks/pyqt5", "_append_to_init", ".py")
    finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_append_to_init")

    # Include a module that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyqt5", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_debug")

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
        import PyQt5._cx_freeze_debug
        # cx_Freeze patch end
        """
    )
    module.code = compile(code_string, module.file.as_posix(), "exec")


__all__ = [
    "load_pyqt5",
    "load_pyqt5_qtdesigner",
    "load_pyqt5_qtgui",
    "load_pyqt5_qtmultimedia",
    "load_pyqt5_qtnetwork",
    "load_pyqt5_qtopengl",
    "load_pyqt5_qtpositioning",
    "load_pyqt5_qtprintsupport",
    "load_pyqt5_qtqml",
    "load_pyqt5_qtsql",
    "load_pyqt5_qtsvg",
    "load_pyqt5_qtwebenginecore",
    "load_pyqt5_qtwebenginewidgets",
    "load_pyqt5_qtwidgets",
    "load_pyqt5_uic",
]
