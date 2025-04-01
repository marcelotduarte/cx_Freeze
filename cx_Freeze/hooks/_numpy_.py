"""A collection of functions which are triggered automatically by finder when
numpy package is included.
"""

from __future__ import annotations

import json
import sys
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.libs import replace_delvewheel_patch

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

    Supported pypi and conda-forge versions (tested from 1.21.2 to 2.2.4).
    """
    source_dir = module.file.parent.parent / f"{module.name}.libs"
    if source_dir.exists():  # numpy >= 1.26.0
        target_dir = f"lib/{source_dir.name}"
        for source in source_dir.iterdir():
            target = f"{target_dir}/{source.name}"
            finder.lib_files[source] = target
        if IS_WINDOWS:
            finder.include_files(source_dir, target_dir)
            replace_delvewheel_patch(module)

    # Exclude unnecessary modules
    finder.exclude_module("numpy._configtool")
    finder.exclude_module("numpy.conftest")
    finder.exclude_module("numpy.distutils")
    finder.exclude_module("numpy.f2py")
    finder.exclude_module("numpy._pyinstaller")
    finder.exclude_module("numpy.random._examples")
    finder.exclude_module("numpy.typing.mypy_plugin")

    # Exclude/Include modules based on distribution and/or version
    distribution = module.distribution
    if distribution:
        # Exclude tests
        excludes = set()
        for file in distribution.original.files:
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

    code_string = module.file.read_text(encoding="utf_8")
    code_string = code_string.replace(
        "__file__", "__file__.replace('library.zip', '.')"
    )
    module.code = compile(
        code_string.replace("import numpy.f2py as f2py", "f2py = None"),
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def load_numpy_compat_py3k(_, module: Module) -> None:
    """Ignore errors if optionally imported module cannot be found."""
    module.ignore_names.add("pickle5")


def load_numpy___config__(_, module: Module) -> None:
    """Ignore errors if optionally imported module cannot be found."""
    module.ignore_names.add("yaml")


# see list from numpy/__init__.py
NUMPY_GLOBAL_NAMES = """
    False_, ScalarType, True_,
    abs, absolute, acos, acosh, add, all, allclose,
    amax, amin, any, arange, arccos, arccosh, arcsin, arcsinh,
    arctan, arctan2, arctanh, argmax, argmin, argpartition, argsort,
    argwhere, around, array, array2string, array_equal, array_equiv,
    array_repr, array_str, asanyarray, asarray, ascontiguousarray,
    asfortranarray, asin, asinh, atan, atanh, atan2, astype, atleast_1d,
    atleast_2d, atleast_3d, base_repr, binary_repr, bitwise_and,
    bitwise_count, bitwise_invert, bitwise_left_shift, bitwise_not,
    bitwise_or, bitwise_right_shift, bitwise_xor, block, bool, bool_,
    broadcast, busday_count, busday_offset, busdaycalendar, byte, bytes_,
    can_cast, cbrt, cdouble, ceil, character, choose, clip, clongdouble,
    complex128, complex64, complexfloating, compress, concat, concatenate,
    conj, conjugate, convolve, copysign, copyto, correlate, cos, cosh,
    count_nonzero, cross, csingle, cumprod, cumsum, cumulative_prod,
    cumulative_sum, datetime64, datetime_as_string, datetime_data,
    deg2rad, degrees, diagonal, divide, divmod, dot, double, dtype, e,
    einsum, einsum_path, empty, empty_like, equal, errstate, euler_gamma,
    exp, exp2, expm1, fabs, finfo, flatiter, flatnonzero, flexible,
    float16, float32, float64, float_power, floating, floor, floor_divide,
    fmax, fmin, fmod, format_float_positional, format_float_scientific,
    frexp, from_dlpack, frombuffer, fromfile, fromfunction, fromiter,
    frompyfunc, fromstring, full, full_like, gcd, generic, geomspace,
    get_printoptions, getbufsize, geterr, geterrcall, greater,
    greater_equal, half, heaviside, hstack, hypot, identity, iinfo,
    indices, inexact, inf, inner, int16, int32, int64, int8, int_, intc,
    integer, intp, invert, is_busday, isclose, isdtype, isfinite,
    isfortran, isinf, isnan, isnat, isscalar, issubdtype, lcm, ldexp,
    left_shift, less, less_equal, lexsort, linspace, little_endian, log,
    log10, log1p, log2, logaddexp, logaddexp2, logical_and, logical_not,
    logical_or, logical_xor, logspace, long, longdouble, longlong, matmul,
    matvec, matrix_transpose, max, maximum, may_share_memory, mean, memmap,
    min, min_scalar_type, minimum, mod, modf, moveaxis, multiply, nan,
    ndarray, ndim, nditer, negative, nested_iters, newaxis, nextafter,
    nonzero, not_equal, number, object_, ones, ones_like, outer, partition,
    permute_dims, pi, positive, pow, power, printoptions, prod,
    promote_types, ptp, put, putmask, rad2deg, radians, ravel, recarray,
    reciprocal, record, remainder, repeat, require, reshape, resize,
    result_type, right_shift, rint, roll, rollaxis, round, sctypeDict,
    searchsorted, set_printoptions, setbufsize, seterr, seterrcall, shape,
    shares_memory, short, sign, signbit, signedinteger, sin, single, sinh,
    size, sort, spacing, sqrt, square, squeeze, stack, std,
    str_, subtract, sum, swapaxes, take, tan, tanh, tensordot,
    timedelta64, trace, transpose, true_divide, trunc, typecodes, ubyte,
    ufunc, uint, uint16, uint32, uint64, uint8, uintc, uintp, ulong,
    ulonglong, unsignedinteger, unstack, ushort, var, vdot, vecdot,
    vecmat, void, vstack, where, zeros, zeros_like
"""


def load_numpy_core(_, module: Module) -> None:  # NumPy < 2.0
    """Set the numpy.core global names."""
    module.global_names.update(
        NUMPY_GLOBAL_NAMES.replace("\n", "").replace(" ", "").split(",")
    )
    module.global_names.add("geterrobj")


def load_numpy__core(_, module: Module) -> None:
    """Set the numpy._core global names."""
    module.global_names.update(
        NUMPY_GLOBAL_NAMES.replace("\n", "").replace(" ", "").split(",")
    )


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
    module.ignore_names.add("numpy._distributor_init_local")
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
        code_string = code_string.replace(
            "__file__", "__file__.replace('library.zip', '.')"
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
    dynamically; define these to avoid spurious errors about missing modules.
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


def load_numpy_lib_utils(_, module: Module) -> None:  # numpy<2
    """The module numpy.lib.utils optionally imports the threadpoolctl module;
    ignore the error if the module cannot be found.
    """
    module.ignore_names.add("threadpoolctl")


def load_numpy_lib__utils_impl(_, module: Module) -> None:
    """The module numpy.lib._utils_impl optionally imports the threadpoolctl
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("threadpoolctl")


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
    module.exclude_names.update(["numpy.distutils", "pytest"])
    module.ignore_names.update(["numpy.distutils", "pytest"])


def load_numpy_random_mtrand(_, module: Module) -> None:
    """The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules.
    """
    module.global_names.update(["rand", "randn"])


def load_numpy_testing__private_utils(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(
        ["numpy.distutils.misc_util", "psutil", "pytest", "win32pdh"]
    )


def load_numpy__typing(_, module: Module) -> None:
    """Ignore optional module."""
    module.ignore_names.add("numpy._typing._ufunc")
