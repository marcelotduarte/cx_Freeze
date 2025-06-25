"""A collection of functions which are triggered automatically by finder when
re module is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import RE_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """Ignore names that should not be confused with modules to be imported."""

    def re(self, _finder: ModuleFinder, module: Module) -> None:
        if module.path:  # package since Python 3.11
            module.global_names.update(RE_GLOBAL_NAMES)
