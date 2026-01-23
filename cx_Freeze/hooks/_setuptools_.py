"""A collection of functions which are triggered automatically by finder when
setuptools package is included.
"""

from __future__ import annotations

import importlib.metadata
import os
import sys
from typing import TYPE_CHECKING

from packaging.requirements import Requirement

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
        finder.include_package("setuptools._distutils")

        try:
            requires = importlib.metadata.requires(module.name)
        except importlib.metadata.PackageNotFoundError:
            requires = None
        if requires:
            core_names = set()
            for requirement_string in requires:
                require = Requirement(requirement_string)
                if require.marker is None:
                    continue
                if require.marker.evaluate({"extra": "core"}):
                    core_names.add(require.name)
        else:
            core_names = (
                "jaraco.functools",
                "jaraco.text",
                "more_itertools",
                "packaging",
                "platformdirs",
                "wheel",
            )
        failed = []
        for name in sorted(core_names):
            try:
                finder.include_module(name)
            except ImportError:  # noqa: PERF203
                failed.append(name)
        vendor = module.file.parent / "_vendor"
        if vendor.is_dir():
            finder.path.append(os.path.normpath(vendor))
            for name in failed:
                try:  # noqa: SIM105
                    finder.include_module(name)
                except ImportError:  # noqa: PERF203
                    pass
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
