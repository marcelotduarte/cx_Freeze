"""Tests for 'cxfreeze' command."""

from __future__ import annotations

import os
import sys
from subprocess import CalledProcessError

import pytest

SOURCE = """
test.py
    print("Hello from cx_Freeze")
command
    cxfreeze --script test.py --target-dir=dist --excludes=tkinter
"""


def test_cxfreeze(tmp_package) -> None:
    """Test cxfreeze."""
    tmp_package.create(SOURCE)
    output = tmp_package.run()

    file_created = tmp_package.executable_in_dist("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_help(tmp_package) -> None:
    """Test cxfreeze help."""
    tmp_package.create(SOURCE)
    output = tmp_package.run("cxfreeze --help")
    assert output.startswith("usage")


def test_cxfreeze_additional_help(tmp_package) -> None:
    """Test cxfreeze additional help."""
    tmp_package.create(SOURCE)
    output = tmp_package.run("cxfreeze build_exe --help")
    assert "usage: " in output


def test_cxfreeze_debug_verbose(tmp_package) -> None:
    """Test cxfreeze --debug --verbose."""
    tmp_package.create(SOURCE)
    output = tmp_package.run(
        "cxfreeze --script test.py --debug --verbose --excludes=tkinter"
    )

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_target_name_not_isidentifier(tmp_package) -> None:
    """Test cxfreeze --target-name not isidentifier, but valid filename."""
    tmp_package.create(SOURCE)
    output = tmp_package.run(
        "cxfreeze --script test.py --target-name=12345 --excludes=tkinter",
    )

    file_created = tmp_package.executable("12345")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_deprecated_behavior(tmp_package) -> None:
    """Test cxfreeze deprecated behavior."""
    tmp_package.create(SOURCE)
    tmp_package.path.joinpath("test.py").rename(tmp_package.path / "test2")
    output = tmp_package.run(
        "cxfreeze --install-dir=dist --excludes=tkinter test2"
    )

    file_created = tmp_package.executable_in_dist("test2")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_deprecated_option(tmp_package) -> None:
    """Test cxfreeze deprecated option."""
    tmp_package.create(SOURCE)
    output = tmp_package.run(
        "cxfreeze -c -O -OO test.py --target-dir=dist --excludes=tkinter",
    )
    assert "WARNING: deprecated" in output

    file_created = tmp_package.executable_in_dist("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")


def test_cxfreeze_without_options(tmp_package) -> None:
    """Test cxfreeze without options."""
    tmp_package.create(SOURCE)
    with pytest.raises(CalledProcessError):
        tmp_package.run("cxfreeze")


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


def test_cxfreeze_include_path(tmp_package) -> None:
    """Test cxfreeze."""
    tmp_package.create(SOURCE_TEST_PATH)
    output = tmp_package.run()

    executable = tmp_package.executable_in_dist("advanced_1")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output == OUTPUT1

    executable = tmp_package.executable_in_dist("advanced_2")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    assert output == OUTPUT2
