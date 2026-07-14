"""Hooks triggered by finder when PyQt6 package is included."""

from __future__ import annotations

import sys
from importlib import resources
from importlib.machinery import SourceFileLoader
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW
from cx_Freeze.hooks.qthooks import QtHook, copy_qt_files

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(QtHook):
    """The Hook class for PyQt6."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        self.name = "qt"

    def qt(self, finder: ModuleFinder, module: Module) -> None:
        """Inject code in PyQt6 to locate and load plugins and resources."""
        distribution = module.distribution
        environment = (distribution and distribution.installer) or "pip"
        # Activate the optimized mode by default in pip environments
        if environment == "pip":
            if module.name in finder.zip_exclude_packages:
                print(f"WARNING: zip_exclude_packages={module.name} ignored.")
            if module.name in finder.zip_include_packages:
                print(f"WARNING: zip_include_packages={module.name} ignored.")
            module.in_file_system = 2

        # Include modules that inject an optional debug code
        package = resources.files(__package__ or "cx_Freeze.hooks._pyqt6_")
        finder.include_file_as_module(
            str(package / "_debug.py"), "PyQt6._cx_freeze_debug"
        )

        # Include a qt.conf in the module path (Prefix = lib/PyQt6/Qt6)
        if IS_MACOS:
            finder.include_files(str(package / "qt_macos.conf"), "qt.conf")
            # bdist_mac (.app) uses a different Prefix in qt.conf
            finder.include_files(
                str(package / "qt_bdist_mac.conf"), "qt_bdist_mac.conf"
            )
        # Include a qt.conf in the module path (Prefix = lib/PyQt6) for msys2
        if IS_MINGW:
            finder.include_files(str(package / "qt_msys2.conf"), "qt.conf")

        # Include a copy of qt.conf (used by QtWebEngine)
        copy_qt_files(finder, "PyQt6", "LibraryExecutablesPath", "qt.conf")

        # Inject code to init
        patch = f"""
            # cx_Freeze patch start
            if {IS_MACOS} and {environment == "pip"}:
                # note: conda doesn't support pyqt6
                import os, sys
                # Support for QtWebEngine (bdist_mac differs from build_exe)
                helpers = os.path.join(os.path.dirname(sys.prefix), "Helpers")
                if not os.path.isdir(helpers):
                    helpers = os.path.join(sys.prefix, "share")
                os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                    helpers,
                    "QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"
                )
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--single-process"
            import PyQt6._cx_freeze_debug
            # cx_Freeze patch end
        """
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code is None:
            return
        module.code = loader.source_to_code(
            source_code + dedent(patch),
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )

    def qt_qtwidgets(self, finder: ModuleFinder, module: Module) -> None:
        """Include module dependency."""
        super().qt_qtwidgets(finder, module)
        if sys.platform == "linux":
            copy_qt_files(
                finder, "PyQt6", "LibrariesPath", "libQt6Widgets.so.6"
            )
