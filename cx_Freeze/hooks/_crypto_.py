"""A collection of functions which are triggered automatically by finder when
pycryptodome package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks._cryptodome_ import Hook as CryptoHook

if TYPE_CHECKING:
    from cx_Freeze.module import Module

__all__ = ["Hook"]


class Hook(CryptoHook):
    """The Module Hook class."""

    def __init__(self, module: Module) -> None:
        super().__init__(module)
        self.name = "cryptodome"
