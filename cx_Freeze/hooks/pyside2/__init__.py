"""A collection of functions which are triggered automatically by finder when
PySide2 package is included.
"""
from __future__ import annotations

from textwrap import dedent

from cx_Freeze._compat import IS_CONDA, IS_MACOS, IS_MINGW
from cx_Freeze.common import (
    code_object_replace_function,
    get_resource_file_path,
)
from cx_Freeze.finder import ModuleFinder
from cx_Freeze.module import Module

from .._qthooks import copy_qt_files
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
from .._qthooks import load_qt_qtwebenginecore as _load_qt_qtwebenginecore
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
    resources. Also, this fixes issues with conda-forge versions.
    """
    # Include QtCore module needed by all modules
    finder.include_module("PySide2.QtCore")

    # Activate an optimized mode when PySide2 is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2

    # Include a module that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyside2", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PySide2._cx_freeze_debug")

    # Include a resource with qt.conf (Prefix = lib/PySide2) for conda-forge
    if IS_CONDA:
        resource = get_resource_file_path("hooks/pyside2", "resource", ".py")
        finder.include_file_as_module(resource, "PySide2._cx_freeze_resource")

    # Include a qt.conf in the module path (Prefix = lib/PySide2) for msys2
    if IS_MINGW:
        qt_conf = get_resource_file_path("hooks/pyside2", "qt", ".conf")
        finder.include_files(qt_conf, qt_conf.name)

    # Include an optional qt.conf to be used by QtWebEngine (Prefix = ..)
    copy_qt_files(finder, "PySide2", "LibraryExecutablesPath", "qt.conf")

    # Inject code to init
    code_string = module.file.read_text(encoding="utf_8")
    code_string += dedent(
        f"""
        # cx_Freeze patch start
        import os, sys
        if {IS_CONDA}:  # conda-forge linux, macos and windows
            import PySide2._cx_freeze_resource
        elif {IS_MACOS}:  # macos using 'pip install pyside2'
            # Support for QtWebEngine (bdist_mac differs from build_exe)
            helpers = os.path.join(os.path.dirname(sys.frozen_dir), "Helpers")
            if not os.path.isdir(helpers):
                helpers = os.path.join(sys.frozen_dir, "share")
            os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                helpers,
                "QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"
            )
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--single-process"
        else:
            # Support for QtWebEngine (linux and windows using pip)
            os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
        import PySide2._cx_freeze_debug
        # cx_Freeze patch end
        """
    )
    code = compile(code_string, module.file.as_posix(), "exec")

    # shiboken2 in zip_include_packages
    shiboken2 = finder.include_package("shiboken2")
    if shiboken2.in_file_system == 0:
        name = "_additional_dll_directories"
        source = f"""\
        def {name}(package_dir):
            return []
        """
        code = code_object_replace_function(code, name, source)
    finder.include_module("inspect")  # for shiboken2

    module.code = code


def load_pyside2_qtwebenginecore(finder: ModuleFinder, module: Module) -> None:
    """Include module dependency and QtWebEngineProcess files."""
    _load_qt_qtwebenginecore(finder, module)
    if IS_MACOS and not IS_CONDA:
        # duplicate resource files
        for source, target in finder.included_files[:]:
            if any(
                filter(source.match, ("Resources/*.pak", "Resources/*.dat"))
            ):
                finder.include_files(
                    source,
                    target.parent.parent / target.name,
                    copy_dependent_files=False,
                )


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
