"""A collection of functions which are triggered automatically by finder when
pygments package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pygments(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The pygments package dynamically load styles."""
    finder.include_package("pygments.styles")
    finder.include_package("pygments.lexers")
    finder.include_package("pygments.formatters")


def load_pygments_lexer(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("chardet")


def load_pygments_formatters_img(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("PIL")


def load_pygments_formatters_html(_, module: Module) -> None:
    """Ignore optional package."""
    module.ignore_names.add("ctags")
