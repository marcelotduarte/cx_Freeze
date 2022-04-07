"""Extends setuptools 'build' command."""
# TODO: Borrow the distutils.command.build module, because setuptools doesn't
# extend this module.

import distutils.command.build  # pylint: disable=deprecated-module
import os
import sysconfig

__all__ = ["Build"]


# pylint: disable=attribute-defined-outside-init
class Build(distutils.command.build.build):
    """Build everything needed to install."""

    user_options = distutils.command.build.build.user_options + [
        ("build-exe=", None, "build directory for executables")
    ]

    def get_sub_commands(self):
        sub_commands = distutils.command.build.build.get_sub_commands(self)
        if self.distribution.executables:
            sub_commands.append("build_exe")
        return sub_commands

    def initialize_options(self):
        distutils.command.build.build.initialize_options(self)
        self.build_exe = None

    def finalize_options(self):
        distutils.command.build.build.finalize_options(self)
        if self.build_exe is None:
            platform = sysconfig.get_platform()
            python_version = sysconfig.get_python_version()
            dir_name = f"exe.{platform}-{python_version}"
            self.build_exe = os.path.join(self.build_base, dir_name)
