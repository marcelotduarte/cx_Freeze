"""Tests for hooks of numpy and pandas using mkl."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import IS_CONDA, IS_LINUX, IS_X86_64

TIMEOUT = 15
TIMEOUT_SLOW = 60 if IS_CONDA else 30

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.skipif(
    IS_CONDA
    or not (IS_LINUX and IS_X86_64 and sys.version_info[:2] == (3, 10)),
    reason="Test only on Linux64 and Python 3.10",
)
@pytest.mark.venv(install_dependencies=False)
@zip_packages
def test_mkl(tmp_package, zip_packages: bool) -> None:
    """Test that the pandas/numpy is working correctly."""
    tmp_package.create_from_sample("pandas")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    # use numpy with mkl
    tmp_package.install(
        "numpy", index="https://pypi.anaconda.org/intel/simple"
    )
    tmp_package.install("pandas")
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
