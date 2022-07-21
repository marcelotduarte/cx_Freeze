"""Module for the Executable base class."""

import os
import string
import sys
from pathlib import Path
from sysconfig import get_config_var, get_platform
from typing import Optional, Union

from .common import get_resource_file_path, validate_args
from .exception import ConfigError

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)
WIN32 = sys.platform == "win32"

__all__ = ["Executable"]


class Executable:
    """
    Base Executable class.
    """

    def __init__(
        self,
        script: Union[str, Path],
        init_script: Optional[Union[str, Path]] = None,
        base: Optional[Union[str, Path]] = None,
        target_name: Optional[str] = None,
        icon: Optional[Union[str, Path]] = None,
        shortcut_name: Optional[str] = None,
        shortcut_dir: Optional[Union[str, Path]] = None,
        copyright: Optional[str] = None,  # pylint: disable=W0622
        trademarks: Optional[str] = None,
        manifest: Optional[Union[str, Path]] = None,
        uac_admin: bool = False,
        *,
        initScript: Optional[str] = None,
        targetName: Optional[str] = None,
        shortcutName: Optional[str] = None,
        shortcutDir: Optional[str] = None,
    ):
        self.main_script = script
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
        self.manifest = manifest
        self.uac_admin = uac_admin

    def __repr__(self):
        return f"<Executable script={self.main_script}>"

    @property
    def base(self) -> Path:
        """

        :return: the name of the base executable
        :rtype: Path

        """
        return self._base

    @base.setter
    def base(self, name: Optional[Union[str, Path]]):
        name = name or "console"
        if WIN32:
            py_version_nodot = get_config_var("py_version_nodot")
            platform_nodot = get_platform().replace(".", "").replace("-", "_")
            soabi = f"cp{py_version_nodot}-{platform_nodot}"
            suffix = ".exe"
        else:
            soabi = get_config_var("SOABI")
            suffix = ""
        name_base = f"{name}-{soabi}"
        self._base: Path = get_resource_file_path("bases", name_base, suffix)
        if self._base is None:
            raise ConfigError(f"no base named {name!r} ({name_base!r})")
        self._ext: str = suffix

    @property
    def icon(self) -> str:
        """

        :return: the path of the icon
        :rtype: Path

        """
        return self._icon

    @icon.setter
    def icon(self, name: Optional[Union[str, Path]]):
        self._icon: Path = Path(name) if name else None

    @property
    def init_module_name(self) -> str:
        """

        :return: the name of the init module in zip file
        :rtype: str

        """
        return f"{self._internal_name}__init__"

    @property
    def init_script(self) -> Path:
        """
        :return: the name of the initialization script that will be executed
        before the main script is executed
        :rtype: Path

        """
        return self._init_script

    @init_script.setter
    def init_script(self, name: Optional[Union[str, Path]]):
        name = name or "console"
        self._init_script: Path = get_resource_file_path(
            "initscripts", name, ".py"
        )
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
    def main_script(self) -> Path:
        """
        :return: the path of the file containing the script which is to be
        frozen
        :rtype: Path

        """
        return self._main_script

    @main_script.setter
    def main_script(self, name: Union[str, Path]):
        self._main_script: Path = Path(name)

    @property
    def manifest(self) -> Optional[str]:
        """
        :return: the XML schema of the manifest which is to be included in the
        frozen executable
        :rtype: str

        """
        return self._manifest

    @manifest.setter
    def manifest(self, name: Optional[Union[str, Path]]) -> None:
        self._manifest: Optional[str] = None
        if name is None:
            return
        if isinstance(name, str):
            name = Path(name)
        self._manifest = name.read_text(encoding="utf-8")

    @property
    def shortcut_name(self) -> str:
        """
        :return: the name to give a shortcut for the executable when included
        in an MSI package (Windows only).
        :rtype: str

        """
        return self._shortcut_name

    @shortcut_name.setter
    def shortcut_name(self, name: str):
        self._shortcut_name: str = name

    @property
    def shortcut_dir(self) -> Path:
        """
        :return: tthe directory in which to place the shortcut when being
        installed by an MSI package; see the MSI Shortcut table documentation
        for more information on what values can be placed here (Windows only).
        :rtype: Path

        """
        return self._shortcut_dir

    @shortcut_dir.setter
    def shortcut_dir(self, name: Union[str, Path]):
        self._shortcut_dir: Path = Path(name) if name else None

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
            name = self.main_script.stem
        else:
            pathname = Path(name)
            if name != pathname.name:
                raise ConfigError(
                    "target_name should only be the name, for example: "
                    f"{pathname.name}"
                )
            if sys.platform == "win32" and pathname.suffix.lower() == ".exe":
                name = pathname.stem
        self._name: str = name
        name = name.partition(".")[0]
        if not name.isidentifier():
            for invalid in STRINGREPLACE:
                name = name.replace(invalid, "_")
        name = os.path.normcase(name)
        if not name.isidentifier():
            raise ConfigError(f"Invalid name for target_name ({self._name!r})")
        self._internal_name: str = name
