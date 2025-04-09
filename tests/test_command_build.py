"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

import pytest
from setuptools import Distribution

from cx_Freeze.exception import OptionError

SOURCE = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    setup(executables=["test.py"])
command
    python setup.py build
"""


def test_build(tmp_package) -> None:
    """Test a simple build."""
    tmp_package.create(SOURCE)

    # first run, count the files
    output = tmp_package.run()

    file_created = tmp_package.executable("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    build_exe_dir = file_created.parent
    files1 = sorted(build_exe_dir.rglob("*"))

    # second run to test target_dir "starts in a clean directory"
    output = tmp_package.run()

    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    files2 = sorted(build_exe_dir.rglob("*"))

    # compare
    assert files1 == files2


@pytest.mark.parametrize(
    ("build_args", "expected_exception", "expected_match"),
    [
        pytest.param(
            ["--build-exe="], OptionError, "[REMOVED]", id="build-exe="
        ),
    ],
)
def test_build_raises(
    tmp_package, build_args: list[str], expected_exception, expected_match: str
) -> None:
    """Test the build with an option that raises an exception."""
    tmp_package.create(SOURCE)
    dist = Distribution(
        {
            "executables": ["test.py"],
            "script_name": "setup.py",
            "script_args": ["build", *build_args],
        }
    )
    dist.parse_command_line()
    dist.dump_option_dicts()
    with pytest.raises(expected_exception, match=expected_match):
        dist.run_command("build")
