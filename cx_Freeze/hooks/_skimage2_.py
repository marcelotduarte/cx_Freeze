"""Hooks triggered by finder when scikit-image package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks._skimage_ import Hook

if TYPE_CHECKING:
    from cx_Freeze.module import Module

__all__ = ["Hook_skimage2"]


class Hook_skimage2(Hook):
    """The Hook class for helper namespace _skimage2 (scikit-image)."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        self.name = "skimage"
