"""Tests for cx_Freeze.hooks of numpy, pandas and scipy."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_LINUX,
    IS_MINGW,
    IS_WINDOWS,
    IS_X86_64,
)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pandas not supported in windows arm64",
    strict=True,
)
@zip_packages
def test_pandas(tmp_package, zip_packages: bool) -> None:
    """Test that the pandas/numpy is working correctly."""
    command = "python setup.py build_exe -O2 --excludes=tkinter,unittest"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr"

    tmp_package.create_from_sample("pandas")
    if IS_LINUX and IS_X86_64 and sys.version_info[:2] == (3, 10):
        tmp_package.install(
            "numpy", index="https://pypi.anaconda.org/intel/simple"
        )
    tmp_package.install("pandas")
    output = tmp_package.run(command)
    executable = tmp_package.executable("test_pandas")
    assert executable.is_file()

    output = tmp_package.run(executable, timeout=20)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("pandas version")
    assert len(lines) == 8, lines[2:]


SOURCE_TEST_RASTERIO = """
test_rasterio.py
    import numpy as np
    import rasterio

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("rasterio version", rasterio.__version__)
pyproject.toml
    [project]
    name = "test_rasterio"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_rasterio.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    (IS_LINUX or IS_WINDOWS) and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="rasterio not supported in windows/linux arm64",
    strict=True,
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="rasterio not supported in mingw",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="rasterio does not support Python 3.13t",
    strict=True,
)
@zip_packages
def test_rasterio(tmp_package, zip_packages: bool) -> None:
    """Test if rasterio hook is working correctly."""
    tmp_package.create(SOURCE_TEST_RASTERIO)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.install("rasterio")
    output = tmp_package.run()
    executable = tmp_package.executable("test_rasterio")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=20)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("numpy version")
    assert lines[2].startswith("rasterio version")


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pandas not supported in windows arm64",
    strict=True,
)
@zip_packages
def test_scipy(tmp_package, zip_packages: bool) -> None:
    """Test that the scipy/numpy is working correctly."""
    command = "python setup.py build_exe -O2 --excludes=tkinter"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr"

    tmp_package.create_from_sample("scipy")
    tmp_package.install("scipy")
    output = tmp_package.run(command)
    executable = tmp_package.executable("test_scipy")
    assert executable.is_file()

    output = tmp_package.run(executable, timeout=20)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("scipy version")
    assert len(lines) == 5, lines[2:]
