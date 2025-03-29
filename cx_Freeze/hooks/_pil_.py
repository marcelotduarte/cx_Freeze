"""A collection of functions which are triggered automatically by finder when
Pillow (PIL) package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MACOS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pil(finder: ModuleFinder, module: Module) -> None:
    """The Pillow must be loaded as a package."""
    finder.include_package("PIL")
    source_dir = module.file.parent.parent / "pillow.libs"  # Pillow 10.2+
    if not source_dir.exists():
        source_dir = module.file.parent.parent / "Pillow.libs"
    if source_dir.exists():
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            finder.lib_files[source] = f"{target_dir}/{source.name}"
    if IS_LINUX and module.in_file_system == 0:
        module.in_file_system = 2
    # [macos] copy dependent files when using zip_include_packages
    if IS_MACOS:
        source_dir = module.file.parent / ".dylibs"
        if source_dir.exists() and module.in_file_system == 0:
            finder.include_files(source_dir, "lib/.dylibs")


def load_pil_fpximageplugin(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("olefile")


def load_pil_image(_, module: Module) -> None:
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


def load_pil_imagefilter(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("numpy")


def load_pil_imageqt(_, module: Module) -> None:
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


def load_pil_imagetk(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("tkinter")


def load_pil_imageshow(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("IPython.display")


def load_pil_micimageplugin(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("olefile")


def load_pil_pyaccess(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("cffi")


def load_pil__tkinter_finder(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("tkinter")


def load_pil__typing(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("numpy.typing")
