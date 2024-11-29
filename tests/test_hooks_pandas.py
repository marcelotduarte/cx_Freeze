"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

from pathlib import Path

import pytest
from generate_samples import run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


pytest.importorskip("pandas", reason="Depends on extra package: pandas")
pytest.importorskip("numpy", reason="Depends on extra package: numpy")


@pytest.mark.datafiles(SAMPLES_DIR / "pandas")
def test_pandas(datafiles: Path) -> None:
    """Test that the pandas/numpy is working correctly."""
    output = run_command(datafiles, "python setup.py build_exe -O2")
    executable = datafiles / BUILD_EXE_DIR / f"test_pandas{EXE_SUFFIX}"
    assert executable.is_file()

    output = run_command(datafiles, executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("pandas version")
    assert len(lines) == 8, lines[2:]
