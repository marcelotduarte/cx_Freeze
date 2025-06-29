"""A collection of functions which are triggered automatically by finder when
Pillow (PIL) package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for Pillow."""

    def pil(self, finder: ModuleFinder, module: Module) -> None:
        """The Pillow must be loaded as a package."""
        finder.include_package("PIL")
        module.update_distribution("pillow")
        if IS_LINUX and module.in_file_system == 0:
            module.in_file_system = 2

    def pil_fpximageplugin(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("olefile")

    def pil_image(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            {
                "cffi",
                "defusedxml",
                "defusedxml.ElementTree",
                "IPython.lib.pretty",
                "numpy",
            }
        )

    def pil_imagefilter(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("numpy")

    def pil_imageqt(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            {
                "PyQt5.QtCore",
                "PyQt5.QtGui",
                "PyQt6",
                "PyQt6.QtCore",
                "PyQt6.QtGui",
                "PySide2.QtCore",
                "PySide2.QtGui",
                "PySide6",
                "PySide6.QtCore",
                "PySide6.QtGui",
            }
        )

    def pil_imagetk(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("tkinter")

    def pil_imageshow(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("IPython.display")

    def pil_micimageplugin(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("olefile")

    def pil_pyaccess(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("cffi")

    def pil__tkinter_finder(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("tkinter")

    def pil__typing(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("numpy.typing")
