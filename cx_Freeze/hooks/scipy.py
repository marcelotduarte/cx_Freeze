"""A collection of functions which are triggered automatically by finder when
scipy package is included.
"""

from __future__ import annotations

import os

from .._compat import IS_MINGW, IS_WINDOWS
from ..finder import ModuleFinder
from ..module import Module
from ._libs import replace_delvewheel_patch


def load_scipy(finder: ModuleFinder, module: Module) -> None:
    """The scipy module loads items within itself in a way that causes
    problems without libs and a number of subpackages being present.
    """
    source_dir = module.file.parent.parent / f"{module.name}.libs"
    if source_dir.exists():
        finder.include_files(source_dir, f"lib/{source_dir.name}")
    replace_delvewheel_patch(module)
    finder.include_package("scipy.integrate")
    finder.include_package("scipy._lib")
    finder.include_package("scipy.misc")
    finder.include_package("scipy.optimize")


def load_scipy__distributor_init(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """Fix the location of dependent files in Windows."""
    if not (IS_WINDOWS or IS_MINGW):
        # In Linux and macOS it is detected correctly.
        return

    if module.in_file_system != 0:  # not in zip_include_packages
        return

    # patch the code
    code_string = module.file.read_text(encoding="utf-8").replace(
        "__file__", "__file__.replace('library.zip/', '')"
    )
    module.code = compile(code_string, os.fspath(module.file), "exec")


def load_scipy_interpolate(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.interpolate must be loaded as a package."""
    finder.exclude_module("scipy.interpolate.tests")
    finder.include_package("scipy.interpolate")


def load_scipy_linalg(finder: ModuleFinder, module: Module) -> None:
    """The scipy.linalg module loads items within itself in a way that causes
    problems without the entire package being present.
    """
    module.global_names.add("norm")
    finder.include_package("scipy.linalg")


def load_scipy_linalg_interface_gen(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.linalg.interface_gen module optionally imports the pre module;
    ignore the error if this module cannot be found.
    """
    module.ignore_names.add("pre")


def load_scipy_ndimage(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.ndimage must be loaded as a package."""
    finder.exclude_module("scipy.ndimage.tests")
    finder.include_package("scipy.ndimage")


def load_scipy_sparse(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.sparse must be loaded as a package."""
    finder.exclude_module("scipy.sparse.tests")
    finder.include_package("scipy.sparse")


def load_scipy_sparse_csgraph(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.sparse.csgraph must be loaded as a package."""
    finder.exclude_module("scipy.sparse.csgraph.tests")
    finder.include_package("scipy.sparse.csgraph")


def load_scipy_sparse_linalg__dsolve_linsolve(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.sparse.linalg._dsolve.linsolve optionally loads
    scikits.umfpack.
    """
    module.ignore_names.add("scikits.umfpack")


def load_scipy_spatial(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.spatial must be loaded as a package."""
    finder.include_package("scipy.spatial")
    finder.exclude_module("scipy.spatial.tests")
    if IS_WINDOWS or IS_MINGW:
        finder.exclude_module("scipy.spatial.cKDTree")


def load_scipy_spatial_transform(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.spatial.transform must be loaded as a package."""
    finder.include_package("scipy.spatial.transform")
    finder.exclude_module("scipy.spatial.transform.tests")


def load_scipy_special(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.special must be loaded as a package."""
    finder.exclude_module("scipy.special.tests")
    finder.include_package("scipy.special")
    finder.include_package("scipy.special._precompute")


def load_scipy_special__cephes(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.special._cephes is an extension module and the scipy module
    imports * from it in places; advertise the global names that are used
    in order to avoid spurious errors about missing modules.
    """
    module.global_names.add("gammaln")


def load_scipy_stats(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The scipy.stats must be loaded as a package."""
    finder.include_package("scipy.stats")
    finder.exclude_module("scipy.stats.tests")
