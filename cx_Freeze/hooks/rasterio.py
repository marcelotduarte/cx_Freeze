"""A collection of functions which are triggered automatically by finder when
rasterio package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks._libs import replace_delvewheel_patch

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_rasterio(finder: ModuleFinder, module: Module) -> None:
    """The rasterio package loads items within itself in a way that causes
    problems without libs and data being present.
    """
    finder.include_package("rasterio")
    distribution = module.distribution
    if distribution:
        for file in distribution.binary_files:
            finder.include_files(
                file.locate().resolve(), f"lib/{file.as_posix()}"
            )
    replace_delvewheel_patch(module)
