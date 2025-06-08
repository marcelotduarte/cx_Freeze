"""Tests for cx_Freeze.hooks of pyarrow."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PYMUPDF = """
test_pymupdf.py
    import pymupdf

    print("Hello from cx_Freeze")
    print("pymupdf version", pymupdf.__version__)
pyproject.toml
    [project]
    name = "test_pymupdf"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_pymupdf.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.skipif(
    IS_CONDA and (IS_LINUX or IS_WINDOWS or (IS_ARM_64 and IS_MACOS)),
    reason="pymupdf is broken in conda-forge (except on OSX64)",
)
@pytest.mark.skipif(IS_MINGW, reason="pymupdf is broken in mingw")
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pymupdf not supported in windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pymupdf does not support Python 3.13t",
    strict=True,
)
@zip_packages
def test_pymupdf(tmp_package, zip_packages: bool) -> None:
    """Test if pymupdf hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PYMUPDF)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    if sys.version_info[:2] <= (3, 10):
        package = "pymupdf~=1.24.4" if IS_CONDA else "pymupdf==1.24.4"
    elif sys.version_info[:2] < (3, 11):
        package = "pymupdf<=1.26"
    else:
        package = "pymupdf"
    tmp_package.install(package)
    output = tmp_package.run()
    executable = tmp_package.executable("test_pymupdf")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=20)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("pymupdf version")
