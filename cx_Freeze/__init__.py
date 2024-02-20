"""Create standalone executables from Python scripts, with the same performance
and is cross-platform.
"""

from __future__ import annotations

import sys

import setuptools

from cx_Freeze.command.build_exe import BuildEXE as build_exe
from cx_Freeze.command.install import Install as install
from cx_Freeze.command.install_exe import InstallEXE as install_exe
from cx_Freeze.executable import Executable, validate_executables
from cx_Freeze.finder import Module, ModuleFinder
from cx_Freeze.freezer import ConstantsModule, Freezer

__all__ = [
    "build_exe",
    "install",
    "install_exe",
    "setup",
    "ConstantsModule",
    "Executable",
    "Freezer",
    "Module",
    "ModuleFinder",
    "__version__",
]

if sys.platform == "win32":
    from cx_Freeze.command.bdist_msi import BdistMSI as bdist_msi

    __all__.append(bdist_msi.__name__)
elif sys.platform == "darwin":
    from cx_Freeze.command.bdist_mac import BdistDMG as bdist_dmg
    from cx_Freeze.command.bdist_mac import BdistMac as bdist_mac

    __all__.extend([bdist_dmg.__name__, bdist_mac.__name__])
else:
    from cx_Freeze.command.bdist_appimage import (
        BdistAppImage as bdist_appimage,
    )
    from cx_Freeze.command.bdist_deb import BdistDEB as bdist_deb
    from cx_Freeze.command.bdist_rpm import BdistRPM as bdist_rpm

    __all__.extend(
        [bdist_appimage.__name__, bdist_deb.__name__, bdist_rpm.__name__]
    )

__version__ = "6.16.0-dev12"


def setup(**attrs) -> setuptools.Distribution:  # noqa: D103
    cmdclass = attrs.setdefault("cmdclass", {})
    if sys.platform == "win32":
        cmdclass.setdefault("bdist_msi", bdist_msi)
    elif sys.platform == "darwin":
        cmdclass.setdefault("bdist_dmg", bdist_dmg)
        cmdclass.setdefault("bdist_mac", bdist_mac)
    else:
        cmdclass.setdefault("bdist_appimage", bdist_appimage)
        cmdclass.setdefault("bdist_deb", bdist_deb)
        cmdclass.setdefault("bdist_rpm", bdist_rpm)
    cmdclass.setdefault("build_exe", build_exe)
    cmdclass.setdefault("install", install)
    cmdclass.setdefault("install_exe", install_exe)
    attrs.setdefault("executables", [])
    return setuptools.setup(**attrs)


setup.__doc__ = setuptools.setup.__doc__


def plugin_install(dist: setuptools.Distribution) -> None:
    """Use a setuptools extension to customize Distribution options."""
    if getattr(dist, "executables", None) is None:
        return
    validate_executables(dist, "executables", dist.executables)

    # Disable package discovery (setuptools >= 61) and/or misuse of packages
    dist.py_modules = []
    dist.packages = []

    # Add/update commands (provisional)
    cmdclass = dist.cmdclass
    cmdclass.setdefault("build_exe", build_exe)
    cmdclass.setdefault("install", install)
    cmdclass.setdefault("install_exe", install_exe)

    # Add build_exe as subcommand of setuptools build (plugin)
    build = dist.get_command_obj("build")
    build.user_options.insert(
        1,
        (
            "build-exe=",
            None,
            "directory for built executables and dependent files [DEPRECATED]",
        ),
    )
    build.sub_commands = [*build.sub_commands, ("build_exe", None)]
    build.build_exe = None
