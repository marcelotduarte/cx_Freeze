"""Extends setuptools 'build' command."""

from __future__ import annotations

import os
from sysconfig import get_python_version

try:
    # setuptools 62.4.0 supports 'build'
    from setuptools.command.build import build as _build
except ImportError:
    _build = __import__("distutils.command.build", fromlist=["build"]).build

__all__ = ["Build"]


# pylint: disable=attribute-defined-outside-init,missing-function-docstring
class Build(_build):
    """Build everything needed to install."""

    user_options = _build.user_options + [
        ("build-exe=", None, "build directory for executables")
    ]

    def initialize_options(self):
        super().initialize_options()
        self.build_exe = None

    def finalize_options(self):
        super().finalize_options()

        # 'build_exe' is the actual directory that we will use for this
        if self.build_exe is None:
            python_version = get_python_version()
            dir_name = f"exe.{self.plat_name}-{python_version}"
            self.build_exe = os.path.join(self.build_base, dir_name)

    # copy to avoid sharing the object with parent class
    sub_commands = _build.sub_commands[:] + [("build_exe", None)]
