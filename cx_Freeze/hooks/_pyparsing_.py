"""A collection of functions which are triggered automatically by finder when
pyparsing package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import PYPARSING_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pyparsing."""

    def pyparsing(self, _finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(PYPARSING_GLOBAL_NAMES)

    def pyparsing_diagram(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional package."""
        module.ignore_names.update(["jinja2", "railroad"])
