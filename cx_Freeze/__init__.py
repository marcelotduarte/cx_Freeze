"""Create standalone executables from Python scripts, with the same performance
and is cross-platform.
"""
# pylint: disable=invalid-name

from __future__ import annotations

import sys

import setuptools

from .command.build_exe import BuildEXE as build_exe
from .command.install import Install as install
from .command.install_exe import InstallEXE as install_exe
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer

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
    from .command.bdist_msi import BdistMSI as bdist_msi

    __all__.append(bdist_msi.__name__)
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG as bdist_dmg
    from .command.bdist_mac import BdistMac as bdist_mac

    __all__.extend([bdist_dmg.__name__, bdist_mac.__name__])
else:
    from .command.bdist_rpm import BdistRPM as bdist_rpm

    __all__.append(bdist_rpm.__name__)

__version__ = "6.15.7"


def setup(**attrs):  # noqa: D103
    cmdclass = attrs.setdefault("cmdclass", {})
    if sys.platform == "win32":
        cmdclass.setdefault("bdist_msi", bdist_msi)
    elif sys.platform == "darwin":
        cmdclass.setdefault("bdist_dmg", bdist_dmg)
        cmdclass.setdefault("bdist_mac", bdist_mac)
    else:
        cmdclass.setdefault("bdist_rpm", bdist_rpm)
    cmdclass.setdefault("build_exe", build_exe)
    cmdclass.setdefault("install", install)
    cmdclass.setdefault("install_exe", install_exe)
    attrs.setdefault("executables", [])
    setuptools.setup(**attrs)


setup.__doc__ = setuptools.setup.__doc__


def plugin_install(dist: setuptools.Distribution) -> None:
    """Use a setuptools extension to customize Distribution options."""
    if getattr(dist, "executables", None) is None:
        return

    # Fix package discovery (setuptools >= 61)
    if getattr(dist, "py_modules", None) is None:
        dist.py_modules = []

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
