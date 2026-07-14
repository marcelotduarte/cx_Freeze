"""Hooks triggered by finder when Xlib package is included."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for Xlib."""

    def xlib_display(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Implicitly loads a number of extension modules for Xlib.display.

        Make sure this happens.
        """
        finder.include_module("Xlib.ext.xtest")
        finder.include_module("Xlib.ext.shape")
        finder.include_module("Xlib.ext.xinerama")
        finder.include_module("Xlib.ext.record")
        finder.include_module("Xlib.ext.composite")
        finder.include_module("Xlib.ext.randr")

    def xlib_support_connect(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Implicitly loads a number of extension modules.

        Make sure this happens.
        """
        if sys.platform.split("-", maxsplit=1)[0] == "OpenVMS":
            module_name = "vms_connect"
        else:
            module_name = "unix_connect"
        finder.include_module(f"Xlib.support.{module_name}")

    def xlib_xk(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Implicitly loads some keysymdef modules for Xlib.XK module.

        Make sure this happens.
        """
        finder.include_module("Xlib.keysymdef.miscellany")
        finder.include_module("Xlib.keysymdef.latin1")
