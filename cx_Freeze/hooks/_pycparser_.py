"""A collection of functions which are triggered automatically by finder when
pycparser package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pycparser.

    Supported versions: 2.21 to 3.0.
    """

    def pycparser(self, finder: ModuleFinder, module: Module) -> None:
        """Avoid permission denied issues on windows, using pycparser < 3.0.

        When lextab and yacctab modules are regenerated.
        """
        distribution = module.distribution
        if distribution and distribution.version < (3,):
            finder.include_module("pycparser.lextab")
            finder.include_module("pycparser.yacctab")
