"""A collection of functions which are triggered automatically by finder when
jaraco namespace is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_jaraco_context(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("backports")


def load_jaraco_functools(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("more_itertools")


def load_jaraco_text(finder: ModuleFinder, module: Module) -> None:
    """jaraco.text requires a text file."""
    if module.in_file_system == 0:
        target_dir = module.name.replace(".", "/")
        for textfile in module.file.parent.glob("*.txt"):
            finder.zip_include_files(textfile, f"{target_dir}/{textfile.name}")
