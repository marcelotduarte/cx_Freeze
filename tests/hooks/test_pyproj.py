"""Tests for hooks of pyproj."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_CONDA

TIMEOUT_SLOW = 60 if IS_CONDA else 30

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PYPROJ = """
test_pyproj.py
    import pyproj

    print("Hello from cx_Freeze")
    print("pyproj version", pyproj.__version__)
pyproject.toml
    [project]
    name = "test_pyproj"
    version = "0.1.2.3"
    dependencies = ["pyproj"]

    [tool.cxfreeze]
    executables = ["test_pyproj.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_pyproj(tmp_package, zip_packages: bool) -> None:
    """Test if pyproj hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PYPROJ)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_pyproj")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "pyproj version *"])
    result.stderr.no_fnmatch_line(
        "*UserWarning: Valid PROJ data directory not found.*"
    )
