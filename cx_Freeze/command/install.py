"""Extends setuptools 'install' command."""

import sys

import setuptools.command.install

__all__ = ["Install"]


# pylint: disable=attribute-defined-outside-init
class Install(setuptools.command.install.install):
    """Install everything from build directory."""

    user_options = setuptools.command.install.install.user_options + [
        ("install-exe=", None, "installation directory for executables")
    ]

    def expand_dirs(self):
        setuptools.command.install.install.expand_dirs(self)
        self._expand_attrs(["install_exe"])

    def get_sub_commands(self):
        sub_commands = setuptools.command.install.install.get_sub_commands(
            self
        )
        if self.distribution.executables:
            sub_commands.append("install_exe")
        return [s for s in sub_commands if s != "install_egg_info"]

    def initialize_options(self):
        setuptools.command.install.install.initialize_options(self)
        self.install_exe = None

    def finalize_options(self):
        if self.prefix is None and sys.platform == "win32":
            winreg = __import__("winreg")
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion",
            )
            prefix = str(winreg.QueryValueEx(key, "ProgramFilesDir")[0])
            metadata = self.distribution.metadata
            self.prefix = f"{prefix}/{metadata.name}"
        setuptools.command.install.install.finalize_options(self)
        self.convert_paths("exe")
        if self.root is not None:
            self.change_roots("exe")

    def select_scheme(self, name):
        setuptools.command.install.install.select_scheme(self, name)
        if self.install_exe is None:
            if sys.platform == "win32":
                self.install_exe = "$base"
            else:
                metadata = self.distribution.metadata
                dir_name = f"{metadata.name}-{metadata.version}"
                self.install_exe = f"$base/lib/{dir_name}"
