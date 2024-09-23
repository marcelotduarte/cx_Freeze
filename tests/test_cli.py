"""Tests for 'cxfreeze' command."""

from __future__ import annotations

import os
import sys
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = """
test.py
    print("Hello from cx_Freeze")
command
    cxfreeze --script test.py --target-dir=dist --excludes=tkinter
"""


def test_cxfreeze(tmp_path: Path) -> None:
    """Test cxfreeze."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)

    file_created = tmp_path / "dist" / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_help(tmp_path: Path) -> None:
    """Test cxfreeze help."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path, "cxfreeze --help")
    assert output.startswith("usage")


def test_cxfreeze_additional_help(tmp_path: Path) -> None:
    """Test cxfreeze additional help."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path, "cxfreeze build_exe --help")
    assert "usage: " in output


def test_cxfreeze_target_name_not_isidentifier(tmp_path: Path) -> None:
    """Test cxfreeze --target-name not isidentifier, but valid filename."""
    create_package(tmp_path, SOURCE)
    output = run_command(
        tmp_path,
        "cxfreeze --script test.py --target-name=12345 --excludes=tkinter",
    )

    file_created = tmp_path / BUILD_EXE_DIR / f"12345{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_deprecated_behavior(tmp_path: Path) -> None:
    """Test cxfreeze deprecated behavior."""
    create_package(tmp_path, SOURCE)
    tmp_path.joinpath("test.py").rename(tmp_path / "test2")
    output = run_command(
        tmp_path, "cxfreeze --install-dir=dist --excludes=tkinter test2"
    )

    file_created = tmp_path / "dist" / f"test2{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_deprecated_option(tmp_path: Path) -> None:
    """Test cxfreeze deprecated option."""
    create_package(tmp_path, SOURCE)
    output = run_command(
        tmp_path,
        "cxfreeze -c -O -OO test.py --target-dir=dist --excludes=tkinter",
    )
    assert "WARNING: deprecated" in output

    file_created = tmp_path / "dist" / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_without_options(tmp_path: Path) -> None:
    """Test cxfreeze without options."""
    create_package(tmp_path, SOURCE)
    with pytest.raises(CalledProcessError):
        run_command(tmp_path, "cxfreeze")


SOURCE_TEST_PATH = f"""
advanced_1.py
    print("Hello from cx_Freeze Advanced #1")
    module = __import__("testfreeze_1")
advanced_2.py
    print("Hello from cx_Freeze Advanced #2")
    module = __import__("testfreeze_2")
modules/testfreeze_1.py
    print("Test freeze module #1")
modules/testfreeze_2.py
    print("Test freeze module #2")
pyproject.toml
    [project]
    name = "advanced"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "advanced_1.py"

    [[tool.cxfreeze.executables]]
    script = "advanced_2.py"

    [tool.cxfreeze.build_exe]
    build_exe = "dist"
    excludes = ["tkinter", "unittest"]
    includes = ["testfreeze_1", "testfreeze_2"]
    #silent = true
command
    cxfreeze build_exe --include-path=modules --default-path={os.pathsep.join(sys.path)}
"""
OUTPUT1 = "Hello from cx_Freeze Advanced #1\nTest freeze module #1\n"
OUTPUT2 = "Hello from cx_Freeze Advanced #2\nTest freeze module #2\n"


def test_cxfreeze_include_path(tmp_path: Path) -> None:
    """Test cxfreeze."""
    create_package(tmp_path, SOURCE_TEST_PATH)
    output = run_command(tmp_path)

    executable = tmp_path / "dist" / f"advanced_1{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT1

    executable = tmp_path / "dist" / f"advanced_2{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output == OUTPUT2
