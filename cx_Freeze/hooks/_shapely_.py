"""A collection of functions which are triggered automatically by finder when
shapely package is included.
"""

from __future__ import annotations

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
        """Hook for shapely."""
        finder.exclude_module("shapely.examples")  # shapely < 2.0
        finder.exclude_module("shapely.tests")  # shapely >= 2.0
        if module.in_file_system == 0:
            # shapely < 2.0 supports Python <= 3.11
            # The directory must be found when uing delvewheel < 1.7.0
            module.code = compile(
                module.file.read_bytes().replace(
                    b"__file__", b"__file__.replace('library.zip', '.')"
                ),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )

    def shapely_geos(self, finder: ModuleFinder, module: Module) -> None:
        """Hook for shapely.geos for shapely < 2.0."""
        # The directory must be found
        if module.in_file_system == 0:
            module.code = compile(
                module.file.read_bytes().replace(
                    b"__file__", b"__file__.replace('library.zip', '.')"
                ),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )

    def shapely__geometry_helpers(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Hook for shapely._geometry_helpers for shapely >= 2.0."""
        finder.include_module("shapely._geos")
