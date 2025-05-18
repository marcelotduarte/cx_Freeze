"""A collection of functions which are triggered automatically by finder when
pandas package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pandas(finder: ModuleFinder, module: Module) -> None:  # noqa: ARG001
    """The pandas package.

    Supported pypi and conda-forge versions (tested from 1.3.3 to 2.2.3).
    """
    finder.include_package("pandas._libs")
    finder.exclude_module("pandas.conftest")
    finder.exclude_module("pandas.tests")


def load_pandas_io_formats_style(_, module: Module) -> None:
    """Ignore optional modules in the pandas.io.formats.style module."""
    module.ignore_names.update(
        ["matplotlib", "matplotlib.colors", "matplotlib.pyplot"]
    )


def load_pandas__libs_testing(
    finder: ModuleFinder,
    module: Module,  # noqa: ARG001
) -> None:
    """Include module used by the pandas._libs.testing module."""
    finder.include_module("cmath")


def load_pandas_plotting__core(_, module: Module) -> None:
    """Ignore optional modules in the pandas.plotting._core module."""
    module.ignore_names.add("matplotlib.axes")


def load_pandas_plotting__misc(_, module: Module) -> None:
    """Ignore optional modules in the pandas.plotting._misc module."""
    module.ignore_names.update(
        [
            "matplotlib.axes",
            "matplotlib.colors",
            "matplotlib.figure",
            "matplotlib.table",
        ]
    )


def load_pandas__testing(_, module: Module) -> None:
    """Ignore optional modules in the pandas._testing module."""
    module.exclude_names.add("pytest")


def load_pandas__testing_asserters(_, module: Module) -> None:
    """Ignore optional modules in the pandas._testing.asserters module."""
    module.ignore_names.add("matplotlib.pyplot")


def load_pandas__testing__io(_, module: Module) -> None:
    """Ignore optional modules in the pandas._testing._io module."""
    module.exclude_names.add("pytest")
