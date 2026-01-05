"""A collection of functions which are triggered automatically by finder when
pkg_resources package is included.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pkg_resources.

    Since cx_Freeze 8.5.0, setuptools>=78.1.1 is used.
    """

    def pkg_resources(self, finder: ModuleFinder, module: Module) -> None:
        """The pkg_resources must import modules from the setuptools."""
        finder.exclude_module("pkg_resources.tests")

        vendor = os.path.normpath(
            module.file.parent.parent / "setuptools" / "_vendor"
        )
        failed = []
        for name in ("jaraco.text", "packaging", "platformdirs"):
            try:
                finder.include_module(name)
            except ImportError:  # noqa: PERF203
                failed.append(name)
        finder.path.append(vendor)
        for name in failed:
            finder.include_module(name)
        finder.path.pop()
