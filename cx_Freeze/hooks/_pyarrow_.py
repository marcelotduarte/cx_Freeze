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

    Supported pypi and conda-forge versions (tested from 14.0 to 22.0).
    """

    def pyarrow(self, finder: ModuleFinder, module: Module) -> None:
        """The pyarrow must include vendored modules."""
        module.ignore_names.update(["setuptools_scm", "setuptools_scm.git"])
        finder.exclude_module("pyarrow.include")
        finder.exclude_module("pyarrow.includes")
        finder.exclude_module("pyarrow.src")
        finder.exclude_module("pyarrow.tests")
        finder.include_module("pyarrow.vendored.docscrape")
        finder.include_module("pyarrow.vendored.version")
        finder.include_module("queue")

    def pyarrow_fs(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("fsspec")

    def pyarrow_util(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("requests")

    def pyarrow_vendored_docscrape(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("sphinx.ext.autodoc")
