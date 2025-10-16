"""Tests for some hooks of stdlib packages."""

from __future__ import annotations

import os

import pytest

from cx_Freeze._compat import IS_MACOS, IS_WINDOWS

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
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@zip_packages
def test_ctypes(tmp_package, zip_packages: bool) -> None:
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
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "Hello ctypes*"])


@zip_packages
def test_sqlite(tmp_package, zip_packages: bool) -> None:
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
    result = tmp_package.run(executable, timeout=TIMEOUT)
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
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@zip_packages
def test_sqlite_ext(tmp_package, zip_packages: bool) -> None:
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
    result = tmp_package.run(executable, timeout=TIMEOUT)
    print(result.stdout)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "sqlite3 *",
            "[('this is a test of full-text search',)]",
        ]
    )


SOURCE_TEST_SSL = """
test_ssl.py
    import os
    import ssl

    print("Hello from cx_Freeze")
    print(ssl.__name__, ssl.OPENSSL_VERSION)
    ssl_paths = ssl.get_default_verify_paths()
    print(ssl_paths.openssl_cafile)
    print(os.environ.get("SSL_CERT_FILE"))
pyproject.toml
    [project]
    name = "test_ssl"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_ssl.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@zip_packages
def test_ssl(tmp_package, zip_packages: bool) -> None:
    """Test that the ssl is working correctly."""
    tmp_package.create(SOURCE_TEST_SSL)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_ssl")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "ssl*", "*"])


SOURCE_TEST_TK = """
test_tk.py
    import tkinter

    root = tkinter.Tk(useTk=False)
    print(root.tk.exprstring("$tcl_library"))
pyproject.toml
    [project]
    name = "test_tk"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_tk.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["unittest"]
    silent = true
"""


@zip_packages
def test_tkinter(tmp_package, zip_packages: bool) -> None:
    """Test if tkinter hook is working correctly."""
    pytest.importorskip("tkinter", reason="Depends on extra package: tkinter")

    tmp_package.create(SOURCE_TEST_TK)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_tk")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(executable.parent / "share/tcl")
    result.stdout.fnmatch_lines(f"{expected}*")


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_tkinter_bdist_mac(tmp_package) -> None:
    """Test if tkinter hook is working correctly using bdist_mac."""
    pytest.importorskip("tkinter", reason="Depends on extra package: tkinter")

    tmp_package.create(SOURCE_TEST_TK)
    tmp_package.freeze("cxfreeze bdist_mac")
    executable = tmp_package.executable("test_tk")

    name = "test_tk"
    version = "0.1.2.3"
    bundle_name = f"{name}-{version}"
    build_app_dir = tmp_package.path / "build" / f"{bundle_name}.app"
    executable = build_app_dir / "Contents/MacOS/test_tk"
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(build_app_dir / "Contents/Resources/share/tcl")
    result.stdout.fnmatch_lines(f"{expected}*")


@pytest.mark.venv(install_dependencies=False)
@pytest.mark.skipif(IS_WINDOWS, reason="Windows doesn't have system timezone")
@zip_packages
def test_zoneinfo(tmp_package, zip_packages: bool) -> None:
    """Test if zoneinfo hook with system timezone is working correctly."""
    tmp_package.create_from_sample("tz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    result = tmp_package.freeze()

    executable = tmp_package.executable("test_tz")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    if result.stderr.lines:
        python_result = tmp_package.run("python test_tz.py", timeout=TIMEOUT)
        if python_result.stderr.lines:
            pytest.xfail("system timezone is broken")
    result.stdout.fnmatch_lines(
        [
            "TZPATH: *",
            "Available timezones: *",
            "UTC time: *",
            "Brazil time: *",
            "US Eastern time: *",
        ]
    )


@pytest.mark.venv
@zip_packages
def test_zoneinfo_and_tzdata(tmp_package, zip_packages: bool) -> None:
    """Test if zoneinfo and tzdata hook is working correctly."""
    tmp_package.create_from_sample("tz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    result = tmp_package.freeze()

    executable = tmp_package.executable("test_tz")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "TZPATH: *",
            "Available timezones: *",
            "UTC time: *",
            "Brazil time: *",
            "US Eastern time: *",
        ]
    )
