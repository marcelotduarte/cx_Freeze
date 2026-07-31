"""Hooks triggered by finder when rasterio package is included."""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS
from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for rasterio.

    Tested rasterio versions of pypi from 1.3.0 to 1.5.0
    """

    def rasterio(self, finder: ModuleFinder, module: Module) -> None:
        """Load rasterio as a package.

        The rasterio package loads items within itself in a way that causes
        problems without libs and data being present.
        """
        # TODO: this can be optimized w/ finder.exclude_module("rasterio.rio")?
        finder.include_package("rasterio")

        if module.in_file_system == 0 and module.file:
            if IS_MACOS:  # rasterio fails in macOS using zipfile
                module.in_file_system = 1
                return
            # in zip file
            source_path = module.file.parent / "gdal_data"
            if source_path.is_dir():
                finder.include_files(
                    source_path, "share/gdal", copy_dependent_files=False
                )
            source_path = module.file.parent / "proj_data"
            if source_path.is_dir():
                finder.include_files(
                    source_path, "share/proj", copy_dependent_files=False
                )
            patch = r"""
                # cx_Freeze patch start
                import os as _os
                import sys as _sys
                _os.environ.setdefault(
                    "GDAL_DATA",
                    _os.path.join(_sys.prefix, "share", "gdal")
                )
                # cx_Freeze patch end
            """
            loader = module.loader
            if not isinstance(loader, SourceFileLoader):
                return
            source_code = loader.get_source(module.name)
            if source_code is None:
                return
            module.code = loader.source_to_code(
                dedent(patch) + source_code,
                loader.get_filename(module.name),
                _optimize=finder.optimize,
            )

    def rasterio_plot(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names.add("matplotlib.pyplot")

    def rasterio_rio_insp(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names |= {"IPython", "matplotlib.pyplot"}

    def rasterio_session(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names |= {"boto3", "swiftclient.client"}

    def rasterio__show_versions(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        dist = module.root.distribution
        version = tuple(map(int, dist.version[:3])) if dist else (0, 0, 0)
        if version != (1, 5, 0):
            return
        loader = module.loader
        if not isinstance(loader, SourceFileLoader):
            return
        source_code = loader.get_source(module.name)
        if source_code is None:
            return
        source_code = source_code.replace(
            "import importlib",
            "import importlib.metadata  # cx_Freeze patch # ",
        )
        module.code = loader.source_to_code(
            source_code,
            loader.get_filename(module.name),
            _optimize=finder.optimize,
        )

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
