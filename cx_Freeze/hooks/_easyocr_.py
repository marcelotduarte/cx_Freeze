"""A collection of functions which are triggered automatically by finder when
easyocr package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for easyocr."""

    def easyocr(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The easyocr package."""
        finder.include_module("easyocr.easyocr")
        finder.include_module("easyocr.model.vgg_model")
        finder.include_module("imageio.plugins.pillow")

    def easyocr_easyocr(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["six", "pathlib2"])
