"""Tests for cx_Freeze.command.build_exe."""
from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import SUB_PACKAGE_TEST, create_package, run_command
from setuptools import Distribution

from cx_Freeze.command.build_exe import BuildEXE as build_exe
from cx_Freeze.exception import SetupError

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
FIXTURE_DIR = Path(__file__).resolve().parent

OUTPUT1 = "Hello from cx_Freeze Advanced #1\nTest freeze module #1\n"
OUTPUT2 = "Hello from cx_Freeze Advanced #2\nTest freeze module #2\n"

OUTPUT_SUBPACKAGE_TEST = "This is p.p1\nThis is p.q.q1\n"

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": [],
    "script_name": "setup.py",
}


@pytest.mark.parametrize(
    ("option", "value"),
    [
        # build_exe directory is the same as the build_base
        ("build_exe", "build")
    ],
)
def test_build_exe_invalid_options(option, value):
    """Test the build_exe with invalid options."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **{option: value})
    with pytest.raises(SetupError):
        cmd.finalize_options()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.parametrize(
    ("option", "value", "result"),
    [
        ("include_msvcr", True, True),
        ("include_msvcr", None, False),
        ("include_msvcr", False, False),
    ],
)
def test_build_exe_with_include_msvcr_option(option, value, result):
    """Test the build_exe with include-msvcr option."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **{option: value})
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.include_msvcr == result


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "advanced")
def test_build_exe_advanced(datafiles: Path):
    """Test the advanced sample."""
    output = run_command(
        datafiles, "python setup.py build_exe --silent --excludes=tkinter"
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""

    executable = datafiles / BUILD_EXE_DIR / f"advanced_1{suffix}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output == OUTPUT1

    executable = datafiles / BUILD_EXE_DIR / f"advanced_2{suffix}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output == OUTPUT2


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "asmodule")
def test_build_exe_asmodule(datafiles: Path):
    """Test the asmodule sample."""
    output = run_command(
        datafiles, "python setup.py build_exe --silent --excludes=tkinter"
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"asmodule{suffix}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "simple")
def test_build_exe_simple_include_msvcr(datafiles: Path):
    """Test the simple sample with include_msvcr option."""
    output = run_command(
        datafiles,
        "python setup.py build_exe --silent --excludes=tkinter "
        "--include-msvcr",
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"hello{suffix}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.datafiles(FIXTURE_DIR.parent / "samples" / "sqlite")
def test_build_exe_sqlite(datafiles: Path):
    """Test the sqlite sample."""
    output = run_command(
        datafiles, "python setup.py build_exe --silent --excludes=tkinter"
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = datafiles / BUILD_EXE_DIR / f"test_sqlite3{suffix}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("dump.sql created")


def test_zip_include_packages(tmp_path):
    """Provides test cases for ModuleFinder class."""
    source = SUB_PACKAGE_TEST[4]
    create_package(tmp_path, source)
    output = run_command(
        tmp_path,
        "python setup.py build_exe --silent --excludes=tkinter "
        "--zip-exclude-packages=* --zip-include-packages=p",
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = tmp_path / BUILD_EXE_DIR / f"main{suffix}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT_SUBPACKAGE_TEST


def test_zip_exclude_packages(tmp_path):
    """Provides test cases for ModuleFinder class."""
    source = SUB_PACKAGE_TEST[4]
    create_package(tmp_path, source)
    output = run_command(
        tmp_path,
        "python setup.py build_exe --silent --excludes=tkinter "
        "--zip-exclude-packages=p --zip-include-packages=*",
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = tmp_path / BUILD_EXE_DIR / f"main{suffix}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT_SUBPACKAGE_TEST
