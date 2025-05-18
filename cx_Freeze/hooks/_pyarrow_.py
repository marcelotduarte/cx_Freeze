"""A collection of functions which are triggered automatically by finder when
pyarrow package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pyarrow.

    Supported pypi and conda-forge versions (tested from 14.0 to 20.0).
    """

    def pyarrow(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa:ARG002
    ) -> None:
        """The pyarrow must include vendored modules."""
        finder.exclude_module("pyarrow.tests")
        finder.include_module("pyarrow.vendored.docscrape")
        finder.include_module("pyarrow.vendored.version")
        finder.include_module("queue")
