"""A collection of functions which are triggered automatically by finder when
jaraco namespace is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for jaraco."""

    def jaraco_functools(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("more_itertools")

    def jaraco_text(self, finder: ModuleFinder, module: Module) -> None:
        """jaraco.text requires a text file."""
        if module.in_file_system == 0:
            target_dir = module.name.replace(".", "/")
            for textfile in module.file.parent.glob("*.txt"):
                finder.zip_include_files(
                    textfile, f"{target_dir}/{textfile.name}"
                )
