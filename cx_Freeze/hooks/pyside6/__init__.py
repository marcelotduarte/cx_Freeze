"""A collection of functions which are triggered automatically by finder when
PySide6 package is included.
"""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW
from cx_Freeze.common import (
    code_object_replace_function,
    get_resource_file_path,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qt3dinput as load_pyside6_qt3dinput,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qt3drender as load_pyside6_qt3drender,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtbluetooth as load_pyside6_qtbluetooth,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtdesigner as load_pyside6_qtdesigner,
)
from cx_Freeze.hooks._qthooks import load_qt_qtgui as load_pyside6_qtgui
from cx_Freeze.hooks._qthooks import (
    load_qt_qtlocation as load_pyside6_qtlocation,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtmultimedia as load_pyside6_qtmultimedia,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtnetwork as load_pyside6_qtnetwork,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtpositioning as load_pyside6_qtpositioning,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtprintsupport as load_pyside6_qtprintsupport,
)
from cx_Freeze.hooks._qthooks import load_qt_qtqml as load_pyside6_qtqml
from cx_Freeze.hooks._qthooks import load_qt_qtquick as load_pyside6_qtquick
from cx_Freeze.hooks._qthooks import (
    load_qt_qtquick3d as load_pyside6_qtquick3d,
)
from cx_Freeze.hooks._qthooks import load_qt_qtscxml as load_pyside6_qtscxml
from cx_Freeze.hooks._qthooks import (
    load_qt_qtserialbus as load_pyside6_qtserialbus,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtserialport as load_pyside6_qtserialport,
)
from cx_Freeze.hooks._qthooks import load_qt_qtsql as load_pyside6_qtsql
from cx_Freeze.hooks._qthooks import (
    load_qt_qttexttospeech as load_pyside6_qttexttospeech,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtvirtualkeyboard as load_pyside6_qtvirtualkeyboard,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtwebenginecore as load_pyside6_qtwebenginecore,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtwebenginewidgets as load_pyside6_qtwebenginewidgets,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtwebsockets as load_pyside6_qtwebsockets,
)
from cx_Freeze.hooks._qthooks import (
    load_qt_qtwidgets as load_pyside6_qtwidgets,
)

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pyside6(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PySide6 __init__ to locate and load plugins and
    resources.
    """
    # Activate the optimized mode by default in pip environments
    if module.name in finder.zip_exclude_packages:
        print(f"WARNING: zip_exclude_packages={module.name} ignored.")
    if module.name in finder.zip_include_packages:
        print(f"WARNING: zip_include_packages={module.name} ignored.")
    distribution = module.distribution
    environment = (distribution and distribution.installer) or "pip"
    if environment == "pip":
        module.in_file_system = 2
    else:
        module.in_file_system = 1

    # Include modules that inject an optional debug code
    qt_debug = get_resource_file_path("hooks/pyside6", "debug", ".py")
    finder.include_file_as_module(qt_debug, "PySide6._cx_freeze_qt_debug")

    # Include a resource for conda-forge
    if environment == "conda":
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
        if {environment == "conda"}:
            import PySide6._cx_freeze_resource
        else:
            # Support for QtWebEngine
            import os, sys
            if {IS_MACOS}:
                # is a bdist_mac ou build_exe directory?
                helpers = os.path.join(
                    os.path.dirname(sys.frozen_dir), "Helpers"
                )
                if not os.path.isdir(helpers):
                    helpers = os.path.join(sys.frozen_dir, "share")
                os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.join(
                    helpers,
                    "QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"
                )
                os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--single-process"
        import PySide6._cx_freeze_qt_debug
        # cx_Freeze patch end
        """
    )
    code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )

    # shiboken6 in zip_include_packages
    shiboken6 = finder.include_package("shiboken6")
    if module.in_file_system == 2:
        shiboken6.in_file_system = 0
    if shiboken6.in_file_system == 0:
        name = "_additional_dll_directories"
        source = f"""\
        def {name}(package_dir):
            return []
        """
        code = code_object_replace_function(code, name, source)
    module.code = code

    # extra modules
    finder.include_module("inspect")  # for shiboken6


__all__ = [
    "load_pyside6",
    "load_pyside6_qt3dinput",
    "load_pyside6_qt3drender",
    "load_pyside6_qtbluetooth",
    "load_pyside6_qtdesigner",
    "load_pyside6_qtgui",
    "load_pyside6_qtlocation",
    "load_pyside6_qtmultimedia",
    "load_pyside6_qtnetwork",
    "load_pyside6_qtpositioning",
    "load_pyside6_qtprintsupport",
    "load_pyside6_qtquick",
    "load_pyside6_qtquick3d",
    "load_pyside6_qtscxml",
    "load_pyside6_qtserialbus",
    "load_pyside6_qtserialport",
    "load_pyside6_qtqml",
    "load_pyside6_qtsql",
    "load_pyside6_qttexttospeech",
    "load_pyside6_qtvirtualkeyboard",
    "load_pyside6_qtwebenginecore",
    "load_pyside6_qtwebenginewidgets",
    "load_pyside6_qtwebsockets",
    "load_pyside6_qtwidgets",
]
