"""Tests for hooks of pandas (and numpy and mkl)."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_CONDA, IS_LINUX, IS_MACOS, IS_X86_64

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT_SLOW = 30 * (2 if IS_CONDA else 1) * (2 if IS_MACOS else 1)

USE_MKL = [pytest.param(False, id="")]
if not IS_CONDA and (
    IS_LINUX and IS_X86_64 and sys.version_info[:2] == (3, 11)
):
    USE_MKL.append(pytest.param(True, id="use_mkl"))

use_mkl = pytest.mark.parametrize("use_mkl", USE_MKL)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PANDAS = """
test_pandas.py
    import numpy as np
    import pandas as pd

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("pandas version", pd.__version__)

    a = np.arange(1.0, 10.0).reshape((3, 3)) % 5
    np.linalg.det(a)
    a @ a
    a @ a.T
    np.linalg.inv(a)
    np.sin(np.exp(a))
    np.linalg.svd(a)
    np.linalg.eigh(a)

    np.unique(np.random.randint(0, 10, 100))
    np.sort(np.random.uniform(0, 10, 100))

    np.fft.fft(np.exp(2j * np.pi * np.arange(8) / 8))
    np.ma.masked_array(np.arange(10), np.random.rand(10) < 0.5).sum()
    np.polynomial.Legendre([7, 8, 9]).roots()

    df = pd.DataFrame(np.random.random(size=(100, 5)))
    corr_mat = df.corr()
    mask = np.tril(np.ones_like(corr_mat, dtype=bool), k=-1)
    print(corr_mat.where(mask))
pyproject.toml
    [project]
    name = "test_pandas"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "pandas<2.3;python_version < '3.11'",
        "pandas>=2.3;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_pandas.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter", "email", "http", "xml", "pyarrow"]
    optimize = 2
    silent = true
"""


@pytest.mark.venv(install_dependencies=False)
@use_mkl
@zip_packages
def test_pandas(
    tmp_package: TempPackage, zip_packages: bool, use_mkl: bool
) -> None:
    """Test that the pandas/numpy/mkl is working correctly."""
    tmp_package.create(SOURCE_TEST_PANDAS)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))

    if use_mkl:  # numpy with mkl
        tmp_package.install(
            "numpy", index="https://pypi.anaconda.org/intel/simple"
        )
        tmp_package.install("pandas")
    else:
        tmp_package.install_dependencies()
    tmp_package.freeze()

    executable = tmp_package.executable("test_pandas")
    assert executable.is_file()

    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "numpy version *",
            "pandas version *",
            " *",
            "0*",
            "1*",
            "2*",
            "3*",
            "4*",
        ]
    )
