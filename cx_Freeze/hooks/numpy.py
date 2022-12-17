"""A collection of functions which are triggered automatically by finder when
numpy package is included."""
# pylint: disable=unused-argument

from __future__ import annotations

import os
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path

from .._compat import IS_MINGW, IS_WINDOWS
from ..finder import ModuleFinder
from ..module import Module


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy must be loaded as a package; support for pypi version and
    numpy+mkl version - tested with 1.19.5+mkl, 1.20.3+mkl, 1.21.0+mkl,
    1.21.1+mkl, 1.21.2+mkl and 1.21.2 from conda-forge."""
    finder.include_package("numpy")

    if IS_WINDOWS or IS_MINGW:
        numpy_dir = module.path[0]
        # numpy+mkl from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
        libs_dir = numpy_dir / "DLLs"
        if not libs_dir.is_dir():
            # numpy+mkl from conda-forge
            libs_dir = Path(sys.base_prefix, "Library", "bin")
        if libs_dir.is_dir():
            dest_dir = Path("lib", "numpy_mkl")
            for path in libs_dir.glob("mkl_*.dll"):
                finder.include_files(path, dest_dir / path.name)
            for path in libs_dir.glob("lib*.dll"):
                finder.include_files(path, dest_dir / path.name)
            finder.add_constant("MKL_PATH", os.fspath(dest_dir))
            finder.exclude_module("numpy.DLLs")

            # do not check dependencies already handled
            extension = EXTENSION_SUFFIXES[0]
            for path in numpy_dir.rglob(f"*{extension}"):
                finder.exclude_dependent_files(path)

        # support for old versions (numpy <= 1.18.2)
        if module.in_file_system == 0:
            # copy any file at site-packages/numpy/.libs
            libs_dir = numpy_dir / ".libs"
            if libs_dir.is_dir():
                finder.include_files(libs_dir, "lib")

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


def load_numpy_core_numerictypes(finder: ModuleFinder, module: Module) -> None:
    """The numpy.core.numerictypes module adds a number of items to itself
    dynamically; define these to avoid spurious errors about missing
    modules."""
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
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("numscons")


def load_numpy_distutils_misc_util(
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("numscons")


def load_numpy_distutils_system_info(
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("Numeric")


def load_numpy_f2py___version__(finder: ModuleFinder, module: Module) -> None:
    """The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("__svn_version__")


def load_numpy_linalg(finder: ModuleFinder, module: Module) -> None:
    """The numpy.linalg module implicitly loads the lapack_lite module; make
    sure this happens."""
    finder.include_module("numpy.linalg.lapack_lite")


def load_numpy_random_mtrand(finder: ModuleFinder, module: Module) -> None:
    """The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules."""
    module.global_names.update(["rand", "randn"])
