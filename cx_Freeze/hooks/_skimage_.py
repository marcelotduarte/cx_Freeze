"""A collection of functions which are triggered automatically by finder when
scikit-image package is included.
"""

from __future__ import annotations

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

        # Exclude unnecessary modules
        if module.distribution is None:
            module.update_distribution("scikit-image")

        distribution = module.distribution
        if distribution:
            # Exclude all tests
            excludes = set()
            files = distribution.original.files or []
            for file in files:
                if file.parent.match("**/tests"):
                    excludes.add(file.parent.as_posix().replace("/", "."))
            for exclude in excludes:
                finder.exclude_module(exclude)
            # Include stubs
            if module.in_file_system == 0:
                for file in files:
                    if file.match("*.pyi"):
                        finder.zip_include_files(
                            file.locate(), file.as_posix()
                        )
            else:
                for file in files:
                    if file.match("*.pyi"):
                        finder.include_files(
                            file.locate(), f"lib/{file.as_posix()}"
                        )

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
        if module.in_file_system == 0:
            for file in module.file.parent.iterdir():
                if file.match("*.py*") or file.name == "tests":
                    continue
                finder.include_files(file, f"share/skimage/data/{file.name}")

    def skimage_data__fetchers(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, copy data to share folder - fix _LEGACY_DATA_DIR
        if module.in_file_system == 0:
            module.code = compile(
                module.file.read_bytes().replace(
                    b"__file__",
                    b"__import__('sys').prefix + '/share/skimage/data/file'",
                ),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )

        module.exclude_names.add("pytest")
        module.ignore_names.add("pytest")

    def skimage_io_manage_plugins(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, fix directory to copy data to share folder
        if module.in_file_system == 0:
            module.code = compile(
                module.file.read_bytes().replace(
                    b"__file__",
                    b"__import__('sys').prefix + '/share/skimage/_'",
                ),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )

    def skimage_io__plugins(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        # using zip file, copy data to share folder
        if module.in_file_system == 0:
            for file in module.file.parent.iterdir():
                if file.match("*.ini"):
                    finder.include_files(
                        file, f"share/skimage/_plugins/{file.name}"
                    )

    def skimage__shared(self, finder: ModuleFinder, module: Module) -> None:
        finder.include_package(module.name)
