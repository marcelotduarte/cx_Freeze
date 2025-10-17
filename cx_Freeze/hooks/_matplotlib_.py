"""A collection of functions which are triggered automatically by finder when
matplotlib package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._bytecode import code_object_replace_function
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder

__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for matplotlib.

    Supported pypi versions (tested from 3.3 to 3.10.3).
    """

    def matplotlib(self, finder: ModuleFinder, module: Module) -> None:
        finder.exclude_module("matplotlib.sphinxext")
        finder.exclude_module("matplotlib.testing")
        finder.exclude_module("matplotlib.tests")
        finder.exclude_module("mpl_toolkits.tests")
        with suppress(ImportError):
            finder.include_module("mpl_toolkits")
        module.ignore_names.update(["certifi", "setuptools_scm", "pytest"])
        module.exclude_names.update(["pytest"])
        finder.include_package("matplotlib")

        # mpl-data is always in a subdirectory in matplotlib >= 3.4
        if module.in_file_system == 0:
            # zip_include_packages
            source_data = module.file.parent / "mpl-data"
            target_data = "lib/mpl-data"
            self._patch_data_path(module, target_data)
            finder.include_files(
                source_data, target_data, copy_dependent_files=False
            )

    def matplotlib_axes(self, _finder: ModuleFinder, module: Module) -> None:
        module.global_names.update(
            [
                "Axes",  # matplotlib < 3.9
                "Subplot",  # matplotlib < 3.7
                "SubplotBase",  # matplotlib < 3.7
                "rcParams",  # matplotlib < 3.7
                "subplot_class_factory",  # matplotlib < 3.7
            ]
        )

    def matplotlib_backend_bases(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["IPython", "IPython.core"])

    def matplotlib_backends_backend_cairo(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["cairo", "cairocffi"])

    def matplotlib_backends_backend_macosx(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["matplotlib.backends._macosx"])

    def matplotlib_backends__backend_gtk(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["gi", "gi.repository"])

    def matplotlib_backends_backend_gtk3(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["gi", "gi.repository"])

    def matplotlib_backends_backend_gtk3agg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["cairo"])

    def matplotlib_backends_backend_gtk4(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["gi", "gi.repository"])

    def matplotlib_backends_backend_gtk4agg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["cairo"])

    def matplotlib_backends_backend_nbagg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(
            [
                "IPython.display",
                "IPython.kernel.comm",  # matplotlib < 3.6
                "ipykernel.comm",
            ]
        )

    def matplotlib_backends_backend_qtagg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["PyQt6"])

    def matplotlib_backends_backend_qtcairo(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["PyQt6"])

    def matplotlib_backends__backend_tk(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(
            [
                "tkinter",
                "tkinter.filedialog",
                "tkinter.font",
                "tkinter.messagebox",
                "tkinter.simpledialog",
            ]
        )

    def matplotlib_backends_backend_webagg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(
            [
                "tornado",
                "tornado.ioloop",
                "tornado.template",
                "tornado.web",
                "tornado.websocket",
            ]
        )

    def matplotlib_backends_backend_webagg_core(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["tornado"])

    def matplotlib_backends_backend_wx(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["wx", "wx.svg"])

    def matplotlib_backends_backend_wxagg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["wx"])

    def matplotlib_backends_backend_wxcairo(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(["wx.lib.wxcairo"])

    def matplotlib_backends_qt_compat(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.update(
            [
                "PyQt4",  # matplotlib < 3.5
                "PyQt5",
                "PyQt6",
                "PySide",  # matplotlib < 3.5
                "PySide2",
                "PySide6",
                "shiboken",  # matplotlib < 3.5
                "shiboken2",
                "shiboken6",
                "sip",
            ]
        )

    def matplotlib_cbook(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names.update(
            ["gi.repository", "numpy.VisibleDeprecationWarning"]
        )

    def matplotlib_pyplot(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names.update(["IPython", "IPython.core.pylabtools"])

    def matplotlib_tri(self, _finder: ModuleFinder, module: Module) -> None:
        module.global_names.update(["Triangulation"])

    def _patch_data_path(self, module: Module, data_path: str) -> None:
        # fix get_data_path functions when using zip_include_packages or
        # with some distributions that have matplotlib < 3.4 installed.
        code = module.code
        if code is None:
            return
        for name in ("_get_data_path", "get_data_path"):
            source = f"""\
            def {name}():
                import os.path as _p
                import sys as _sys
                return _p.normpath(_p.join(_sys.prefix, "{data_path}"))
            """
            # patch if the name (_get_data_path and/or get_data_path) is found
            code = code_object_replace_function(code, name, source)
        module.code = code
