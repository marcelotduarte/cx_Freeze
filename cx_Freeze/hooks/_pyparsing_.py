"""Hooks triggered by finder when pyparsing package is included."""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import PYPARSING_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pyparsing."""

    def pyparsing(self, finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(PYPARSING_GLOBAL_NAMES)

        # remove testing module
        finder.exclude_module("pyparsing.testing")
        # also, patch code to remove testing module
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code is None:
            return
        module.code = loader.source_to_code(
            source_code.replace(
                "from .testing import pyparsing_test as testing",
                "testing = None",
            ),
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )

    def pyparsing_core(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional (excluded) module."""
        module.ignore_names.add("pyparsing.testing")

    def pyparsing_diagram(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional packages."""
        module.ignore_names.update(["jinja2", "railroad"])
