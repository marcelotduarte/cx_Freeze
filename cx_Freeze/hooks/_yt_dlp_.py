"""Hooks triggered by finder when yt_dlp package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for yt_dlp."""

    def yt_dlp(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include backends for yt_dlp package."""
        finder.include_module("yt_dlp.compat._deprecated")
        finder.include_module("yt_dlp.compat._legacy")
        finder.include_module("yt_dlp.utils._deprecated")
        finder.include_module("yt_dlp.utils._legacy")
