"""Tests for hooks of stdlib sqlite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


@zip_packages
def test_sqlite(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test that the sqlite3 is working correctly."""
    tmp_package.create_from_sample("sqlite")
    if zip_packages:
        tmp_package.freeze(
            "python setup.py build_exe"
            " --zip-include-packages=* --zip-exclude-packages="
        )
    else:
        tmp_package.freeze()
    executable = tmp_package.executable("test_sqlite3")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines("dump.sql created")


SOURCE_TEST_SQLITE = """
test_sqlite.py
    import sqlite3

    print("Hello from cx_Freeze")
    print(sqlite3.__name__, sqlite3.sqlite_version)

    conn = sqlite3.connect(":memory:")
    try:
        conn.execute("create virtual table fts5test using fts5 (data);")
    except:
        import sys
        sys.exit()
    conn.execute(
        "insert into fts5test (data) "
        "values ('this is a test of full-text search');"
    )
    print(
        conn.execute(
            "select * from fts5test where data match 'full';"
        ).fetchall()
    )
pyproject.toml
    [project]
    name = "test_sqlite"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_sqlite.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


@zip_packages
def test_sqlite_ext(tmp_package: TempPackage, zip_packages: bool) -> None:
    """Test that the sqlite3 is working correctly."""
    tmp_package.create(SOURCE_TEST_SQLITE)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_sqlite")
    assert executable.is_file()
    result = tmp_package.run(executable)
    print(result.stdout)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "sqlite3 *",
            "[('this is a test of full-text search',)]",
        ]
    )
