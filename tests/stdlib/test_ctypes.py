"""Tests for hooks of stdlib ctypes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_CTYPES = """
test_ctypes.py
    import ctypes

    print("Hello from cx_Freeze")
    print("Hello", ctypes.__name__)
pyproject.toml
    [project]
    name = "test_ctypes"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_ctypes.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


@zip_packages
def test_ctypes(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test if ctypes hook is working correctly."""
    tmp_package.create(SOURCE_TEST_CTYPES)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_ctypes")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "Hello ctypes*"])
