"""A collection of functions which are triggered automatically by finder when
tiktoken package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for tiktoken."""

    def tiktoken(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The tiktoken must include extension."""
        finder.include_module("tiktoken_ext.openai_public")
