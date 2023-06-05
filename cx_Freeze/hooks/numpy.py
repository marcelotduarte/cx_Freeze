"""A collection of functions which are triggered automatically by finder when
numpy package is included.
"""


from __future__ import annotations

import json
import os
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from textwrap import dedent

from .._compat import IS_CONDA, IS_MINGW, IS_WINDOWS
from ..finder import ModuleFinder
from ..module import Module

# The sample/pandas is used to test.
# Using pip (pip install numpy) in Windows/Linux/macOS from pypi (w/ OpenBLAS)
# And using cgohlke/numpy-mkl.whl, numpy 1.23.5+mkl in windows:
# https://github.com/cgohlke/numpy-mkl.whl/releases/download/v2023.1.4/numpy-1.23.5+mkl-cp311-cp311-win_amd64.whl
#
# Read the numpy documentation, especially if using conda-forge and MKL:
# https://numpy.org/install/#numpy-packages--accelerated-linear-algebra-libraries
#
# For conda-forge we can use the default installation with MKL:
# conda install -c conda-forge numpy
# Or use OpenBLAS:
# conda install -c conda-forge blas=*=openblas numpy


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy must be loaded as a package.

    Supported pypi and conda-forge versions (tested from 1.21.2 to 1.24.3).
    """
    finder.include_package("numpy")
    module.in_file_system = 1  # TODO: support zip or optimized mode
    # exclude the tests
    finder.exclude_module("numpy.compat.tests")
    finder.exclude_module("numpy.core.tests")
    finder.exclude_module("numpy.distutils.tests")
    finder.exclude_module("numpy.f2py.tests")
    finder.exclude_module("numpy.fft.tests")
    finder.exclude_module("numpy.lib.tests")
    finder.exclude_module("numpy.linalg.tests")
    finder.exclude_module("numpy.ma.tests")
    finder.exclude_module("numpy.matrixlib.tests")
    finder.exclude_module("numpy.polynomial.tests")
    finder.exclude_module("numpy.random._examples")
    finder.exclude_module("numpy.random.tests")
    finder.exclude_module("numpy.tests")
    finder.exclude_module("numpy.typing.tests")


def load_numpy__distributor_init(finder: ModuleFinder, module: Module) -> None:
    """Fix the location of dependent files in Windows."""
    if not (IS_WINDOWS or IS_MINGW):
        # In Linux and macOS it is detected correctly.
        return

    # patch the code when necessary
    code_string = module.file.read_text(encoding="utf-8")

    # installed from pypi, using zip_include_packages we must fix it
    numpy_dir = module.file.parent
    libs_dir = numpy_dir / ".libs"
    if libs_dir.is_dir():
        if module.in_file_system == 0:  # zip_include_packages
            # copy any file at site-packages/numpy/.libs
            finder.include_files(libs_dir, "lib/numpy/.libs")
    else:
        # cgohlke/numpy-mkl.whl, numpy 1.23.5+mkl
        libs_dir = numpy_dir / "DLLs"
        if libs_dir.is_dir():
            finder.exclude_module("numpy.DLLs")
            finder.include_files(libs_dir, "lib/numpy/DLLs")
        # conda-forge
        elif IS_CONDA:
            prefix = Path(sys.prefix)
            conda_meta = prefix / "conda-meta"
            packages = ["libblas", "libcblas", "liblapack"]
            blas_options = ["libopenblas", "mkl"]
            packages += blas_options
            files_to_copy: list[Path] = []
            for package in packages:
                try:
                    pkg = next(conda_meta.glob(f"{package}-*.json"))
                except StopIteration:
                    continue
                files = json.loads(pkg.read_text(encoding="utf-8"))["files"]
                files_to_copy += [
                    prefix / file
                    for file in files
                    if file.lower().endswith(".dll")
                ]
                blas = package
            for source in files_to_copy:
                finder.include_files(source, f"lib/{blas}/{source.name}")
            numpy_blas = f"""
            def init_numpy_blas():
                import os

                blas_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), "{blas}"
                )
                try:
                    os.add_dll_directory(blas_path)
                except (OSError, AttributeError):
                    pass
                env_path = os.environ.get("PATH", "").split(os.pathsep)
                if blas_path not in env_path:
                    env_path.insert(0, blas_path)
                    os.environ["PATH"] = os.pathsep.join(env_path)

            init_numpy_blas()
            """
            code_string += dedent(numpy_blas)

    # do not check dependencies already handled
    extension = EXTENSION_SUFFIXES[0]
    for file in numpy_dir.rglob(f"*{extension}"):
        finder.exclude_dependent_files(file)

    if module.in_file_system == 0:
        code_string = code_string.replace(
            "__file__", "__file__.replace('library.zip/', '')"
        )
    module.code = compile(code_string, os.fspath(module.file), "exec")


def load_numpy_core_numerictypes(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.core.numerictypes module adds a number of items to itself
    dynamically; define these to avoid spurious errors about missing
    modules.
    """
    module.global_names.update(
        [
            "bool_",
            "cdouble",
            "complexfloating",
            "csingle",
            "double",
            "float64",
            "float_",
            "inexact",
            "intc",
            "int32",
            "number",
            "single",
        ]
    )


def load_numpy_distutils_command_scons(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_misc_util(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_system_info(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("Numeric")


def load_numpy_f2py___version__(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("__svn_version__")


def load_numpy_linalg(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.linalg module implicitly loads the lapack_lite module; make
    sure this happens.
    """
    finder.include_module("numpy.linalg.lapack_lite")


def load_numpy_random_mtrand(
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules.
    """
    module.global_names.update(["rand", "randn"])
