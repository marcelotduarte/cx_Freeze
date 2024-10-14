"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command
from setuptools import Distribution

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX
from cx_Freeze.exception import OptionError

if TYPE_CHECKING:
    from pathlib import Path

SOURCE = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup

    setup(executables=["test.py"])
command
    python setup.py build
"""


def test_build(tmp_path: Path) -> None:
    """Test a simple build."""
    create_package(tmp_path, SOURCE)

    # first run, count the files
    output = run_command(tmp_path)

    build_exe_dir = tmp_path / BUILD_EXE_DIR

    file_created = build_exe_dir / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    files1 = sorted(build_exe_dir.rglob("*"))

    # second run to test target_dir "starts in a clean directory"
    output = run_command(tmp_path)

    file_created = build_exe_dir / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
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
    tmp_path: Path,
    monkeypatch,
    build_args: list[str],
    expected_exception,
    expected_match: str,
) -> None:
    """Test the build with an option that raises an exception."""
    create_package(tmp_path, SOURCE)
    monkeypatch.chdir(tmp_path)
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
