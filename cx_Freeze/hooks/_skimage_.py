"""A collection of functions which are triggered automatically by finder when
scikit-image package is included.
"""

from __future__ import annotations

from importlib.machinery import SourceFileLoader
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for scikit-image."""

    def skimage(self, finder: ModuleFinder, module: Module) -> None:
        """Include the skimage package, using the lazy implementation."""
        module.lazy = True

        dist = finder.import_distributions.get(module.name)
        if dist and dist.files:
            # Exclude all tests
            excludes = set()
            for file in dist.files:
                if file.parent.match("**/tests"):
                    excludes.add(file.parent.as_posix().replace("/", "."))
            for exclude in excludes:
                finder.exclude_module(exclude)
            # Include stubs
            if module.in_file_system == 0:
                for file in dist.files:
                    if file.match("*.pyi"):
                        finder.zip_include_files(
                            file.locate(), file.as_posix()
                        )
            else:
                for file in dist.files:
                    if file.match("*.pyi"):
                        finder.include_files(
                            file.locate(), f"lib/{file.as_posix()}"
                        )

        # Exclude unnecessary modules
        finder.exclude_module("skimage.conftest")
        finder.exclude_module("skimage._shared.testing")

        # Include the required skimage sub-packages
        finder.include_package("skimage.data")
        finder.include_package("skimage.io")

        # Include pillow plugin
        try:
            finder.include_module("PIL")
        except ImportError:
            pass
        else:
            finder.include_module("imageio.plugins.pillow")

    def skimage_data(self, finder: ModuleFinder, module: Module) -> None:
        # using zip file, copy data to share folder
        if module.in_file_system == 0 and module.file:
            for file in module.file.parent.iterdir():
                if file.match("*.py*") or file.name == "tests":
                    continue
                finder.include_files(file, f"share/skimage/data/{file.name}")

    def skimage_data__fetchers(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, copy data to share folder - fix _LEGACY_DATA_DIR
        if module.in_file_system == 0:
            loader = module.loader
            if not isinstance(loader, SourceFileLoader):
                return
            source_code = loader.get_source(module.name)
            if source_code is None:
                return
            module.code = loader.source_to_code(
                source_code.replace(
                    "__file__",
                    "__import__('sys').prefix + '/share/skimage/data/file'",
                ),
                loader.get_filename(module.name),
                _optimize=finder.optimize,
            )

        module.exclude_names.add("pytest")
        module.ignore_names.add("pytest")

    def skimage_io_manage_plugins(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, fix directory to copy data to share folder
        if module.in_file_system == 0:
            loader = module.loader
            if not isinstance(loader, SourceFileLoader):
                return
            source_code = loader.get_source(module.name)
            if source_code is None:
                return
            module.code = loader.source_to_code(
                source_code.replace(
                    "__file__",
                    "__import__('sys').prefix + '/share/skimage/_'",
                ),
                loader.get_filename(module.name),
                _optimize=finder.optimize,
            )

    def skimage_io__plugins(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, copy data to share folder
        if module.in_file_system == 0 and module.file:
            for file in module.file.parent.iterdir():
                if file.match("*.ini"):
                    finder.include_files(
                        file, f"share/skimage/_plugins/{file.name}"
                    )

    def skimage__shared(self, finder: ModuleFinder, module: Module) -> None:
        finder.include_package(module.name)
