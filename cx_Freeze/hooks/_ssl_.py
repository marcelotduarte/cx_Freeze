"""A collection of functions which are triggered automatically by finder when
ssl module is included.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for ssl."""

    def ssl(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """In Windows, the SSL module requires additional dlls to be present in
        the build directory. In other OS certificates are required.
        """
        if IS_WINDOWS:
            parts = ["DLLs", "Library/bin"]
            patterns = ["libcrypto-*.dll", "libssl-*.dll"]
            for part in parts:
                for pattern in patterns:
                    for source in Path(sys.base_prefix, part).glob(pattern):
                        target = f"lib/{source.name}"
                        finder.lib_files[source] = target
                        finder.include_files(source, target)
