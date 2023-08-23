"""A collection of functions which are triggered automatically by finder when
PySide6 package is included.
"""
from __future__ import annotations

import os
from textwrap import dedent

from ..._compat import IS_CONDA, IS_MINGW
from ...common import code_object_replace_function, get_resource_file_path
from ...finder import ModuleFinder
from ...module import Module
from .._qthooks import load_qt_qtdesigner as load_pyside6_qtdesigner
from .._qthooks import load_qt_qtgui as load_pyside6_qtgui
from .._qthooks import load_qt_qtmultimedia as load_pyside6_qtmultimedia
from .._qthooks import load_qt_qtnetwork as load_pyside6_qtnetwork
from .._qthooks import load_qt_qtopengl as load_pyside6_qtopengl
from .._qthooks import load_qt_qtopenglwidgets as load_pyside6_qtopenglwidgets
from .._qthooks import load_qt_qtpositioning as load_pyside6_qtpositioning
from .._qthooks import load_qt_qtprintsupport as load_pyside6_qtprintsupport
from .._qthooks import load_qt_qtqml as load_pyside6_qtqml
from .._qthooks import load_qt_qtquick as load_pyside6_qtquick
from .._qthooks import load_qt_qtsql as load_pyside6_qtsql
from .._qthooks import load_qt_qtsvg as load_pyside6_qtsvg
from .._qthooks import load_qt_qtwebenginecore as load_pyside6_qtwebenginecore
from .._qthooks import (
    load_qt_qtwebenginewidgets as load_pyside6_qtwebenginewidgets,
)
from .._qthooks import load_qt_qtwidgets as load_pyside6_qtwidgets


def load_pyside6(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PySide6 __init__ to locate and load plugins and
    resources.
    """
    # Activate an optimized mode when PySide6 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyside6", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PySide6._cx_freeze_qt_debug")

    # Include a resource for conda-forge
    if IS_CONDA:
        # The resource include a qt.conf (Prefix = lib/PySide6)
        resource = get_resource_file_path("hooks/pyside6", "resource", ".py")
        finder.include_file_as_module(resource, "PySide6._cx_freeze_resource")

    if IS_MINGW:
        # Include a qt.conf in the module path (Prefix = lib/PySide6)
        qt_conf = get_resource_file_path("hooks/pyside6", "qt", ".conf")
        finder.include_files(qt_conf, qt_conf.name)

    # Inject code to init
    code_string = module.file.read_text(encoding="utf_8")
    code_string += dedent(
        f"""
        # cx_Freeze patch start
        if {IS_CONDA}:
            import PySide6._cx_freeze_resource
        import PySide6._cx_freeze_qt_debug
        # cx_Freeze patch end
        """
    )
    code = compile(code_string, os.fspath(module.file), "exec")

    # shiboken6 in zip_include_packages
    shiboken6 = finder.include_package("shiboken6")
    if shiboken6.in_file_system == 0:
        name = "_additional_dll_directories"
        source = f"""\
        def {name}(package_dir):
            return []
        """
        code = code_object_replace_function(code, name, source)
    finder.include_module("inspect")  # for shiboken6

    module.code = code


__all__ = [
    "load_pyside6",
    "load_pyside6_qtdesigner",
    "load_pyside6_qtgui",
    "load_pyside6_qtmultimedia",
    "load_pyside6_qtnetwork",
    "load_pyside6_qtopengl",
    "load_pyside6_qtopenglwidgets",
    "load_pyside6_qtpositioning",
    "load_pyside6_qtprintsupport",
    "load_pyside6_qtquick",
    "load_pyside6_qtqml",
    "load_pyside6_qtsql",
    "load_pyside6_qtsvg",
    "load_pyside6_qtwebenginecore",
    "load_pyside6_qtwebenginewidgets",
    "load_pyside6_qtwidgets",
]
