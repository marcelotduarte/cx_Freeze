"""A collection of functions which are triggered automatically by finder when
pandas package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pandas."""

    def pandas(
        self,
        finder: ModuleFinder,
        module: Module,
    ) -> None:
        """The pandas package.

        Supported pypi and conda-forge versions (tested from 1.3.3 to 2.3.0).
        """
        finder.exclude_module("pandas.conftest")
        finder.exclude_module("pandas.testing")
        finder.exclude_module("pandas._testing")
        finder.exclude_module("pandas.tests")
        finder.include_package("pandas._config")
        finder.include_package("pandas._libs")

        code_bytes = module.file.read_bytes()
        code_bytes = code_bytes.replace(
            b"from pandas import testing", b"testing = None"
        )
        module.code = compile(
            code_bytes,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )

    def pandas_core__numba_executor(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core__numba_extensions(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(
            [
                "numba",
                "numba.core",
                "numba.core.datamodel",
                "numba.core.extending",
                "numba.core.imputils",
                "numba.typed",
            ]
        )

    def pandas_core__numba_kernels_mean_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core__numba_kernels_min_max_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core__numba_kernels_shared(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core__numba_kernels_sum_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba", "numba.extending"])

    def pandas_core__numba_kernels_var_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core_computation_engines(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numexpr"])

    def pandas_core_computation_expressions(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numexpr"])

    def pandas_core_groupby_numba_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core_nanops(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["scipy.stats"])

    def pandas_core_missing(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["scipy"])

    def pandas_core_util_numba_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core_window_numba_(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_core_window_online(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.core module."""
        module.ignore_names.update(["numba"])

    def pandas_io_clipboard(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.formats.style module."""
        module.ignore_names.update(
            [
                "AppKit",
                "Foundation",
                "PyQt4",
                "PyQt4.QtGui",
                "PyQt5",
                "PyQt5.QtWidgets",
                "qtpy",
                "qtpy.QtWidgets",
            ]
        )

    def pandas_io_common(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["botocore.exceptions"])

    def pandas_io_excel__base(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["xlrd"])

    def pandas_io_excel__calamine(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["python_calamine"])

    def pandas_io_excel__odfreader(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(
            [
                "odf.element",
                "odf.namespaces",
                "odf.office",
                "odf.opendocument",
                "odf.table",
                "odf.text",
            ]
        )

    def pandas_io_excel__odswriter(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(
            [
                "odf.config",
                "odf.opendocument",
                "odf.style",
                "odf.table",
                "odf.text",
            ]
        )

    def pandas_io_excel__openpyxl(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(
            [
                "openpyxl",
                "openpyxl.cell.cell",
                "openpyxl.descriptors.serialisable",
                "openpyxl.styles",
                "openpyxl.workbook",
            ]
        )

    def pandas_io_excel__pyxlsb(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["pyxlsb"])

    def pandas_io_excel__xlrd(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["xlrd"])

    def pandas_io_excel__xlsxwriter(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.excel module."""
        module.ignore_names.update(["xlsxwriter"])

    def pandas_io_feather_format(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in pandas.io.parsers.base_parser module."""
        module.ignore_names.update(["pyarrow"])

    def pandas_io_formats_printing(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.formats.printing module."""
        module.ignore_names.update(
            ["IPython", "IPython.core.formatters", "traitlets"]
        )

    def pandas_io_formats_xml(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.formats.xml module."""
        module.ignore_names.update(["lxml.etree"])

    def pandas_io_formats_style(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.formats.style module."""
        module.ignore_names.update(
            ["matplotlib", "matplotlib.colors", "matplotlib.pyplot"]
        )

    def pandas_io_formats_style_render(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in pandas.io.formats.style_render module."""
        module.ignore_names.update(
            ["markupsafe", "pandas.api.types.is_list_like"]
        )

    def pandas_io_gbq(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in pandas.io.parsers.base_parser module."""
        module.ignore_names.update(["google.auth.credentials"])

    def pandas_io_html(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.html module."""
        module.ignore_names.update(["bs4", "lxml.etree", "lxml.html"])

    def pandas_io_orc(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.orc module."""
        module.ignore_names.update(["fsspec", "pyarrow.fs"])

    def pandas_io_parsers_base_parser(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in pandas.io.parsers.base_parser module."""
        module.ignore_names.update(["pyarrow"])

    def pandas_io_parquet(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.sql module."""
        module.ignore_names.update(["pyarrow.parquet"])

    def pandas_io_pytables(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.io.pytables module."""
        module.ignore_names.update(["pandas.core.internals.Block", "tables"])

    def pandas_io_sql(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.sql module."""
        module.ignore_names.update(
            [
                "pyarrow",
                "sqlalchemy",
                "sqlalchemy.engine",
                "sqlalchemy.schema",
                "sqlalchemy.sql.expression",
                "sqlalchemy.types",
            ]
        )

    def pandas_io__util(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io._util module."""
        module.ignore_names.update(["pyarrow"])

    def pandas_io_xml(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas.io.xml module."""
        module.ignore_names.update(["lxml", "lxml.etree"])

    def pandas__libs_testing(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include module used by the pandas._libs.testing module."""
        finder.include_module("cmath")

    def pandas_plotting__core(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.plotting._core module."""
        module.ignore_names.add("matplotlib.axes")

    def pandas_plotting__misc(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas.plotting._misc module."""
        module.ignore_names.update(
            [
                "matplotlib.axes",
                "matplotlib.colors",
                "matplotlib.figure",
                "matplotlib.table",
            ]
        )

    def pandas__testing(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules in the pandas._testing module."""
        module.exclude_names.add("pytest")

    def pandas__testing_asserters(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas._testing.asserters module."""
        module.ignore_names.add("matplotlib.pyplot")

    def pandas__testing__io(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules in the pandas._testing._io module."""
        module.exclude_names.add("pytest")
