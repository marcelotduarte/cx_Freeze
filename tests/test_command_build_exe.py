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

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"
BUILD_EXE_CMD = "python setup.py build_exe --silent --excludes=tkinter"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""

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
    ids=["yes", "none", "no"],
)
def test_build_exe_with_include_msvcr_option(option, value, result):
    """Test the build_exe with include_msvcr option."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **{option: value})
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert cmd.include_msvcr == result


@pytest.mark.datafiles(SAMPLES_DIR / "advanced")
def test_build_exe_advanced(datafiles: Path):
    """Test the advanced sample."""
    output = run_command(
        datafiles, "python setup.py build_exe --silent --excludes=tkinter"
    )

    executable = datafiles / BUILD_EXE_DIR / f"advanced_1{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output == OUTPUT1

    executable = datafiles / BUILD_EXE_DIR / f"advanced_2{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output == OUTPUT2


@pytest.mark.datafiles(SAMPLES_DIR / "asmodule")
def test_build_exe_asmodule(datafiles: Path):
    """Test the asmodule sample."""
    output = run_command(datafiles, BUILD_EXE_CMD)

    executable = datafiles / BUILD_EXE_DIR / f"asmodule{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.datafiles(SAMPLES_DIR / "sqlite")
def test_build_exe_sqlite(datafiles: Path):
    """Test the sqlite sample."""
    output = run_command(datafiles, BUILD_EXE_CMD)

    executable = datafiles / BUILD_EXE_DIR / f"test_sqlite3{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("dump.sql created")


def test_zip_include_packages(tmp_path):
    """Test the simple sample with zip_include_packages option."""
    source = SUB_PACKAGE_TEST[4]
    create_package(tmp_path, source)
    output = run_command(
        tmp_path,
        f"{BUILD_EXE_CMD} --zip-exclude-packages=* --zip-include-packages=p",
    )

    executable = tmp_path / BUILD_EXE_DIR / f"main{SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT_SUBPACKAGE_TEST


def test_zip_exclude_packages(tmp_path):
    """Test the simple sample with zip_exclude_packages option."""
    source = SUB_PACKAGE_TEST[4]
    create_package(tmp_path, source)
    output = run_command(
        tmp_path,
        f"{BUILD_EXE_CMD} --zip-exclude-packages=p --zip-include-packages=*",
    )

    executable = tmp_path / BUILD_EXE_DIR / f"main{SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT_SUBPACKAGE_TEST
