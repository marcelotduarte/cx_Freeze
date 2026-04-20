"""A collection of functions which are triggered automatically by finder when
scikit-learn package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for scikit-learn."""

    def sklearn(
        self,
        finder: ModuleFinder,
        module: Module,
    ) -> None:
        # Exclude unnecessary modules
        if module.distribution is None:
            module.update_distribution("scikit-learn")
        distribution = module.distribution
        if distribution:
            # Exclude tests
            excludes = set()
            files = distribution.original.files or []
            for file in files:
                if file.parent.match("**/conftest.py"):
                    exclude = file.with_suffix("").as_posix().replace("/", ".")
                    excludes.add(exclude)
            for file in files:
                if file.parent.match("**/tests"):
                    excludes.add(file.parent.as_posix().replace("/", "."))
            for exclude in excludes:
                finder.exclude_module(exclude)
        finder.exclude_module("sklearn._build_utils")
        finder.exclude_module("sklearn.utils._testing")
        with suppress(ImportError):
            finder.include_module("sklearn._cyutility")  # v1.7.1

    def sklearn__distributor_init(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Fix the location of dependent files in Windows."""
        loader = module.loader
        source_code = loader.get_source(module.name)
        if "msvcp140.dll" in source_code:
            # msvcp140 and vcomp140 dlls should be copied
            # but in cx_Freeze, include_msvcr do the work
            module.code = loader.source_to_code(
                "", loader.get_filename(module.name), _optimize=finder.optimize
            )

    def sklearn_externals_array_api_compat_numpy(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Loads an extension module."""
        finder.include_package("sklearn.externals.array_api_compat.numpy.fft")

    def sklearn_utils(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.ignore_names.update(["matplotlib", "pandas"])

    def sklearn_utils__estimator_html_repr(
        self,
        finder: ModuleFinder,
        module: Module,
    ) -> None:
        # copy css file and patch the code to locate css file # v1.4.x to 1.6.x
        if module.in_file_system == 0:
            source = module.file.with_suffix(".css")
            if source.is_file():
                target_dir = module.parent.name.replace(".", "/")
                finder.include_files(source, f"lib/{target_dir}/{source.name}")
                loader = module.loader
                path = loader.get_filename(module.name)
                source_code = loader.get_source(module.name)
                module.code = loader.source_to_code(
                    source_code.replace(
                        "__file__", "__file__.replace('library.zip', '.')"
                    ),
                    path,
                    _optimize=finder.optimize,
                )

    def sklearn_utils__mask(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.ignore_names.update(["pandas"])

    def sklearn_utils__param_validation(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.ignore_names.update(["pandas"])

    def sklearn_utils__repr_html(
        self,
        finder: ModuleFinder,
        module: Module,
    ) -> None:
        # copy js/css files # v 1.7.0
        if module.in_file_system == 0:
            target_dir = module.name.replace(".", "/")
            for source in module.file.parent.glob("*.css"):
                finder.include_files(source, f"lib/{target_dir}/{source.name}")
            for source in module.file.parent.glob("*.js"):
                finder.include_files(source, f"lib/{target_dir}/{source.name}")

    def sklearn_utils__repr_html_estimator(
        self,
        finder: ModuleFinder,
        module: Module,
    ) -> None:
        # patch the code to locate css/js files # v 1.7.0
        if module.in_file_system == 0:
            loader = module.loader
            path = loader.get_filename(module.name)
            source_code = loader.get_source(module.name)
            module.code = loader.source_to_code(
                source_code.replace(
                    "__file__", "__file__.replace('library.zip', '.')"
                ),
                path,
                _optimize=finder.optimize,
            )

    def sklearn_utils_validation(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.ignore_names.update(["pandas.api.types"])
