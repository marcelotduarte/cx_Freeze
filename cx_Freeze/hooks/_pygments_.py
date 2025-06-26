"""A collection of functions which are triggered automatically by finder when
pygments package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pygments."""

    def pygments(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The pygments package dynamically load styles."""
        finder.include_package("pygments.styles")
        finder.include_package("pygments.lexers")
        finder.include_package("pygments.formatters")

    def pygments_lexer(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional package."""
        module.ignore_names.add("chardet")

    def pygments_lexers_cplint(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("pygments.lexers.PrologLexer")

    def pygments_formatters_img(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("PIL")

    def pygments_formatters_html(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional package."""
        module.ignore_names.add("ctags")
