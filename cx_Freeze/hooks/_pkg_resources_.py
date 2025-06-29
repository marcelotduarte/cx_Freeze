"""A collection of functions which are triggered automatically by finder when
pkg_resources package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pkg_resources."""

    def pkg_resources(self, finder: ModuleFinder, module: Module) -> None:
        """The pkg_resources must load the _vendor subpackage."""
        module.ignore_names.update(
            ["_typeshed", "_typeshed.importlib", "typing_extensions"]
        )
        finder.exclude_module("pkg_resources.tests")
        try:
            finder.include_package("pkg_resources._vendor")
        except ImportError:
            pass  # pkg_resources from setuptools >= 71 does not uses _vendor
        else:
            module.ignore_names.update(
                [
                    "pkg_resources.extern.jaraco.text",
                    "pkg_resources.extern.packaging",
                    "pkg_resources.extern.packaging.markers",
                    "pkg_resources.extern.packaging.requirements",
                    "pkg_resources.extern.packaging.specifiers",
                    "pkg_resources.extern.packaging.utils",
                    "pkg_resources.extern.packaging.version",
                    "pkg_resources.extern.platformdirs",
                ]
            )
            finder.exclude_module(
                "pkg_resources._vendor.platformdirs.__main__"
            )

    def pkg_resources__vendor_jaraco_context(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("pkg_resources.extern.backports")

    def pkg_resources__vendor_jaraco_functools(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("pkg_resources.extern.more_itertools")

    def pkg_resources__vendor_jaraco_text(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(
            [
                "pkg_resources.extern.importlib_resources",
                "pkg_resources.extern.jaraco.context",
                "pkg_resources.extern.jaraco.functools",
            ]
        )

    def pkg_resources__vendor_packaging_metadata(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules_."""
        module.ignore_names.add("typing_extensions")

    def pkg_resources__vendor_platformdirs(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules_."""
        module.ignore_names.add("pkg_resources._vendor.typing_extensions")
