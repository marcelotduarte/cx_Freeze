"""
Module for the Executable base class.
"""

import os
import string
import sys
from typing import Optional

from .common import get_resource_file_path, validate_args
from .exception import ConfigError

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)

__all__ = ["Executable"]


class Executable:
    """
    Base Executable class.
    """

    _base: str
    _init_script: str
    _internal_name: str
    _name: str
    _ext: str

    def __init__(
        self,
        script: str,
        init_script: Optional[str] = None,
        base: Optional[str] = None,
        target_name: Optional[str] = None,
        icon: Optional[str] = None,
        shortcut_name: Optional[str] = None,
        shortcut_dir: Optional[str] = None,
        copyright: Optional[str] = None,
        trademarks: Optional[str] = None,
        *,
        initScript: Optional[str] = None,
        targetName: Optional[str] = None,
        shortcutName: Optional[str] = None,
        shortcutDir: Optional[str] = None,
    ):
        self.main_script: str = script
        self.init_script = validate_args(
            "init_script", init_script, initScript
        )
        self.base = base
        self.target_name = validate_args(
            "target_name", target_name, targetName
        )
        self.icon = icon
        self.shortcut_name = validate_args(
            "shortcut_name", shortcut_name, shortcutName
        )
        self.shortcut_dir = validate_args(
            "shortcut_dir", shortcut_dir, shortcutDir
        )
        self.copyright = copyright
        self.trademarks = trademarks

    def __repr__(self):
        return f"<Executable script={self.main_script}>"

    @property
    def base(self) -> str:
        """

        :return: the name of the base executable
        :rtype: str

        """
        return self._base

    @base.setter
    def base(self, name: Optional[str]):
        name = name or "Console"
        ext = ".exe" if sys.platform == "win32" else ""
        self._base = get_resource_file_path("bases", name, ext)
        if self._base is None:
            raise ConfigError(f"no base named {name!r}")

    @property
    def init_module_name(self) -> str:
        """

        :return: the name of the init module in zip file
        :rtype: str

        """
        return f"{self._internal_name}__init__"

    @property
    def init_script(self) -> str:
        """
        :return: the name of the initialization script that will be executed
        before the actual script is executed
        :rtype: str

        """
        return self._init_script

    @init_script.setter
    def init_script(self, name: Optional[str]):
        name = name or "Console"
        self._init_script = get_resource_file_path("initscripts", name, ".py")
        if self._init_script is None:
            raise ConfigError(f"no init_script named {name}")

    @property
    def main_module_name(self) -> str:
        """

        :return: the name of the main module in zip file
        :rtype: str

        """
        return f"{self._internal_name}__main__"

    @property
    def target_name(self) -> str:
        """

        :return: the name of the target executable
        :rtype: str

        """
        return self._name + self._ext

    @target_name.setter
    def target_name(self, name: Optional[str]):
        if name is None:
            name = os.path.splitext(os.path.basename(self.main_script))[0]
            ext = os.path.splitext(self.base)[1]
        else:
            if name != os.path.basename(name):
                raise ConfigError(
                    "target_name should only be the name, for example: "
                    f"{os.path.basename(name)}"
                )
            if sys.platform == "win32":
                if name.endswith(".exe"):
                    name, ext = os.path.splitext(name)
                else:
                    ext = ".exe"
            else:
                ext = ""
        self._name = name
        self._ext = ext
        name = name.partition(".")[0]
        if not name.isidentifier():
            for invalid in STRINGREPLACE:
                name = name.replace(invalid, "_")
        name = os.path.normcase(name)
        if not name.isidentifier():
            raise ConfigError(f"Invalid name for target_name ({self._name!r})")
        self._internal_name = name
