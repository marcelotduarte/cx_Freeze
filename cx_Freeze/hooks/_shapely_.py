"""Hooks triggered by finder when shapely package is included."""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for shapely.

    Supported pypi versions (tested from 1.8.0 to 2.1.0).
    """

    # Note: shapely 1.8.5 supports Python <= 3.11

    def shapely(self, finder: ModuleFinder, module: Module) -> None:
        """Patch shapely."""
        finder.exclude_module("shapely.examples")  # shapely < 2.0
        finder.exclude_module("shapely.tests")  # shapely >= 2.0
        if module.in_file_system == 0:
            # shapely < 2.0 supports Python <= 3.11
            # The directory must be found when uing delvewheel < 1.7.0
            loader = module.loader
            if not isinstance(loader, SourceFileLoader):
                return
            source_code = loader.get_source(module.name)
            if source_code is None:
                return
            module.code = loader.source_to_code(
                source_code.replace(
                    "__file__", "__file__.replace('library.zip', '.')"
                ),
                loader.get_filename(module.name),
                _optimize=finder.optimize,
            )

    def shapely_geos(self, finder: ModuleFinder, module: Module) -> None:
        """Patch shapely.geos for shapely < 2.0."""
        # The directory must be found
        if module.in_file_system == 0:
            loader = module.loader
            if not isinstance(loader, SourceFileLoader):
                return
            source_code = loader.get_source(module.name)
            if source_code is None:
                return
            module.code = loader.source_to_code(
                source_code.replace(
                    "__file__", "__file__.replace('library.zip', '.')"
                ),
                loader.get_filename(module.name),
                _optimize=finder.optimize,
            )

    def shapely__geometry_helpers(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include for shapely._geometry_helpers (shapely >= 2.0)."""
        finder.include_module("shapely._geos")
