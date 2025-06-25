"""A collection of functions which are triggered automatically by finder when
asyncio package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import ASYNCIO_GLOBAL_NAMES

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_asyncio(finder: ModuleFinder, module: Module) -> None:
    """The asyncio must be loaded as a package."""
    module.global_names.update(ASYNCIO_GLOBAL_NAMES)
    finder.include_package("asyncio")
