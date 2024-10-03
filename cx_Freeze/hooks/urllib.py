"""A collection of functions which are triggered automatically by finder when
urllib package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MACOS, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_urllib_request(
    finder: ModuleFinder,  # noqa: ARG001
    module: Module,
) -> None:
    """Ignore optional modules."""
    if not IS_MACOS:
        module.ignore_names.add("_scproxy")
    if not IS_WINDOWS:
        module.ignore_names.add("nturl2path")
