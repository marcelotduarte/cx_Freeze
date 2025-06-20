"""A collection of functions which are triggered automatically by finder when
multiprocess package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks._multiprocessing_ import Hook as MPHook

if TYPE_CHECKING:
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(MPHook):
    """The Module Hook class."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        # remap to ...
        self.name = "multiprocessing"
