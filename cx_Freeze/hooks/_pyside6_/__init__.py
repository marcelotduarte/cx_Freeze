"""Hooks triggered by finder when PySide6 package is included."""

from __future__ import annotations

from importlib import resources
from importlib.machinery import SourceFileLoader
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW
from cx_Freeze.hooks.qthooks import QtHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(QtHook):
    """The Hook class for PySide6."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        self.name = "qt"

    def qt(self, finder: ModuleFinder, module: Module) -> None:
        """Inject code in PySide6 to locate and load plugins and resources."""
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
        package = resources.files(__package__ or "cx_Freeze.hooks._pyside6_")
        finder.include_file_as_module(
            str(package / "_debug.py"), "PySide6._cx_freeze_debug"
        )

        # Include a resource for conda-forge
        if environment == "conda":
            # The resource include a qt.conf (Prefix = lib/PySide6)
            finder.include_file_as_module(
                str(package / "_resource.py"), "PySide6._cx_freeze_resource"
            )

        if IS_MINGW:
            # Include a qt.conf in the module path (Prefix = lib/PySide6)
            finder.include_files(str(package / "qt.conf"), "qt.conf")

        # Inject code to init
        patch = f"""
            # cx_Freeze patch start
            if {environment == "conda"}:
                import PySide6._cx_freeze_resource
            else:
                # Support for QtWebEngine
                import os, sys
                if {IS_MACOS}:
                    # is a bdist_mac ou build_exe directory?
                    helpers = os.path.join(
                        os.path.dirname(sys.prefix), "Helpers"
                    )
                    if not os.path.isdir(helpers):
                        helpers = os.path.join(sys.prefix, "share")
                    os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                        helpers,
                        "QtWebEngineProcess.app",
                        "Contents/MacOS/QtWebEngineProcess"
                    )
                    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
                        "--single-process"
                    )
            import PySide6._cx_freeze_debug
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

        # small tweaks for shiboken6
        if module.in_file_system == 2:
            shiboken6 = finder.include_package("shiboken6")
            if shiboken6:
                shiboken6.in_file_system = 2
        finder.include_module("inspect")
