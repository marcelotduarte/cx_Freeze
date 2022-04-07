"""The classes and functions with which cx_Freeze extends setuptools."""
# pylint: disable=C0116,C0103,W0201

import setuptools  # isort:skip
import sys
from pathlib import Path
from typing import Optional

from .command.build import Build as build
from .command.build_exe import BuildEXE as build_exe
from .command.install import Install as install

if sys.platform == "win32":
    from .command.bdist_msi import BdistMSI as bdist_msi
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG as bdist_dmg
    from .command.bdist_mac import BdistMac as bdist_mac
else:
    from .command.bdist_rpm import BdistRPM as bdist_rpm

__all__ = [
    "install_exe",
    "setup",
]


class Distribution(setuptools.Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)


class install_exe(setuptools.Command):
    """Install executables built from Python scripts."""

    description = "install executables built from Python scripts"
    user_options = [
        ("install-dir=", "d", "directory to install executables to"),
        ("build-dir=", "b", "build directory (where to install from)"),
        ("force", "f", "force installation (overwrite existing files)"),
        ("skip-build", None, "skip the build steps"),
    ]

    def initialize_options(self):
        self.install_dir: Optional[str] = None
        self.force = 0
        self.build_dir = None
        self.skip_build = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_exe", "build_dir"))
        self.set_undefined_options(
            "install",
            ("install_exe", "install_dir"),
            ("force", "force"),
            ("skip_build", "skip_build"),
        )

    def run(self):
        if not self.skip_build:
            self.run_command("build_exe")
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)
        if sys.platform != "win32":
            install_dir = Path(self.install_dir)
            base_dir = install_dir.parent.parent
            bin_dir: Path = base_dir / "bin"
            if not bin_dir.exists():
                bin_dir.mkdir(parents=True)
            source_dir = ".." / install_dir.relative_to(base_dir)
            for executable in self.distribution.executables:
                name = executable.target_name
                source = source_dir / name
                target = bin_dir / name
                if target.exists():
                    target.unlink()
                target.symlink_to(source)
                self.outfiles.append(target.as_posix())

    def get_inputs(self):
        return self.distribution.executables or []

    def get_outputs(self):
        return self.outfiles or []


def _add_command_class(command_classes, name, cls):
    if name not in command_classes:
        command_classes[name] = cls


def setup(**attrs):
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
