"""Module for the Executable base class."""

from __future__ import annotations

import os
import string
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import (
    EXE_SUFFIX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
    SOABI,
)
from cx_Freeze.common import resource_path
from cx_Freeze.exception import OptionError, SetupError

if TYPE_CHECKING:
    from setuptools import Distribution

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)

__all__ = ["Executable", "validate_executables"]


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
        uac_uiaccess: bool = False,
    ) -> None:
        # private
        self._main_script: Path
        self._init_script: Path
        self._base: Path
        self._name: str = ""
        self._ext: str = EXE_SUFFIX
        self._internal_name: str = ""
        self._icon: Path | None = None
        self._manifest: str | None = None
        self._shortcut_name: str | None = None
        self._shortcut_dir: Path | None = None

        self.app_type = "console"

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
        self.uac_uiaccess = uac_uiaccess

    def __repr__(self) -> str:
        return f"<Executable script={self.main_script}>"

    @property
    def base(self) -> Path:
        """:return: the name of the base executable
        :rtype: Path

        """
        return self._base

    @base.setter
    def base(self, name: str | Path | None) -> None:
        if name:
            filename = Path(name)
            if filename.is_absolute():
                self._base = filename
                self._ext = filename.suffix
                return

        # The default base is console
        name = name or "console"

        # Get the app type (console, gui or service)
        self.app_type = name.lower().removeprefix("win32")

        # On non-windows systems the base console is used for any type of app
        if not (IS_WINDOWS or IS_MINGW) and name in ("gui", "service"):
            name = "console"
        if name.lower().startswith("win32"):
            name = f"legacy/{name.lower()}"
        if not name.startswith("legacy"):
            name = f"bases/{name}"
        filename = f"{name}-{SOABI}{EXE_SUFFIX}"
        self._base = resource_path(filename)
        if self._base is None:
            msg = f"no base named {name!r} ({filename!r})"
            raise OptionError(msg)

    @property
    def icon(self) -> Path | None:
        """:return: the path of the icon
        :rtype: Path

        """
        return self._icon

    @icon.setter
    def icon(self, name: str | Path | None) -> None:
        if name is None:
            return
        iconfile = Path(name)
        if not iconfile.suffix:
            # add an extension - defaults to .svg
            valid_extensions = [".png", ".svg"]
            if IS_WINDOWS or IS_MINGW:
                valid_extensions.insert(0, ".ico")
            elif IS_MACOS:
                valid_extensions.insert(0, ".icns")
            for ext in valid_extensions:
                iconfile = iconfile.with_suffix(ext)
                if iconfile.exists():
                    break
        self._icon = iconfile

    @property
    def init_module_name(self) -> str:
        """:return: the name of the init module in zip file
        :rtype: str

        """
        return f"__init__{self._internal_name}"

    @property
    def init_script(self) -> Path:
        """:return: the name of the initialization script that will be executed
        before the main script is executed
        :rtype: Path

        """
        return self._init_script

    @init_script.setter
    def init_script(self, name: str | Path | None) -> None:
        name = name or "console"
        filename = Path(name)
        if filename.is_absolute():
            self._init_script = filename
        else:
            filename = filename.with_suffix(".py")
            self._init_script = resource_path(f"initscripts/{filename}")
        if self._init_script is None:
            msg = f"no init_script named {name!r} ({filename!r})"
            raise OptionError(msg)

    @property
    def main_module_name(self) -> str:
        """:return: the name of the main module in zip file
        :rtype: str

        """
        return f"__main__{self._internal_name}"

    @property
    def main_script(self) -> Path:
        """:return: the path of the file containing the script which is to be
        frozen
        :rtype: Path

        """
        return self._main_script

    @main_script.setter
    def main_script(self, name: str | Path) -> None:
        self._main_script = Path(name)

    @property
    def manifest(self) -> str | None:
        """:return: the XML schema of the manifest which is to be included in
        the frozen executable
        :rtype: str

        """
        return self._manifest

    @manifest.setter
    def manifest(self, name: str | Path | None) -> None:
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
    def shortcut_name(self, name: str | None) -> None:
        self._shortcut_name = name

    @property
    def shortcut_dir(self) -> Path:
        """:return: the directory in which to place the shortcut when being
        installed by an MSI package; see the MSI Shortcut table documentation
        for more information on what values can be placed here (Windows only).
        :rtype: Path

        """
        return self._shortcut_dir

    @shortcut_dir.setter
    def shortcut_dir(self, name: str | Path | None) -> None:
        if name is None:
            return
        self._shortcut_dir = Path(name)

    @property
    def target_name(self) -> str:
        """:return: the name of the target executable
        :rtype: str

        """
        return self._name + self._ext

    @target_name.setter
    def target_name(self, name: str | None) -> None:
        if name is None:
            name = self.main_script.stem
        else:
            pathname = Path(name)
            if name != pathname.name:
                msg = (
                    "target_name cannot contain the path, only the filename: "
                    f"{pathname.name}"
                )
                raise OptionError(msg)
            if sys.platform == "win32" and pathname.suffix.lower() == ".exe":
                name = pathname.stem
        self._name = name
        name = name.partition(".")[0]
        if not name.isidentifier():
            for invalid in STRINGREPLACE:
                name = name.replace(invalid, "_")
        name = os.path.normcase(name)
        self._internal_name = name


def validate_executables(dist: Distribution, attr: str, value) -> None:
    """Verify that value is a valid executables attribute, which could be an
    Executable list, a mapping list or a string list.
    """
    try:
        # verify that value is a list or tuple to exclude unordered
        # or single-use iterables
        assert isinstance(value, (list, tuple))  # noqa: S101
        assert value  # noqa: S101
        # verify that elements of value are Executable, Dict or string
        for executable in value:
            assert isinstance(  # noqa: S101
                executable, (Executable, Mapping, str)
            )
    except (TypeError, ValueError, AttributeError, AssertionError) as exc:
        msg = f"{attr!r} must be a list of Executable (got {value!r})"
        raise SetupError(msg) from exc

    # Returns valid Executable list
    if dist.executables == value:
        dist.executables = []
    executables = list(value)
    for i, executable in enumerate(executables):
        if isinstance(executable, str):
            executables[i] = Executable(executable)
        elif isinstance(executable, Mapping):
            executables[i] = Executable(**executable)
    dist.executables.extend(executables)
