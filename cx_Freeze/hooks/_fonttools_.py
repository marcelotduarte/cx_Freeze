"""A collection of functions which are triggered automatically by finder when
fontTools package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.hooks.global_names import FONTTOOLS_TTLIB_GLOBAL_NAMES
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for fontTools."""

    def fonttools_misc_etree(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("lxml.etree")

    def fonttools_misc_maccreatortype(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("xattr")

    def fonttools_subset_svg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("lxml")

    def fonttools_ttlib(self, _finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(FONTTOOLS_TTLIB_GLOBAL_NAMES)

    def fonttools_ttlib_woff2(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.update(["brotlicffi", "brotli"])

    def fonttools_ttlib_tables_grutils(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.update(["lz4", "lz4.block"])

    def fonttools_ttlib_tables_otbase(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("uharfbuzz")

    def fonttools_ttlib_sfnt(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("zopfli.zlib")

    def fonttools_unicode(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore package for py2."""
        module.ignore_names.add("unicodedata2")

    def fonttools_unicodedata(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore package for py2."""
        module.ignore_names.add("unicodedata2")
