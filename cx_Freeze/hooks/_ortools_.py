"""A collection of functions which are triggered automatically by finder when
ortools package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for ortools."""

    def ortools(self, finder: ModuleFinder, module: Module) -> None:
        if module.in_file_system == 0:
            module.in_file_system = 2
        distribution = module.distribution
        if distribution.installer == "conda":
            finder.include_module("numpy")
