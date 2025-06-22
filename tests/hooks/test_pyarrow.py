"""Tests for cx_Freeze.hooks of pyarrow."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_ARM_64, IS_CONDA, IS_WINDOWS

TIMEOUT_SLOW = 60 if IS_CONDA else 20

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PYARROW = """
test_pyarrow.py
    import pyarrow as pa

    print("Hello from cx_Freeze")
    print("pyarrow version", pa.__version__)

    table = pa.Table.from_pylist([
        {"col1": 1, "col2": "a"},
        {"col1": 2, "col2": "b"},
        {"col1": 3, "col2": "c"},
        {"col1": 4, "col2": "d"},
        {"col1": 5, "col2": "e"}
    ])
    print(table)
pyproject.toml
    [project]
    name = "test_pyarrow"
    version = "0.1.2.3"
    dependencies = [
        "pyarrow;python_version < '3.13'",
        "pyarrow>=20;python_version >= '3.13'",
    ]

    [tool.cxfreeze]
    executables = ["test_pyarrow.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pyarrow not supported in windows arm64",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_pyarrow(tmp_package, zip_packages: bool) -> None:
    """Test if pyarrow hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PYARROW)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()
    executable = tmp_package.executable("test_pyarrow")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("pyarrow version")
    assert len(lines) == 8, lines[1:]
