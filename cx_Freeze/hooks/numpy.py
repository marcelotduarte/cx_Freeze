"""A collection of functions which are triggered automatically by finder when
numpy package is included.
"""

from __future__ import annotations

import json
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks._libs import replace_delvewheel_patch

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

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


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy package.

    Supported pypi and conda-forge versions (tested from 1.21.2 to 2.0.0).
    """
    source_dir = module.file.parent.parent / f"{module.name}.libs"
    if source_dir.exists():  # numpy >= 1.26.0
        finder.include_files(source_dir, f"lib/{source_dir.name}")
        replace_delvewheel_patch(module)

    distribution = module.distribution

    # Exclude all tests
    if distribution:
        tests = set()
        for file in distribution.original.files:
            if file.parent.match("**/tests"):
                tests.add(file.parent.as_posix().replace("/", "."))
        for test in tests:
            finder.exclude_module(test)

        # Include dynamically loaded module / exclude unnecessary modules
        if distribution.version >= (2, 0):
            finder.include_package("numpy._core._exceptions")
            finder.include_package("numpy._core._dtype_ctypes")
            finder.include_package("numpy._core._methods")
            finder.include_package("numpy._core._multiarray_tests")
            finder.exclude_module("numpy._core.include")
            finder.exclude_module("numpy._core.lib")
        else:
            finder.include_package("numpy.core._exceptions")
            finder.include_package("numpy.core._dtype_ctypes")
            finder.include_package("numpy.core._methods")
            finder.include_package("numpy.core._multiarray_tests")
            finder.exclude_module("numpy.core.include")
            finder.exclude_module("numpy.core.lib")
    else:
        finder.include_package("numpy.core")

    # Exclude unnecessary modules
    finder.exclude_module("numpy.conftest")
    finder.exclude_module("numpy.distutils")
    finder.exclude_module("numpy._pyinstaller")
    finder.exclude_module("numpy.random._examples")

    # Include dynamically loaded module
    finder.include_module("numpy.lib.format")
    finder.include_module("numpy.polynomial")
    finder.include_module("secrets")


def load_numpy__core_overrides(finder: ModuleFinder, module: Module) -> None:
    """Recompile the numpy._core.overrides module to workaround optimization
    that removes docstrings, which are required for this module.
    """
    code_string = module.file.read_text(encoding="utf_8")
    module.code = compile(
        code_string.replace("dispatcher.__doc__", "dispatcher.__doc__ or ''"),
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


load_numpy_core_overrides = load_numpy__core_overrides  # numpy < 2.0


def load_numpy__distributor_init(finder: ModuleFinder, module: Module) -> None:
    """Fix the location of dependent files in all OS."""
    # check versions that are handled correctly
    if IS_MINGW:
        return
    distribution = module.parent.distribution
    if distribution is None or (IS_LINUX and distribution.installer == "pip"):
        return

    # patch the code when necessary
    code_string = module.file.read_text(encoding="utf_8")

    module_dir = module.file.parent
    exclude_dependent_files = False
    if distribution.installer == "pip":
        # numpy < 1.26.0 - macOS or Windows
        libs_dir = module_dir.joinpath(".dylibs" if IS_MACOS else ".libs")
        if libs_dir.is_dir():
            # copy any file at site-packages/numpy/.libs
            target_dir = f"lib/numpy/{libs_dir.name}"
            finder.include_files(
                libs_dir, target_dir, copy_dependent_files=False
            )
            exclude_dependent_files = True

        # cgohlke/numpy-mkl.whl, numpy 1.23.5+mkl (Windows)
        libs_dir = module_dir / "DLLs"
        if libs_dir.is_dir():
            finder.exclude_module("numpy.DLLs")
            finder.include_files(
                libs_dir, "lib/numpy/DLLs", copy_dependent_files=False
            )
            exclude_dependent_files = True

        # cgohlke/numpy-mkl-wheels, numpy 1.26.3 and mkl
        if "def init_numpy_mkl():" in code_string:
            code_string = code_string.replace(
                "path = ", "path = f'{sys.frozen_dir}\\lib\\mkl'  # "
            )
            # create a fake module to activate mkl hook
            mkl_path = finder.cache_path.joinpath("mkl")
            mkl_path.touch()
            finder.include_file_as_module(mkl_path)
            exclude_dependent_files = True

    elif distribution.installer == "conda":
        prefix = Path(sys.prefix)
        conda_meta = prefix / "conda-meta"
        packages = ["libblas", "libcblas", "liblapack", "llvm-openmp"]
        blas_options = ["libopenblas", "mkl"]
        packages += blas_options
        files_to_copy: list[Path] = []
        blas = None
        for package in packages:
            try:
                pkg = next(conda_meta.glob(f"{package}-*.json"))
            except StopIteration:
                continue
            files = json.loads(pkg.read_text(encoding="utf_8"))["files"]
            if IS_WINDOWS:
                files_to_copy += [
                    prefix / file
                    for file in files
                    if file.lower().endswith(".dll")
                ]
            else:
                extensions = tuple(
                    [ext for ext in EXTENSION_SUFFIXES if ext != ".so"]
                )
                for file in files:
                    if file.endswith(extensions):
                        continue
                    source = prefix.joinpath(file).resolve()
                    if not source.match("*.so*"):
                        continue
                    target = f"lib/{source.name}"
                    finder.include_files(
                        source, target, copy_dependent_files=False
                    )
            blas = package
        if IS_WINDOWS:
            for source in files_to_copy:
                finder.include_files(
                    source,
                    f"lib/{blas}/{source.name}",
                    copy_dependent_files=False,
                )
            exclude_dependent_files = True
            code_string += dedent(
                f"""
                def _init_numpy_blas():
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

                _init_numpy_blas()
                """
            )

    # do not check dependencies already handled
    if exclude_dependent_files:
        extension = EXTENSION_SUFFIXES[0]
        for file in module_dir.rglob(f"*{extension}"):
            finder.exclude_dependent_files(file)

    if module.in_file_system == 0:
        code_string = code_string.replace(
            "__file__", "__file__.replace('library.zip/', '')"
        )
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def load_numpy_core_numerictypes(_, module: Module) -> None:
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


def load_numpy_distutils_command_scons(_, module: Module) -> None:
    """The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_misc_util(_, module: Module) -> None:
    """The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_system_info(_, module: Module) -> None:
    """The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("Numeric")


def load_numpy_f2py___version__(_, module: Module) -> None:
    """The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("__svn_version__")


def load_numpy_linalg(
    finder: ModuleFinder,
    module: Module,  # noqa: ARG001
) -> None:
    """The numpy.linalg module implicitly loads the lapack_lite module; make
    sure this happens.
    """
    finder.include_module("numpy.linalg.lapack_lite")


def load_numpy__pytesttester(_, module: Module) -> None:
    """Remove optional modules in the numpy._pytesttester module."""
    module.exclude_names.add("pytest")


def load_numpy_random_mtrand(_, module: Module) -> None:
    """The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules.
    """
    module.global_names.update(["rand", "randn"])
