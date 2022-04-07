"""Implements the 'install_exe' command."""

import sys
from pathlib import Path
from typing import Optional

from setuptools import Command

__all__ = ["InstallEXE"]


# pylint: disable=attribute-defined-outside-init,missing-function-docstring
class InstallEXE(Command):
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
