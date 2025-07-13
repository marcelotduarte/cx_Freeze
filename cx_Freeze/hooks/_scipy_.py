"""A collection of functions which are triggered automatically by finder when
scipy package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import (
    SCIPY__LIB_ARRAY_API_COMPAT_GLOBAL_NAMES,
    SCIPY_INTEGRATE_GLOBAL_NAMES,
    SCIPY_INTERPOLATE_GLOBAL_NAMES,
    SCIPY_LINALG_GLOBAL_NAMES,
    SCIPY_OPTIMIZE_GLOBAL_NAMES,
    SCIPY_SPARSE_GLOBAL_NAMES,
    SCIPY_SPARSE_LINALG_GLOBAL_NAMES,
    SCIPY_SPATIAL_GLOBAL_NAMES,
    SCIPY_SPECIAL_GLOBAL_NAMES,
    SCIPY_STATS_GLOBAL_NAMES,
)
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for scipy."""

    def scipy(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy package.

        Supported pypi and conda-forge versions (tested until 1.16.0).
        """
        # Exclude unnecessary modules
        distribution = module.distribution
        if distribution:
            # Exclude tests
            excludes = set()
            files = distribution.original.files or []
            for file in files:
                if file.parent.match("**/tests"):
                    excludes.add(file.parent.as_posix().replace("/", "."))
            # >>> excludes.discard("scipy.special.tests")
            for exclude in excludes:
                finder.exclude_module(exclude)
        finder.exclude_module("scipy.conftest")

        finder.include_package("scipy._lib")
        finder.include_package("scipy.misc")
        with suppress(ImportError):
            finder.include_module("scipy._cyutility")  # v1.16.0

    def scipy__distributor_init(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Fix the location of dependent files in Windows and macOS."""
        module.ignore_names.add("scipy._distributor_init_local")
        if IS_LINUX or IS_MINGW:
            return  # it is detected correctly.

        # patch the code when necessary
        if module.in_file_system == 0:
            module.code = compile(
                module.file.read_bytes().replace(
                    b"__file__", b"__file__.replace('library.zip', '.')"
                ),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )

    def scipy_integrate(self, finder: ModuleFinder, module: Module) -> None:
        """Set the module global names."""
        module.global_names.update(SCIPY_INTEGRATE_GLOBAL_NAMES)
        finder.include_package("scipy.integrate")

    def scipy_interpolate(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.interpolate must be loaded as a package."""
        module.global_names.update(SCIPY_INTERPOLATE_GLOBAL_NAMES)
        finder.include_package("scipy.interpolate")

    def scipy__lib_array_api_compat(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """Set the module global names."""
        module.global_names.update(SCIPY__LIB_ARRAY_API_COMPAT_GLOBAL_NAMES)

    def scipy__lib__docscrape(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.exclude_names.update(["sphinx.ext.autodoc"])

    def scipy__lib__testutils(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.exclude_names.update(
            ["Cython.Compiler.Version", "cython", "psutil", "pytest"]
        )

    def scipy_linalg(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.linalg module loads items within itself in a way that
        causes problems without the entire package being present.
        """
        module.global_names.update(SCIPY_LINALG_GLOBAL_NAMES)
        finder.include_package("scipy.linalg")

    def scipy_linalg_interface_gen(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The scipy.linalg.interface_gen module optionally imports the pre
        module; ignore the error if this module cannot be found.
        """
        module.ignore_names.add("pre")

    def scipy_ndimage(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.ndimage must be loaded as a package."""
        finder.include_package("scipy.ndimage")

    def scipy_optimize(self, finder: ModuleFinder, module: Module) -> None:
        """Set the module global names."""
        module.global_names.update(SCIPY_OPTIMIZE_GLOBAL_NAMES)
        finder.include_package("scipy.optimize")

    def scipy_optimize__constraints(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        self._fix_suppress_warnings(finder, module)

    def scipy_sparse(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.sparse must be loaded as a package."""
        module.global_names.update(SCIPY_SPARSE_GLOBAL_NAMES)
        finder.include_package("scipy.sparse")

    def scipy_sparse_csgraph(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.sparse.csgraph must be loaded as a package."""
        finder.include_package("scipy.sparse.csgraph")

    def scipy_sparse_linalg(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Set the module global names."""
        module.global_names.update(SCIPY_SPARSE_LINALG_GLOBAL_NAMES)

    def scipy_sparse_linalg__dsolve_linsolve(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """The scipy.sparse.linalg._dsolve.linsolve optionally loads
        scikits.umfpack.
        """
        module.ignore_names.add("scikits.umfpack")

    def scipy_spatial(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.spatial must be loaded as a package."""
        module.global_names.update(SCIPY_SPATIAL_GLOBAL_NAMES)
        finder.include_package("scipy.spatial")
        if IS_WINDOWS or IS_MINGW:
            finder.exclude_module("scipy.spatial.cKDTree")

    def scipy_spatial_transform(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.spatial.transform must be loaded as a package."""
        finder.include_package("scipy.spatial.transform")

    def scipy_special(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.special must be loaded as a package."""
        module.global_names.update(SCIPY_SPECIAL_GLOBAL_NAMES)
        finder.include_package("scipy.special")
        finder.include_package("scipy.special._precompute")

    def scipy_special__cephes(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """The scipy.special._cephes is an extension module and the scipy
        module imports * from it in places; advertise the global names that
        are used in order to avoid spurious errors about missing modules.
        """
        module.global_names.add("gammaln")

    def scipy_special__mptestutils(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.exclude_names.add("pytest")

    def scipy_special__testutils(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        module.exclude_names.add("pytest")

    def scipy_stats(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.stats must be loaded as a package."""
        module.global_names.update(SCIPY_STATS_GLOBAL_NAMES)
        finder.include_package("scipy.stats")

    def scipy_stats__binned_statistic(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        self._fix_suppress_warnings(finder, module)

    def scipy_stats__stats_py(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        self._fix_suppress_warnings(finder, module)

    def scipy_stats__sobol(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        finder.include_package("importlib.resources")

    def _fix_suppress_warnings(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        code_bytes = module.file.read_bytes()
        if b"suppress_warnings" in code_bytes:
            code_bytes = code_bytes.replace(
                b"from numpy.testing import suppress_warnings",
                b"from warnings import catch_warnings as suppress_warnings",
            )
            module.code = compile(
                code_bytes,
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )
