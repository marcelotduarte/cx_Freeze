"""A collection of functions which are triggered automatically by finder when
PyGObject package is included.
"""

from __future__ import annotations

import sys
import sysconfig
from ctypes.util import find_library
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

# To test in Ubuntu, pulls all dependencies for pygobject, then install it:
# sudo apt install python3-gi libgirepository1.0-dev libcairo2-dev
# pip install pygobject


def load_gi(finder: ModuleFinder, module: Module) -> None:
    """The PyGObject package."""
    libraries = [
        "libgtk-3-0",
        "libgdk-3-0",
        "libepoxy-0",
        "libgdk_pixbuf-2.0-0",
        "libpango-1.0-0",
        "libpangocairo-1.0-0",
        "libpangoft2-1.0-0",
        "libpangowin32-1.0-0",
        "libatk-1.0-0",
    ]
    for lib in libraries:
        name = find_library(lib)
        if name:
            library_path = (
                Path(sys.base_prefix, "bin", name) if IS_LINUX else Path(name)
            )
            finder.include_files(library_path, f"lib/{library_path.name}")

    common_namespaces = [
        "Atk-1.0",
        "GLib-2.0",
        "GModule-2.0",
        "GObject-2.0",
        "Gdk-3.0",
        "GdkPixbuf-2.0",
        "Gio-2.0",
        "Gtk-3.0",
        "Pango-1.0",
        "cairo-1.0",
        "HarfBuzz-0.0",
        "freetype2-2.0",
    ]

    if IS_LINUX:
        libdir = Path(sysconfig.get_config_var("LIBDIR"))
    else:
        libdir = Path(sys.base_prefix, "lib")

    for ns in common_namespaces:
        subpath = f"girepository-1.0/{ns}.typelib"
        fullpath = libdir / subpath
        if fullpath.exists():
            finder.include_files(fullpath, f"lib/{subpath}")

    finder.include_package(module.name)
