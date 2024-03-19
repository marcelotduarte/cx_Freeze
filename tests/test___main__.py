"""Tests for 'python -m cx_Freeze'."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from generate_samples import create_package, run_command

if TYPE_CHECKING:
    from pathlib import Path

SUFFIX = ".exe" if sys.platform == "win32" else ""

SOURCE = """
test.py
    print("Hello from cx_Freeze")
command
    python -m cx_Freeze test.py --target-dir=dist --excludes=tkinter
"""


def test___main__(tmp_path: Path) -> None:
    """Test __main__."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)

    file_created = tmp_path / "dist" / f"test{SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
