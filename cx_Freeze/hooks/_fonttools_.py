"""A collection of functions which are triggered automatically by finder when
fontTools package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.module import Module


def load_fonttools_misc_maccreatortype(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("xattr")


def load_fonttools_ttlib_woff2(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.update(["brotlicffi", "brotli"])


def load_fonttools_ttlib_tables_grutils(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.update(["lz4", "lz4.block"])


def load_fonttools_ttlib_tables_otbase(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("uharfbuzz")


def load_fonttools_ttlib_sfnt(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("zopfli.zlib")


def load_fonttools_unicode(_, module: Module) -> None:
    """Ignore package for py2."""
    module.ignore_names.add("unicodedata2")
