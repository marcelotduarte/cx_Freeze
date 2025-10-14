"""Tests for 'cxfreeze' command."""

from __future__ import annotations

import os
import sys

SOURCE = """
test.py
    print("Hello from cx_Freeze")
"""


def test_cxfreeze(tmp_package) -> None:
    """Test cxfreeze."""
    tmp_package.create(SOURCE)
    command = "cxfreeze --script test.py --target-dir=dist"
    command += " --excludes=tkinter,unittest --include-msvcr"
    tmp_package.freeze(command)

    executable = tmp_package.executable_in_dist("test")
    assert executable.is_file(), f"file not found: {executable}"

    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


def test_cxfreeze_help(tmp_package) -> None:
    """Test cxfreeze help."""
    tmp_package.create(SOURCE)
    result = tmp_package.freeze("cxfreeze --help")
    result.stdout.fnmatch_lines("usage: *")


def test_cxfreeze_additional_help(tmp_package) -> None:
    """Test cxfreeze additional help."""
    tmp_package.create(SOURCE)
    result = tmp_package.freeze("cxfreeze build_exe --help")
    result.stdout.fnmatch_lines("*--help-commands*")


def test_cxfreeze_debug_verbose(tmp_package) -> None:
    """Test cxfreeze --debug --verbose."""
    tmp_package.create(SOURCE)
    command = "cxfreeze --script test.py --debug --verbose"
    command += " --excludes=tkinter,unittest --include-msvcr"
    tmp_package.freeze(command)

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


def test_cxfreeze_target_name_not_isidentifier(tmp_package) -> None:
    """Test cxfreeze --target-name not isidentifier, but valid filename."""
    tmp_package.create(SOURCE)
    command = "cxfreeze --script test.py --target-name=12345"
    command += " --excludes=tkinter,unittest --include-msvcr"
    tmp_package.freeze(command)

    file_created = tmp_package.executable("12345")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


def test_cxfreeze_deprecated_behavior(tmp_package) -> None:
    """Test cxfreeze deprecated behavior."""
    tmp_package.create(SOURCE)
    tmp_package.path.joinpath("test.py").rename(tmp_package.path / "test2")
    command = "cxfreeze --install-dir=dist test2"
    command += " --excludes=tkinter,unittest --include-msvcr"
    tmp_package.freeze(command)

    file_created = tmp_package.executable_in_dist("test2")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


def test_cxfreeze_deprecated_option(tmp_package) -> None:
    """Test cxfreeze deprecated option."""
    tmp_package.create(SOURCE)
    command = "cxfreeze -c -O -OO test.py --target-dir=dist"
    command += " --excludes=tkinter,unittest --include-msvcr"
    result = tmp_package.freeze(command)
    assert "WARNING: deprecated" in str(result.stdout)

    file_created = tmp_package.executable_in_dist("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")


def test_cxfreeze_without_options(tmp_package) -> None:
    """Test cxfreeze without options."""
    tmp_package.create(SOURCE)
    result = tmp_package.freeze("cxfreeze")
    assert result.ret > 0


SOURCE_TEST_PATH = """
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
    include_msvcr = true
    silent = true
"""
OUTPUT0 = "Hello from cx_Freeze Advanced #{}"
OUTPUT1 = "Test freeze module #{}"


def test_cxfreeze_include_path(tmp_package) -> None:
    """Test cxfreeze."""
    tmp_package.create(SOURCE_TEST_PATH)
    tmp_package.freeze(
        "cxfreeze build_exe"
        f" --include-path=modules --default-path={os.pathsep.join(sys.path)}"
    )

    executable = tmp_package.executable_in_dist("advanced_1")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines([OUTPUT0.format(1), OUTPUT1.format(1)])

    executable = tmp_package.executable_in_dist("advanced_2")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=10)
    result.stdout.fnmatch_lines([OUTPUT0.format(2), OUTPUT1.format(2)])
