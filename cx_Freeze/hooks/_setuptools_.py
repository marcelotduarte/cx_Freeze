"""A collection of functions which are triggered automatically by finder when
setuptools package is included.
"""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for setuptools.

    Since cx_Freeze 8.5.0, setuptools>=78.1.1 is used.
    """

    def setuptools(self, finder: ModuleFinder, module: Module) -> None:
        """The setuptools must load the _distutils and _vendor subpackage."""
        finder.exclude_module("setuptools.tests")
        finder.exclude_module("setuptools._distutils.tests")
        finder.exclude_module("setuptools._vendor")
        finder.include_package(f"{module.name}._distutils")

        vendor = os.path.normpath(module.file.parent / "_vendor")
        names = (
            "jaraco.collections",
            "jaraco.context",
            "jaraco.functools",
            "jaraco.text",
            "more_itertools",
            "packaging",
            "platformdirs",
        )
        failed = []
        for name in names:
            try:
                finder.include_module(name)
            except ImportError:  # noqa: PERF203
                failed.append(name)
        finder.path.append(vendor)
        for name in failed:
            finder.include_module(name)
        finder.path.pop()

    def setuptools_command_bdist_wheel(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """The setuptools.command.bdist_wheel must load the wheel package
        from _vendor subpackage.
        """
        try:
            finder.include_module("wheel")
        except ImportError:
            vendor = os.path.normpath(module.root.file.parent / "_vendor")
            finder.path.append(vendor)
            finder.include_module("wheel")
            finder.path.pop()

    def setuptools_command_build_ext(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            ["Cython.Distutils.build_ext", "Cython.Compiler.Main", "dl"]
        )

    def setuptools_compat_py310(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        if sys.version_info >= (3, 11):
            module.ignore_names.add("tomli")
        else:
            module.ignore_names.add("tomllib")
            try:
                finder.include_module("tomli")
            except ImportError:
                vendor = os.path.normpath(module.root.file.parent / "_vendor")
                finder.path.append(vendor)
                finder.include_module("tomli")
                finder.path.pop()

    def setuptools_config__validate_pyproject_formats(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            ["setuptools._vendor.packaging", "trove_classifiers"]
        )

    def setuptools_extension(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The setuptools.extension module optionally loads
        Pyrex.Distutils.build_ext but its absence is not considered an error.
        """
        module.ignore_names.update(
            ["Cython.Distutils.build_ext", "Pyrex.Distutils.build_ext"]
        )

    def setuptools_monkey(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Add hidden module."""
        finder.include_module("setuptools.msvc")

    def setuptools_msvc(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        if not (IS_MINGW or IS_WINDOWS):
            module.exclude_names.add("winreg")

    def setuptools_windows_support(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        if not (IS_MINGW or IS_WINDOWS):
            module.exclude_names.update(["ctypes", "ctypes.wintypes"])
