"""Tests for cx_Freeze.command.build_exe."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import SUB_PACKAGE_TEST, create_package, run_command
from setuptools import Distribution

from cx_Freeze.command.build_exe import build_exe
from cx_Freeze.exception import SetupError
from cx_Freeze.executable import Executable

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = os.path.normpath(f"build/exe.{PLATFORM}-{PYTHON_VERSION}")

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
    "executables": [Executable("hello.py")],
    "script_name": "setup.py",
}


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        pytest.param(
            {"build_exe": None},
            {"build_exe": BUILD_EXE_DIR},
            id="build-exe=none",
        ),
        pytest.param(
            {"build_exe": "dist"}, {"build_exe": "dist"}, id="build-exe=dist"
        ),
        pytest.param(
            {"excludes": "tkinter,unittest"},
            {"excludes": ["tkinter", "unittest"]},
            id="excludes='tkinter,unittest'",
        ),
        pytest.param(
            {"excludes": ["tkinter", "unittest"]},
            {"excludes": ["tkinter", "unittest"]},
            id="excludes=['tkinter','unittest']",
        ),
        pytest.param(
            {"include_msvcr": None},
            {"include_msvcr": False},
            id="include-msvcr=none",
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
        ),
        pytest.param(
            {"include_msvcr": False},
            {"include_msvcr": False},
            id="include-msvcr=false",
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
        ),
        pytest.param(
            {"include_msvcr": True},
            {"include_msvcr": True},
            id="include-msvcr=true",
            marks=pytest.mark.skipif(not IS_WINDOWS, reason="Windows tests"),
        ),
        pytest.param(
            {"replace_paths": [("*", "")]},
            {"replace_paths": [("*", "")]},
            id="replace_paths=*",
        ),
        pytest.param(
            {"replace_paths": "*="},
            {"replace_paths": ["*="]},
            id="replace_paths=*=",
        ),
        pytest.param(
            {"replace_paths": ["*="]},
            {"replace_paths": ["*="]},
            id="replace_paths=[*=]",
        ),
        pytest.param({"silent": None}, {"silent": 0}, id="silent=none->0"),
        pytest.param({"silent": False}, {"silent": 0}, id="silent=false->0"),
        pytest.param({"silent": True}, {"silent": 1}, id="silent=true->1"),
        pytest.param(
            {"silent_level": None}, {"silent": 0}, id="silent-level=none->0"
        ),
        pytest.param(
            {"silent_level": 0}, {"silent": 0}, id="silent-level=0->0"
        ),
        pytest.param(
            {"silent_level": 1}, {"silent": 1}, id="silent-level=1->1"
        ),
        pytest.param(
            {"silent_level": 2}, {"silent": 2}, id="silent-level=2->2"
        ),
        pytest.param(
            {"silent_level": "3"}, {"silent": 3}, id="silent-level=3->3"
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": None},
            {"zip_include_packages": [], "zip_exclude_packages": []},
            id="zip_include_packages/zip_exclude_packages=none/none",
        ),
        pytest.param(
            {"zip_include_packages": ["*"], "zip_exclude_packages": None},
            {"zip_include_packages": ["*"], "zip_exclude_packages": []},
            id="zip_include_package=[*]",
        ),
        pytest.param(
            {"zip_include_packages": None, "zip_exclude_packages": ["*"]},
            {"zip_include_packages": [], "zip_exclude_packages": ["*"]},
            id="zip_exclude_packages=*",
        ),
        pytest.param(  # zip_*_packages are namespace packages
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            {
                "zip_include_packages": ["namespace.test"],
                "zip_exclude_packages": ["zope.event", "zope.interface"],
            },
            id="zip_include_packages/zip_exclude_packages=namespace/namespace",
        ),
        pytest.param(
            {"zip_include_packages": "*", "zip_exclude_packages": []},
            {"zip_include_packages": ["*"], "zip_exclude_packages": []},
            id="zip_include_package=*",
        ),
    ],
)
def test_build_exe_finalize_options(
    kwargs: dict[str, ...], expected: dict[str, ...]
) -> None:
    """Test the build_exe finalize_options."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **kwargs)
    cmd.finalize_options()
    cmd.ensure_finalized()
    for option, value in expected.items():
        assert getattr(cmd, option) == value


@pytest.mark.parametrize(
    ("kwargs", "expected_exception", "expected_match"),
    [
        pytest.param(
            {"build_exe": "build"},
            SetupError,
            "build_exe option cannot be the same as build_base directory",
            id="build-exe=build",
        ),
    ],
)
def test_build_exe_finalize_options_raises(
    kwargs: dict[str, ...], expected_exception, expected_match: str
) -> None:
    """Test the build_exe finalize_options that raises an exception."""
    dist = Distribution(DIST_ATTRS)
    cmd = build_exe(dist, **kwargs)
    with pytest.raises(expected_exception, match=expected_match):
        cmd.finalize_options()


@pytest.mark.datafiles(SAMPLES_DIR / "advanced")
def test_build_exe_advanced(datafiles: Path) -> None:
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
def test_build_exe_asmodule(datafiles: Path) -> None:
    """Test the asmodule sample."""
    output = run_command(datafiles, BUILD_EXE_CMD)

    executable = datafiles / BUILD_EXE_DIR / f"asmodule{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


@pytest.mark.datafiles(SAMPLES_DIR / "sqlite")
def test_build_exe_sqlite(datafiles: Path) -> None:
    """Test the sqlite sample."""
    output = run_command(datafiles, BUILD_EXE_CMD)

    executable = datafiles / BUILD_EXE_DIR / f"test_sqlite3{SUFFIX}"
    assert executable.is_file()
    output = run_command(datafiles, executable, timeout=10)
    assert output.startswith("dump.sql created")


def test_zip_include_packages(tmp_path) -> None:
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


def test_zip_exclude_packages(tmp_path) -> None:
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
