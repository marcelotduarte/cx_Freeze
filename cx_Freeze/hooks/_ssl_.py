"""A collection of functions which are triggered automatically by finder when
ssl module is included.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_ssl(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """In Windows, the SSL module requires additional dlls to be present in the
    build directory. In other OS certificates are required.
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
