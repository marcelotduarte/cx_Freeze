"""A collection of functions which are triggered automatically by finder when
scipy package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MINGW, IS_WINDOWS
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
            files = distribution.original.files or []
            for file in files:
                if file.parent.match("**/tests"):
                    mod = file.parent.as_posix().replace("/", ".")
                    finder.exclude_module(mod)
        finder.exclude_module("scipy.conftest")

        finder.include_package("scipy.integrate")
        finder.include_package("scipy._lib")
        finder.include_package("scipy.misc")
        finder.include_package("scipy.optimize")
        with suppress(ImportError):
            finder.include_module("scipy._cyutility")  # v1.16.0

    def scipy__distributor_init(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Fix the location of dependent files in Windows and macOS."""
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

    def scipy_interpolate(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.interpolate must be loaded as a package."""
        finder.exclude_module("scipy.interpolate.tests")
        finder.include_package("scipy.interpolate")

    def scipy_linalg(self, finder: ModuleFinder, module: Module) -> None:
        """The scipy.linalg module loads items within itself in a way that
        causes problems without the entire package being present.
        """
        module.global_names.add("norm")
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
        finder.exclude_module("scipy.ndimage.tests")
        finder.include_package("scipy.ndimage")

    def scipy_sparse(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.sparse must be loaded as a package."""
        finder.exclude_module("scipy.sparse.tests")
        finder.include_package("scipy.sparse")

    def scipy_sparse_csgraph(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.sparse.csgraph must be loaded as a package."""
        finder.exclude_module("scipy.sparse.csgraph.tests")
        finder.include_package("scipy.sparse.csgraph")

    def scipy_sparse_linalg__dsolve_linsolve(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """The scipy.sparse.linalg._dsolve.linsolve optionally loads
        scikits.umfpack.
        """
        module.ignore_names.add("scikits.umfpack")

    def scipy_spatial(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.spatial must be loaded as a package."""
        finder.include_package("scipy.spatial")
        finder.exclude_module("scipy.spatial.tests")
        if IS_WINDOWS or IS_MINGW:
            finder.exclude_module("scipy.spatial.cKDTree")

    def scipy_spatial_transform(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.spatial.transform must be loaded as a package."""
        finder.include_package("scipy.spatial.transform")
        finder.exclude_module("scipy.spatial.transform.tests")

    def scipy_special(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.special must be loaded as a package."""
        finder.exclude_module("scipy.special.tests")
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

    def scipy_stats(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The scipy.stats must be loaded as a package."""
        finder.exclude_module("scipy.stats.tests")
        finder.include_package("scipy.stats")
