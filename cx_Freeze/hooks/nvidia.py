"""A collection of functions which are triggered automatically by finder when
nvidia package is included.
"""

from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_nvidia(finder: ModuleFinder, module: Module) -> None:
    """Hook for nvidia."""
    # include the cuda libraries as fixed libraries
    if IS_MINGW or IS_WINDOWS:
        extension = "*.dll"
    elif IS_MACOS:
        extension = "*.dylib"
    else:
        extension = "*.so*"

    source_lib = module.file.parent
    if source_lib.exists():
        target_lib = f"lib/{source_lib.name}"
        for source in source_lib.glob(f"*/lib/{extension}"):
            library = source.relative_to(source_lib).as_posix()
            finder.lib_files[source] = f"{target_lib}/{library}"

    code_string = module.file.read_text(encoding="utf_8")
    # fix for issue #2682
    patch = dedent(
        f"""
        def _cxfreeze_patch():
            import ctypes
            import sys
            from pathlib import Path

            source_lib = Path(sys.frozen_dir, "lib", "nvidia")
            for source in source_lib.glob("*/lib/{extension}"):
                ctypes.CDLL(source)
        _cxfreeze_patch()
        """
    )
    module.code = compile(
        code_string + patch,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )
