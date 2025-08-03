"""A collection of functions which are triggered automatically by finder when
numpy package is included.
"""

from __future__ import annotations

import json
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import (
    NUMPY__CORE_GLOBAL_NAMES,
    NUMPY__CORE_NUMERICTYPES_GLOBAL_NAMES,
    NUMPY_LINALG_GLOBAL_NAMES,
    NUMPY_MA_GLOBAL_NAMES,
    NUMPY_RANDOM_GLOBAL_NAMES,
    NUMPY_RANDOM_MTRAND_GLOBAL_NAMES,
    NUMPY_STRINGS_GLOBAL_NAMES,
)
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


# The sample/pandas is used to test.
# Using pip (pip install numpy) in Windows/Linux/macOS from pypi (w/ OpenBLAS)
#
# Also, using: https://github.com/cgohlke/numpy-mkl-wheels/releases/
#
# Read the numpy documentation, especially if using conda-forge and MKL:
# https://numpy.org/install/#numpy-packages--accelerated-linear-algebra-libraries
#
# For conda-forge we can use the default or switch BLAS implementation:
# https://conda-forge.org/docs/maintainer/knowledge_base/#switching-blas-implementation
# conda install "libblas=*=*mkl" numpy
# conda install "libblas=*=*openblas" numpy


class Hook(ModuleHook):
    """The Hook class for numpy."""

    def numpy(self, finder: ModuleFinder, module: Module) -> None:
        """The numpy package.

        Supported pypi and conda-forge versions (tested from 1.21.2 to 2.3.1).
        """
        # Exclude unnecessary modules
        finder.exclude_module("numpy._configtool")
        finder.exclude_module("numpy.conftest")
        finder.exclude_module("numpy.distutils")
        finder.exclude_module("numpy.f2py")
        finder.exclude_module("numpy._pyinstaller")
        finder.exclude_module("numpy.random._examples")
        finder.exclude_module("numpy.testing")
        finder.exclude_module("numpy.typing.mypy_plugin")
        module.ignore_names.add("numpy.distutils")

        # Exclude/Include modules based on distribution and/or version
        distribution = module.distribution
        if distribution:
            # Exclude tests
            excludes = set()
            files = distribution.original.files or []
            for file in files:
                if file.parent.match("**/tests"):
                    excludes.add(file.parent.as_posix().replace("/", "."))
            excludes.discard("numpy._core.tests")
            for exclude in excludes:
                finder.exclude_module(exclude)

            # Include dynamically loaded module / exclude unnecessary modules
            if distribution.version >= (2, 0):
                finder.exclude_module("numpy._core.include")
                finder.exclude_module("numpy._core.lib")
                finder.exclude_module("numpy.compat")
                finder.include_package("numpy._core._exceptions")
                finder.include_package("numpy._core._dtype_ctypes")
                finder.include_package("numpy._core._methods")
                finder.include_package("numpy._core._multiarray_tests")
                finder.include_package("numpy._expired_attrs_2_0")
            else:
                finder.exclude_module("numpy.core.include")
                finder.exclude_module("numpy.core.lib")
                finder.include_package("numpy.core._exceptions")
                finder.include_package("numpy.core._dtype_ctypes")
                finder.include_package("numpy.core._methods")
                finder.include_package("numpy.core._multiarray_tests")
        else:
            finder.include_package("numpy.core")

        # Include dynamically loaded module
        finder.include_module("numpy.lib.format")
        finder.include_module("numpy.polynomial")
        finder.include_module("secrets")

        code_bytes = module.file.read_bytes()
        if module.in_file_system == 0:
            code_bytes = code_bytes.replace(
                b"__file__", b"__file__.replace('library.zip', '.')"
            )
        code_bytes = code_bytes.replace(
            b"import numpy.f2py as f2py", b"f2py = None"
        )
        code_bytes = code_bytes.replace(
            b"import numpy.testing as testing", b"testing = None"
        )
        module.code = compile(
            code_bytes,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )

    def numpy_compat(self, _finder: ModuleFinder, module: Module) -> None:
        # deprecated since 1.26.0, available until 2.2.6, removed in 2.3.0
        module.global_names.update(
            [
                "Path",
                "asbytes",
                "asbytes_nested",
                "asstr",
                "asunicode",
                "asunicode_nested",
                "basestring",
                "bytes",
                "contextlib_nullcontext",
                "getexception",
                "integer_types",
                "is_pathlib_path",
                "isfileobj",
                "long",
                "npy_load_module",
                "open_latin1",
                "os_PathLike",
                "os_fspath",
                "pickle",
                "sixu",
                "strchar",
                "unicode",
            ]
        )

    def numpy_compat_py3k(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore errors if optionally imported module cannot be found."""
        module.ignore_names.add("pickle5")

    def numpy___config__(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore errors if optionally imported module cannot be found."""
        module.ignore_names.add("yaml")

    def numpy_core(self, _finder: ModuleFinder, module: Module) -> None:
        """Set the numpy.core global names (numpy < 2.0)."""
        module.global_names.update(NUMPY__CORE_GLOBAL_NAMES)
        module.global_names.add("geterrobj")
        module.global_names.add("Inf")

    def numpy__core(self, _finder: ModuleFinder, module: Module) -> None:
        """Set the numpy._core global names (numpy >= 2.0)."""
        module.global_names.update(NUMPY__CORE_GLOBAL_NAMES)

    def numpy__core_numerictypes(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The numpy._core.numerictypes module adds a number of items to itself
        dynamically; define these to avoid spurious errors about missing
        modules.
        """
        module.global_names.update(NUMPY__CORE_NUMERICTYPES_GLOBAL_NAMES)

    numpy_core_numerictypes = numpy__core_numerictypes  # numpy < 2.0

    def numpy__core_overrides(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Recompile the numpy._core.overrides module to workaround an
        optimization that removes docstrings, which are required for this
        module.
        """
        module.code = compile(
            module.file.read_bytes().replace(
                b"dispatcher.__doc__", b"dispatcher.__doc__ or ''"
            ),
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )

    numpy_core_overrides = numpy__core_overrides  # numpy < 2.0

    def numpy__distributor_init(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Fix the location of dependent files in all OS."""
        module.ignore_names.add("numpy._distributor_init_local")
        # check versions that are handled correctly
        if IS_MINGW:
            return
        distribution = module.parent.distribution
        if distribution is None or (
            IS_LINUX and distribution.installer == "pip"
        ):
            return

        # patch the code when necessary
        code_bytes = module.file.read_bytes()

        module_dir = module.file.parent
        exclude_dependent_files = False
        if distribution.installer == "pip":
            # cgohlke/numpy-mkl.whl, numpy 1.23.5+mkl (Windows)
            libs_dir = module_dir / "DLLs"
            if libs_dir.is_dir():
                finder.exclude_module("numpy.DLLs")
                finder.include_files(
                    libs_dir, "lib/numpy/DLLs", copy_dependent_files=False
                )
                exclude_dependent_files = True

            # cgohlke/numpy-mkl-wheels, numpy 1.26.3 and mkl
            if b"def init_numpy_mkl():" in code_bytes:
                code_bytes = code_bytes.replace(
                    b"path = ", b"path = f'{sys.prefix}\\lib\\mkl'  # "
                )
                # create a fake module to activate mkl hook
                mkl_path = finder.cache_path.joinpath("mkl")
                mkl_path.touch()
                finder.include_file_as_module(mkl_path)
                exclude_dependent_files = True

        elif distribution.installer == "conda":
            prefix = Path(sys.prefix)
            conda_meta = prefix / "conda-meta"
            packages = [
                "libblas",
                "libcblas",
                "liblapack",
                "intel-openmp",
                "llvm-openmp",
            ]
            blas_options = ["libopenblas", "mkl"]
            packages += blas_options
            for package in packages:
                pkg = next(conda_meta.glob(f"{package}-*.json"), None)
                if pkg is None:
                    continue
                files = json.loads(pkg.read_text(encoding="utf_8"))["files"]
                # copy mkl/blas files to lib (issue #2574)
                if IS_WINDOWS:
                    for file in files:
                        source = prefix.joinpath(file).resolve()
                        if not source.match("*.dll"):
                            continue
                        target = f"lib/{source.name}"
                        finder.include_files(
                            source, target, copy_dependent_files=False
                        )
                else:
                    extensions = tuple(
                        [ext for ext in EXTENSION_SUFFIXES if ext != ".so"]
                    )
                    for file in files:
                        if file.endswith(extensions):
                            continue
                        source = prefix.joinpath(file)
                        if not source.match("*.so*"):
                            continue
                        if source.is_symlink():
                            target = f"lib/{source.name}"
                            finder.include_files(
                                source, target, copy_dependent_files=False
                            )
                            source = source.resolve()
                        target = f"lib/{source.name}"
                        finder.lib_files[source] = target

        # do not check dependencies already handled
        if exclude_dependent_files:
            extension = EXTENSION_SUFFIXES[0]
            for file in module_dir.rglob(f"*{extension}"):
                finder.exclude_dependent_files(file)

        if module.in_file_system == 0:
            code_bytes = code_bytes.replace(
                b"__file__", b"__file__.replace('library.zip', '.')"
            )
        module.code = compile(
            code_bytes,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )

    def numpy_lib_utils(
        self, _finder: ModuleFinder, module: Module
    ) -> None:  # numpy<2
        """The module numpy.lib.utils optionally imports the threadpoolctl
        module; ignore the error if the module cannot be found.
        """
        module.ignore_names.add("threadpoolctl")

    def numpy_lib__utils_impl(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The module numpy.lib._utils_impl optionally imports the
        threadpoolctl module; ignore the error if the module cannot be found.
        """
        module.ignore_names.add("threadpoolctl")

    def numpy_linalg(self, finder: ModuleFinder, module: Module) -> None:
        """The numpy.linalg module implicitly loads the lapack_lite module;
        make sure this happens.
        """
        module.global_names.update(NUMPY_LINALG_GLOBAL_NAMES)
        finder.include_module("numpy.linalg.lapack_lite")
        finder.include_module("numpy.linalg._umath_linalg")

    def numpy_ma(self, _finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(NUMPY_MA_GLOBAL_NAMES)

    def numpy__pytesttester(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Remove optional modules in the numpy._pytesttester module."""
        module.exclude_names.update(
            ["numpy.distutils", "numpy.testing", "pytest"]
        )
        module.ignore_names.update(
            ["numpy.distutils", "numpy.testing", "pytest"]
        )

    def numpy_random(self, _finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(NUMPY_RANDOM_GLOBAL_NAMES)

    def numpy_random_mtrand(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """The numpy.random.mtrand module is an extension module and the numpy
        module imports * from this module; define the list of global names
        available to this module in order to avoid spurious errors about
        missing modules.
        """
        module.global_names.update(NUMPY_RANDOM_MTRAND_GLOBAL_NAMES)

    def numpy_strings(self, _finder: ModuleFinder, module: Module) -> None:
        """Define the global names to avoid spurious missing modules."""
        module.global_names.update(NUMPY_STRINGS_GLOBAL_NAMES)

    def numpy__typing(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional module."""
        module.ignore_names.add("numpy._typing._ufunc")
