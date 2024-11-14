"""A collection of functions which are triggered automatically by finder when
asyncio package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_asyncio(finder: ModuleFinder, module: Module) -> None:
    """The asyncio must be loaded as a package."""
    module.global_names.update(
        ["get_event_loop", "iscoroutine", "iscoroutinefunction"]
    )
    finder.include_package("asyncio")
