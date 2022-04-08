"""The classes and functions with which cx_Freeze extends setuptools."""

import setuptools  # isort:skip
import sys

from .command.build import Build as build
from .command.build_exe import BuildEXE as build_exe
from .command.install import Install as install
from .command.install_exe import InstallEXE as install_exe

if sys.platform == "win32":
    from .command.bdist_msi import BdistMSI as bdist_msi
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG as bdist_dmg
    from .command.bdist_mac import BdistMac as bdist_mac
else:
    from .command.bdist_rpm import BdistRPM as bdist_rpm

__all__ = ["Distribution", "setup"]


class Distribution(setuptools.Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)

    def has_executables(self):  # pylint: disable=C0116
        return self.executables and len(self.executables) > 0


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
