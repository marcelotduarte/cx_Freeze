"""Tests for some hooks of setuptools package."""

from __future__ import annotations

import pytest

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_SETUPTOOLS = """
test_setuptools.py
    import setuptools

    print("Hello from cx_Freeze")
    print("Hello", setuptools.__name__)
pyproject.toml
    [project]
    name = "test_setuptools"
    version = "0.1.2.3"
    dependencies = [
        "setuptools==78.1.1;python_version == '3.10'",
        "setuptools==80.9.0;python_version == '3.11'",
        "setuptools;python_version >= '3.12'",
    ]


    [tool.cxfreeze]
    executables = ["test_setuptools.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@zip_packages
def test_setuptools(tmp_package, zip_packages: bool) -> None:
    """Test if setuptools hook is working correctly."""
    tmp_package.create(SOURCE_TEST_SETUPTOOLS)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.install_dependencies()
    tmp_package.freeze()
    executable = tmp_package.executable("test_setuptools")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "Hello setuptools*"])
