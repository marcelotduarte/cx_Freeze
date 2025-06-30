"""A collection of functions which are triggered automatically by finder when
PyQt5 package is included.
"""

from __future__ import annotations

import importlib.resources as importlib_resources
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.qthooks import QtHook, copy_qt_files

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(QtHook):
    """The Hook class for PyQt5."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        self.name = "qt"

    def qt(self, finder: ModuleFinder, module: Module) -> None:
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
        qt_debug = importlib_resources.files(__package__) / "_debug.py"
        finder.include_file_as_module(qt_debug, "PyQt5._cx_freeze_debug")

        # Include a resource with qt.conf (Prefix = lib/PyQt5) for conda-forge
        if environment == "conda":
            resource = importlib_resources.files(__package__) / "_resource.py"
            finder.include_file_as_module(
                resource, "PyQt5._cx_freeze_resource"
            )

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

            prefix = sys.prefix
            qt_root_dir = os.path.join(prefix, "lib", "PyQt5")
            try:
                from PyQt5 import QtCore
            except ImportError:
                if {IS_MINGW or IS_WINDOWS}:
                    bin_dir = os.path.join(qt_root_dir, "Qt5", "bin")
                    if os.path.isdir(bin_dir):
                        os.add_dll_directory(bin_dir)
                        from PyQt5 import QtCore
            if {environment == "conda"}:  # conda-forge linux, macos, windows
                import PyQt5._cx_freeze_resource
            elif {IS_MACOS}:  # macos using 'pip install pyqt5'
                # Support for QtWebEngine (bdist_mac differs from build_exe)
                helpers = os.path.join(os.path.dirname(prefix), "Helpers")
                if not os.path.isdir(helpers):
                    helpers = os.path.join(prefix, "share")
                os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                    helpers,
                    "QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"
                )
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--single-process"
            else:
                # Support for QtWebEngine (linux and windows using pip)
                os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
            # With PyQt5 5.15.4, if the folder name contains non-ascii
            # characters, the libraryPaths returns empty.
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

    def qt_qtwebenginecore(self, finder: ModuleFinder, module: Module) -> None:
        """Include module dependency and QtWebEngineProcess files."""
        super().qt_qtwebenginecore(finder, module)
        distribution = module.parent.distribution
        environment = (distribution and distribution.installer) or "pip"
        if IS_MACOS and environment == "pip":
            # duplicate resource files
            for source, target in finder.included_files[:]:
                if any(
                    filter(
                        source.match, ("Resources/*.pak", "Resources/*.dat")
                    )
                ):
                    finder.include_files(
                        source,
                        target.parent.parent / target.name,
                        copy_dependent_files=False,
                    )
