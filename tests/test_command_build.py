"""Tests for cx_Freeze.command.build."""
from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

from generate_samples import create_package, run_command

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SUFFIX = ".exe" if sys.platform == "win32" else ""

SOURCE = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup, Executable

    setup(executables=[Executable("test.py")])
command
    python setup.py build
"""


def test_build(tmp_path: Path):
    """Test a simple build."""
    create_package(tmp_path, SOURCE)

    # first run, count the files
    output = run_command(tmp_path)

    build_exe_dir = tmp_path / BUILD_EXE_DIR

    file_created = build_exe_dir / f"test{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    files1 = list(build_exe_dir.rglob("*"))

    # second run to test target_dir "starts in a clean directory"
    output = run_command(tmp_path)

    file_created = build_exe_dir / f"test{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")

    files2 = list(build_exe_dir.rglob("*"))

    # compare
    assert files1 == files2
