"""Module for the Executable base class."""

from __future__ import annotations

import os
import string
import sys
from pathlib import Path
from sysconfig import get_config_var, get_platform

from setuptools import Distribution

from ._compat import IS_MINGW, IS_WINDOWS
from .common import get_resource_file_path
from .exception import OptionError, SetupError

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)

__all__ = ["Executable"]


class Executable:
    """Base Executable class."""

    def __init__(
        self,
        script: str | Path,
        init_script: str | Path | None = None,
        base: str | Path | None = None,
        target_name: str | None = None,
        icon: str | Path | None = None,
        shortcut_name: str | None = None,
        shortcut_dir: str | Path | None = None,
        copyright: str | None = None,  # noqa: A002
        trademarks: str | None = None,
        manifest: str | Path | None = None,
        uac_admin: bool = False,
    ):
        self.main_script = script
        self.init_script = init_script
        self.base = base
        self.target_name = target_name
        self.icon = icon
        self.shortcut_name = shortcut_name
        self.shortcut_dir = shortcut_dir
        self.copyright = copyright
        self.trademarks = trademarks
        self.manifest = manifest
        self.uac_admin = uac_admin

    def __repr__(self):
        return f"<Executable script={self.main_script}>"

    @property
    def base(self) -> Path:
        """:return: the name of the base executable
        :rtype: Path

        """
        return self._base

    @base.setter
    def base(self, name: str | Path | None):
        name = name or "console"
        if IS_WINDOWS or IS_MINGW:
            platform_nodot = get_platform().replace(".", "").replace("-", "_")
            soabi = f"{sys.implementation.cache_tag}-{platform_nodot}"
            suffix = ".exe"
        else:
            soabi = get_config_var("SOABI")
            suffix = ""
        name_base = f"{name}-{soabi}"
        self._base: Path = get_resource_file_path("bases", name_base, suffix)
        if self._base is None:
            raise OptionError(f"no base named {name!r} ({name_base!r})")
        self._ext: str = suffix

    @property
    def icon(self) -> str:
        """:return: the path of the icon
        :rtype: Path

        """
        return self._icon

    @icon.setter
    def icon(self, name: str | Path | None):
        self._icon: Path = Path(name) if name else None

    @property
    def init_module_name(self) -> str:
        """:return: the name of the init module in zip file
        :rtype: str

        """
        return f"{self._internal_name}__init__"

    @property
    def init_script(self) -> Path:
        """:return: the name of the initialization script that will be executed
        before the main script is executed
        :rtype: Path

        """
        return self._init_script

    @init_script.setter
    def init_script(self, name: str | Path | None):
        name = name or "console"
        self._init_script: Path = get_resource_file_path(
            "initscripts", name, ".py"
        )
        if self._init_script is None:
            raise OptionError(f"no init_script named {name}")

    @property
    def main_module_name(self) -> str:
        """:return: the name of the main module in zip file
        :rtype: str

        """
        return f"{self._internal_name}__main__"

    @property
    def main_script(self) -> Path:
        """:return: the path of the file containing the script which is to be
        frozen
        :rtype: Path

        """
        return self._main_script

    @main_script.setter
    def main_script(self, name: str | Path):
        self._main_script: Path = Path(name)

    @property
    def manifest(self) -> str | None:
        """:return: the XML schema of the manifest which is to be included in
        the frozen executable
        :rtype: str

        """
        return self._manifest

    @manifest.setter
    def manifest(self, name: str | Path | None) -> None:
        self._manifest: str | None = None
        if name is None:
            return
        if isinstance(name, str):
            name = Path(name)
        self._manifest = name.read_text(encoding="utf-8")

    @property
    def shortcut_name(self) -> str:
        """:return: the name to give a shortcut for the executable when
        included in an MSI package (Windows only).
        :rtype: str

        """
        return self._shortcut_name

    @shortcut_name.setter
    def shortcut_name(self, name: str):
        self._shortcut_name: str = name

    @property
    def shortcut_dir(self) -> Path:
        """:return: tthe directory in which to place the shortcut when being
        installed by an MSI package; see the MSI Shortcut table documentation
        for more information on what values can be placed here (Windows only).
        :rtype: Path

        """
        return self._shortcut_dir

    @shortcut_dir.setter
    def shortcut_dir(self, name: str | Path):
        self._shortcut_dir: Path = Path(name) if name else None

    @property
    def target_name(self) -> str:
        """:return: the name of the target executable
        :rtype: str

        """
        return self._name + self._ext

    @target_name.setter
    def target_name(self, name: str | None):
        if name is None:
            name = self.main_script.stem
        else:
            pathname = Path(name)
            if name != pathname.name:
                raise OptionError(
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
            raise OptionError(f"Invalid name for target_name ({self._name!r})")
        self._internal_name: str = name


def validate_executables(dist: Distribution, attr: str, value):  # noqa: ARG001
    """Verify that value is a Executable list."""
    try:
        # verify that value is a list or tuple to exclude unordered
        # or single-use iterables
        assert isinstance(value, (list, tuple))
        # verify that elements of value are Executable
        for executable in value:
            assert isinstance(executable, Executable)
    except (TypeError, ValueError, AttributeError, AssertionError) as exc:
        raise SetupError(
            f"{attr!r} must be a list of Executable (got {value!r})"
        ) from exc
