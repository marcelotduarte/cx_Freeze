"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import run_command

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


pytest.importorskip("pandas", reason="Depends on extra package: pandas")
pytest.importorskip("numpy", reason="Depends on extra package: numpy")


@pytest.mark.datafiles(SAMPLES_DIR / "pandas")
def test_pandas(datafiles: Path) -> None:
    """Test that the pandas/numpy is working correctly."""
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)
    output = run_command(datafiles)
    executable = datafiles / BUILD_EXE_DIR / f"test_pandas{SUFFIX}"
    assert executable.is_file()

    output = run_command(datafiles, executable, timeout=10)
    print(output)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("pandas version")
    assert len(lines) == 8, lines[2:]
