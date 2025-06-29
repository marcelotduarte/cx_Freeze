"""A collection of functions which are triggered automatically by finder when
setuptools package is included.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_MINGW, IS_WINDOWS
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]

_setuptools_extern = [
    "setuptools.extern.jaraco.functools",
    "setuptools.extern.jaraco.text",
    "setuptools.extern.more_itertools",
    "setuptools.extern.ordered_set",
    "setuptools.extern.packaging",
    "setuptools.extern.packaging.markers",
    "setuptools.extern.packaging.requirements",
    "setuptools.extern.packaging.specifiers",
    "setuptools.extern.packaging.tags",
    "setuptools.extern.packaging.utils",
    "setuptools.extern.packaging.version",
    "setuptools.extern.platformdirs",
]


class Hook(ModuleHook):
    """The Hook class for setuptools."""

    def setuptools(self, finder: ModuleFinder, module: Module) -> None:
        """The setuptools must load the _distutils and _vendor subpackage."""
        finder.exclude_module("setuptools.tests")
        finder.exclude_module("setuptools._distutils.tests")
        with contextlib.suppress(ImportError):
            finder.include_package(f"{module.name}._distutils")
        with contextlib.suppress(ImportError):
            finder.include_package(f"{module.name}._vendor")

    def setuptools_command_build(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("typing_extensions")

    def setuptools_command_build_ext(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["Cython.Distutils.build_ext", "dl"])

    def setuptools_command_easy_install(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.jaraco.text")

    def setuptools_command_egg_info(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            ["setuptools.extern.jaraco.text", "setuptools.extern.packaging"]
        )

    def setuptools_config_setupcfg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(_setuptools_extern)

    def setuptools_config__apply_pyprojecttoml(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.packaging.specifiers")

    def setuptools_config_expand(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.more_itertools")

    def setuptools_config_pyprojecttoml(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            ["setuptools.extern.more_itertools", "setuptools.extern.tomli"]
        )

    def setuptools_config__validate_pyproject_formats(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            ["packaging", "trove_classifiers", "typing_extensions"]
        )

    def setuptools_depends(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.packaging")

    def setuptools_dist(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(_setuptools_extern)

    def setuptools__entry_points(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(_setuptools_extern)

    def setuptools_extension(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The setuptools.extension module optionally loads
        Pyrex.Distutils.build_ext but its absence is not considered an error.
        """
        module.ignore_names.add("Pyrex.Distutils.build_ext")

    def setuptools__importlib(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            [
                "importlib_metadata",
                "setuptools.extern.importlib_metadata",
                "setuptools.extern.importlib_resources",
            ]
        )

    def setuptools__itertools(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.more_itertools")

    def setuptools__normalization(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.packaging")

    def setuptools_monkey(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Add hidden module."""
        finder.include_module("setuptools.msvc")

    def setuptools_package_index(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.more_itertools")

    def setuptools__reqs(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(_setuptools_extern)

    def setuptools_sandbox(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("org.python.modules.posix.PosixModule")

    def setuptools__vendor_jaraco_text(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            [
                "setuptools.extern.importlib_resources",
                "setuptools.extern.jaraco.context",
                "setuptools.extern.jaraco.functools",
            ]
        )

    def setuptools__vendor_jaraco_functools(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("setuptools.extern.more_itertools")

    def setuptools__vendor_packaging_metadata(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("typing_extensions")

    def setuptools_wheel(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(_setuptools_extern)

    def setuptools_windows_support(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        if not (IS_MINGW or IS_WINDOWS):
            module.exclude_names.update(["ctypes", "ctypes.wintypes"])
