"""Tests for hooks of rasterio."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_CONDA, IS_MINGW

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT_SLOW = 60 if IS_CONDA else 30

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST_RASTERIO = """
test_rasterio.py
    import numpy
    import rasterio

    print("Hello from cx_Freeze")
    print()
    rasterio.show_versions()
pyproject.toml
    [project]
    name = "test_rasterio"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "rasterio",
    ]

    [tool.cxfreeze]
    executables = ["test_rasterio.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="rasterio not supported in mingw",
    strict=not bool(int(os.getenv("PYTEST_LAX_XFAIL", "0"))),
)
@pytest.mark.venv
@zip_packages
def test_rasterio(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if rasterio hook is working correctly."""
    tmp_package.create(SOURCE_TEST_RASTERIO)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_rasterio")
    assert executable.is_file()

    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "rasterio info:",
            "*rasterio: *",
            "*numpy: *",
        ]
    )
    result.stderr.no_fnmatch_line("Warning*: Cannot find *")
