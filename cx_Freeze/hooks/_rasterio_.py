"""A collection of functions which are triggered automatically by finder when
rasterio package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for rasterio.

    Supported pypi versions (tested with 1.4.x).
    """

    def rasterio(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The rasterio package loads items within itself in a way that causes
        problems without libs and data being present.
        """
        # this can be optimized
        finder.include_package("rasterio")

    def rasterio__io(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        finder.include_module("rasterio.sample")
        finder.include_module("rasterio.vrt")

    def rasterio__warp(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        finder.include_module("rasterio._features")
