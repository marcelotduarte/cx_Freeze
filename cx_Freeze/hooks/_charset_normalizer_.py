"""A collection of functions which are triggered automatically by finder when
charset_normalizer package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for charset_normalizer."""

    def charset_normalizer(self, finder: ModuleFinder, module: Module) -> None:
        """The charset_normalizer package."""
        finder.exclude_module(f"{module.name}.cli")

    def charset_normalizer_md(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """The charset_normalizer.md implicitly imports an extension module."""
        with suppress(ImportError):
            # charset_normalizer 3.0 to 3.4.4
            finder.include_module("charset_normalizer.md__mypyc")
        # charset_normalizer 3.4.5+
        suffix = "".join(module.file.suffixes)
        for mypyc in module.file.parent.parent.glob(f"*__mypyc{suffix}"):
            if mypyc.exists():
                finder.include_module(f"{mypyc.name.split('.')[0]}")
