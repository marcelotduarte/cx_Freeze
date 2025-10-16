"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

import shutil
import stat
import sys
import sysconfig
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MINGW,
    IS_WINDOWS,
    IS_X86_32,
    IS_X86_64,
)
from cx_Freeze.dep_parser import ELFParser
from cx_Freeze.exception import PlatformError

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = """
test.py
    print("Hello from cx_Freeze")
"""

if IS_WINDOWS:
    PACKAGE_VERSION = [("imagehlp", "bind")]
    if IS_CONDA:
        PACKAGE_VERSION += [("py-lief", "0.16.6")]
    elif IS_ARM_64 and sys.version_info[:2] <= (3, 13) and ABI_THREAD == "":
        PACKAGE_VERSION += [("lief", "0.16.6"), ("lief", "0.17.0")]
    elif (IS_X86_32 or IS_X86_64) and ABI_THREAD == "":
        if sys.version_info[:2] <= (3, 13):
            PACKAGE_VERSION += [("lief", "0.15.1"), ("lief", "0.16.6")]
        PACKAGE_VERSION += [("lief", "0.17.0")]
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
    command = "cxfreeze --script test.py --silent"
    command += " --excludes=tkinter,unittest --include-msvcr"
    tmp_package.freeze(command)

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_elf_parser(tmp_package) -> None:
    """Test the search_path and find_library."""
    tmp_package.create(SOURCE)
    parser = ELFParser(sys.path, [sysconfig.get_config_var("LIBDIR")])
    names = ("python", "sqlite3")
    found = None
    for name in names:
        found = parser.find_library(name)
        if found:
            break
    assert found, f"library not found for: {names}"

    # copy the library to use it for tests
    filename: Path = tmp_package.path / found.name
    shutil.copyfile(found, filename)
    mode = filename.stat().st_mode
    if mode & stat.S_IWUSR != 0:
        filename.chmod(mode & ~stat.S_IWUSR)
    so_names = parser.get_needed(filename)
    new_names = sorted(so_names)
    for i, so_name in enumerate(so_names):
        parser.replace_needed(filename, so_name, new_names[i])
    parser.set_soname(filename, "foo.so")

    assert parser.get_rpath("foo") == ""


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
def test_verify_patchelf(monkeypatch) -> None:
    """Test the _verify_patchelf."""
    monkeypatch.setattr("shutil.which", lambda cmd: cmd != "patchelf")
    msg = "Cannot find required utility `patchelf` in PATH"
    with pytest.raises(PlatformError, match=msg):
        ELFParser([], [])


@pytest.mark.skipif(not IS_LINUX, reason="Linux test")
@pytest.mark.skipif(IS_LINUX and IS_CONDA, reason="Disabled on conda-forge")
@pytest.mark.venv
def test_verify_patchelf_older(tmp_package) -> None:
    """Test the _verify_patchelf with older version."""
    tmp_package.create(SOURCE)
    tmp_package.install("patchelf<0.14")

    tmp_bin = tmp_package.venv_prefix / "bin"
    tmp_package.monkeypatch.setattr("shutil.which", lambda cmd: tmp_bin / cmd)
    msg = r"patchelf\s+(\d+(.\d+)?)\s+found."
    with pytest.raises(ValueError, match=msg):
        ELFParser([], [])
