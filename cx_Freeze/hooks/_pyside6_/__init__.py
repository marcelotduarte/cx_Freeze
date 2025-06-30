"""A collection of functions which are triggered automatically by finder when
PySide6 package is included.
"""

from __future__ import annotations

import importlib.resources as importlib_resources
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
        """Inject code in PySide6 __init__ to locate and load plugins and
        resources.
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

        # Include modules that inject an optional debug code
        qt_debug = importlib_resources.files(__package__) / "_debug.py"
        finder.include_file_as_module(qt_debug, "PySide6._cx_freeze_qt_debug")

        # Include a resource for conda-forge
        if environment == "conda":
            # The resource include a qt.conf (Prefix = lib/PySide6)
            resource = importlib_resources.files(__package__) / "_resource.py"
            finder.include_file_as_module(
                resource, "PySide6._cx_freeze_resource"
            )

        if IS_MINGW:
            # Include a qt.conf in the module path (Prefix = lib/PySide6)
            qt_conf = importlib_resources.files(__package__) / "qt.conf"
            finder.include_files(qt_conf, qt_conf.name)

        # Inject code to init
        code_string = module.file.read_text(encoding="utf_8")
        code_string += dedent(
            f"""
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
            import PySide6._cx_freeze_qt_debug
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

        # small tweaks for shiboken6
        if module.in_file_system == 2:
            shiboken6 = finder.include_package("shiboken6")
            shiboken6.in_file_system = 2
        finder.include_module("inspect")
