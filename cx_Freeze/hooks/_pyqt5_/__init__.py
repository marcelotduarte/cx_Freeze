"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included.
"""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.common import get_resource_file_path
from cx_Freeze.hooks.qthooks import copy_qt_files
from cx_Freeze.hooks.qthooks import load_qt_qtcore as load_pyqt5_qtcore
from cx_Freeze.hooks.qthooks import load_qt_qtdesigner as load_pyqt5_qtdesigner
from cx_Freeze.hooks.qthooks import load_qt_qtgui as load_pyqt5_qtgui
from cx_Freeze.hooks.qthooks import (
    load_qt_qtmultimedia as load_pyqt5_qtmultimedia,
)
from cx_Freeze.hooks.qthooks import load_qt_qtnetwork as load_pyqt5_qtnetwork
from cx_Freeze.hooks.qthooks import (
    load_qt_qtpositioning as load_pyqt5_qtpositioning,
)
from cx_Freeze.hooks.qthooks import (
    load_qt_qtprintsupport as load_pyqt5_qtprintsupport,
)
from cx_Freeze.hooks.qthooks import load_qt_qtqml as load_pyqt5_qtqml
from cx_Freeze.hooks.qthooks import load_qt_qtsql as load_pyqt5_qtsql
from cx_Freeze.hooks.qthooks import (
    load_qt_qtwebenginecore as _load_qt_qtwebenginecore,
)
from cx_Freeze.hooks.qthooks import (
    load_qt_qtwebenginewidgets as load_pyqt5_qtwebenginewidgets,
)
from cx_Freeze.hooks.qthooks import load_qt_qtwidgets as load_pyqt5_qtwidgets
from cx_Freeze.hooks.qthooks import load_qt_uic as load_pyqt5_uic

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pyqt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5 __init__ to locate and load plugins and
    resources. Also, this fixes issues with conda-forge versions.
    """
    distribution = module.distribution
    environment = (distribution and distribution.installer) or "pip"
    # Activate the optimized mode by default in pip environments
    if environment == "pip":
        if module.name in finder.zip_exclude_packages:
            print(f"WARNING: zip_exclude_packages={module.name} ignored.")
        if module.name in finder.zip_include_packages:
            print(f"WARNING: zip_include_packages={module.name} ignored.")
        module.in_file_system = 2

    # Include a module that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/_pyqt5_", "_debug", ".py")
    finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_debug")

    # Include a resource with qt.conf (Prefix = lib/PyQt5) for conda-forge
    if environment == "conda":
        resource = get_resource_file_path("hooks/_pyqt5_", "_resource", ".py")
        finder.include_file_as_module(resource, "PyQt5._cx_freeze_resource")

    # Include an optional qt.conf to be used by QtWebEngine (Prefix = ..)
    copy_qt_files(finder, "PyQt5", "LibraryExecutablesPath", "qt.conf")

    # Inject code to the end of init
    if environment == "conda":
        code_string = ""
    else:
        code_string = module.file.read_text(encoding="utf_8")
    code_string += dedent(
        f"""
        # cx_Freeze patch start
        import os, sys

        frozen_dir = sys.frozen_dir
        qt_root_dir = os.path.join(frozen_dir, "lib", "PyQt5")
        try:
            from PyQt5 import QtCore
        except ImportError:
            if {IS_MINGW or IS_WINDOWS}:
                bin_dir = os.path.join(qt_root_dir, "Qt5", "bin")
                if os.path.isdir(bin_dir):
                    os.add_dll_directory(bin_dir)
                    from PyQt5 import QtCore
        if {environment == "conda"}:  # conda-forge linux, macos and windows
            import PyQt5._cx_freeze_resource
        elif {IS_MACOS}:  # macos using 'pip install pyqt5'
            # Support for QtWebEngine (bdist_mac differs from build_exe)
            helpers = os.path.join(os.path.dirname(frozen_dir), "Helpers")
            if not os.path.isdir(helpers):
                helpers = os.path.join(frozen_dir, "share")
            os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                helpers,
                "QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"
            )
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--single-process"
        else:
            # Support for QtWebEngine (linux and windows using pip)
            os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
        # With PyQt5 5.15.4, if the folder name contains non-ascii characters,
        # the libraryPaths returns empty.
        # Prior to this version, this doesn't happen.
        plugins_dir = os.path.join(qt_root_dir, "Qt5", "plugins")  # 5.15.4
        if not os.path.isdir(plugins_dir):
            plugins_dir = os.path.join(qt_root_dir, "Qt", "plugins")
        if not os.path.isdir(plugins_dir):
            plugins_dir = os.path.join(qt_root_dir, "plugins")
        if os.path.isdir(plugins_dir):
            QtCore.QCoreApplication.addLibraryPath(
                plugins_dir.replace(os.path.sep, os.path.altsep or "/")
            )
        import PyQt5._cx_freeze_debug
        # cx_Freeze patch end
        """
    )
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def load_pyqt5_qtwebenginecore(finder: ModuleFinder, module: Module) -> None:
    """Include module dependency and QtWebEngineProcess files."""
    _load_qt_qtwebenginecore(finder, module)
    distribution = module.parent.distribution
    environment = (distribution and distribution.installer) or "pip"
    if IS_MACOS and environment == "pip":
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
    "load_pyqt5",
    "load_pyqt5_qtcore",
    "load_pyqt5_qtdesigner",
    "load_pyqt5_qtgui",
    "load_pyqt5_qtmultimedia",
    "load_pyqt5_qtnetwork",
    "load_pyqt5_qtpositioning",
    "load_pyqt5_qtprintsupport",
    "load_pyqt5_qtqml",
    "load_pyqt5_qtsql",
    "load_pyqt5_qtwebenginecore",
    "load_pyqt5_qtwebenginewidgets",
    "load_pyqt5_qtwidgets",
    "load_pyqt5_uic",
]
