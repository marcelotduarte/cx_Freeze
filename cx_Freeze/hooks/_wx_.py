"""A collection of functions which are triggered automatically by finder when
wxPython (wx) package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for wxPython."""

    def wx_lib_colourutils(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("Carbon.Appearance")

    def wx_lib_pubsub_core(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The wx.lib.pubsub.core module modifies the search path which cannot
        be done in a frozen application in the same way; modify the module
        search path here instead so that the right modules are found; note
        that this only works if the import of wx.lib.pubsub.setupkwargs
        occurs first.
        """
        module.path.insert(0, module.file.parent / "kwargs")

    def wx_lib_wxcairo(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional package."""
        module.ignore_names.add("cairo")

    def wx_lib_wxcairo_wx_pycairo(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.update(["cairo", "macholib.MachO"])

    def wx_lib_wxcairo_wx_cairocffi(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("cairocffi")

    def wx_msw(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional package."""
        module.ignore_names.add("wx._msw")
