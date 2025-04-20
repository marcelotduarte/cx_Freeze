"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import IS_LINUX, IS_MINGW, IS_WINDOWS

SOURCE = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    setup(executables=["test.py"])
command
    python setup.py build_exe --silent
"""

if IS_WINDOWS:
    PACKAGE_VERSION = [("imagehlp", "bind")]
    if sys.version_info[:2] < (3, 12):
        PACKAGE_VERSION += [("lief", "0.13.2")]
    PACKAGE_VERSION += [
        ("lief", "0.14.1"),
        ("lief", "0.15.1"),
        ("lief", "0.16.5"),
    ]
elif IS_MINGW:
    PACKAGE_VERSION = [("imagehlp", "bind")]
elif IS_LINUX:
    PACKAGE_VERSION = [("patchelf", "bind")]
else:
    PACKAGE_VERSION = [("", "")]


@pytest.mark.parametrize(("package", "version"), PACKAGE_VERSION)
def test_parser(tmp_package, package, version) -> None:
    """Test a simple build."""
    tmp_package.create(SOURCE)

    if version == "bind":
        tmp_package.monkeypatch.setenv("CX_FREEZE_BIND", package)
    elif package != "":
        tmp_package.install(f"{package}=={version}")

    # first run, count the files
    output = tmp_package.run()

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
