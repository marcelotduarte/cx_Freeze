"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path

pytest.importorskip("argon2", reason="Depends on extra package: argon2-cffi")

SOURCE = """
test_argon2.py
    import argon2
    from importlib.metadata import distribution, version

    print("Hello from cx_Freeze")
    print(argon2.__name__, version("argon2-cffi"))
command
    cxfreeze --script test_argon2.py build_exe
"""


def test_argon2(tmp_path: Path) -> None:
    """Test if argon2-cffi is working correctly."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)
    executable = tmp_path / BUILD_EXE_DIR / f"test_argon2{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("argon2")
