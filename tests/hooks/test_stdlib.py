"""Tests for some cx_Freeze.hooks using stdlib packages."""

from __future__ import annotations

import os

import pytest

from cx_Freeze._compat import IS_MACOS

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
    output = tmp_package.run()
    executable = tmp_package.executable("test_ctypes")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("Hello ctypes")


@zip_packages
def test_sqlite(tmp_package, zip_packages: bool) -> None:
    """Test that the sqlite3 is working correctly."""
    tmp_package.create_from_sample("sqlite")
    if zip_packages:
        output = tmp_package.run(
            "python setup.py build_exe"
            " --zip-include-packages=* --zip-exclude-packages="
        )
    else:
        output = tmp_package.run()
    executable = tmp_package.executable("test_sqlite3")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.startswith("dump.sql created")


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
    output = tmp_package.run()
    executable = tmp_package.executable("test_ssl")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("ssl")
    assert output.splitlines()[2] != ""


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
    output = tmp_package.run()
    executable = tmp_package.executable("test_tk")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(executable.parent / "share/tcl")
    assert output.splitlines()[0].startswith(expected)


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_tkinter_bdist_mac(tmp_package) -> None:
    """Test if tkinter hook is working correctly using bdist_mac."""
    pytest.importorskip("tkinter", reason="Depends on extra package: tkinter")

    tmp_package.create(SOURCE_TEST_TK)
    output = tmp_package.run("cxfreeze bdist_mac")
    executable = tmp_package.executable("test_tk")

    name = "test_tk"
    version = "0.1.2.3"
    bundle_name = f"{name}-{version}"
    build_app_dir = tmp_package.path / "build" / f"{bundle_name}.app"
    executable = build_app_dir / "Contents/MacOS/test_tk"
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    # Compare the start of the returned path, version independent.
    # This is necessary when the OS has an older tcl/tk version than the
    # version contained in the cx_Freeze wheels.
    expected = os.path.normpath(build_app_dir / "Contents/Resources/share/tcl")
    assert output.splitlines()[0].startswith(expected)


@zip_packages
def test_tz(tmp_package, zip_packages: bool) -> None:
    """Test if zoneinfo hook is working correctly."""
    tmp_package.create_from_sample("tz")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()
    if "? tzdata imported from zoneinfo_hook" in output:
        tmp_package.install("tzdata")
        output = tmp_package.run()

    executable = tmp_package.executable("test_tz")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("TZPATH")
    assert lines[1].startswith("Available")
    assert lines[2].startswith("UTC")
    assert lines[3].startswith("Brazil")
    assert lines[4].startswith("US")
