"""Create standalone executables from Python scripts, with the same performance
and is cross-platform."""
# pylint: disable=invalid-name

import setuptools  # isort:skip
import sys

from .command.build import Build as build
from .command.build_exe import BuildEXE as build_exe
from .command.install import Install as install
from .command.install_exe import InstallEXE as install_exe
from .dist import Distribution
from .exception import ConfigError
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer

__all__ = [
    "build",
    "build_exe",
    "install",
    "install_exe",
    "setup",
    "ConfigError",
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

__version__ = "6.13.1"


def _add_command_class(command_classes, name, cls):
    if name not in command_classes:
        command_classes[name] = cls


def setup(**attrs):  # pylint: disable=C0116
    attrs.setdefault("distclass", Distribution)
    command_classes = attrs.setdefault("cmdclass", {})
    if sys.platform == "win32":
        _add_command_class(command_classes, "bdist_msi", bdist_msi)
    elif sys.platform == "darwin":
        _add_command_class(command_classes, "bdist_dmg", bdist_dmg)
        _add_command_class(command_classes, "bdist_mac", bdist_mac)
    else:
        _add_command_class(command_classes, "bdist_rpm", bdist_rpm)
    _add_command_class(command_classes, "build", build)
    _add_command_class(command_classes, "build_exe", build_exe)
    _add_command_class(command_classes, "install", install)
    _add_command_class(command_classes, "install_exe", install_exe)
    setuptools.setup(**attrs)


setup.__doc__ = setuptools.setup.__doc__
