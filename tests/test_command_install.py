"""Tests for cx_Freeze.command.install."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from generate_samples import create_package, run_command

from cx_Freeze._compat import EXE_SUFFIX

SOURCE = """
test.py
    print("Hello from cx_Freeze")
setup.py
    from cx_Freeze import setup, Executable

    setup(name="hello", executables=[Executable("test.py")])
command
    python setup.py install --prefix=base --root=root
"""


def test_install(tmp_path: Path) -> None:
    """Test a simple install."""
    create_package(tmp_path, SOURCE)

    if sys.platform == "win32":
        run_command(tmp_path, "python setup.py install --root=root")
        program_files = Path(os.getenv("PROGRAMFILES"))
        prefix = program_files.relative_to(program_files.anchor) / "hello"
    else:
        run_command(tmp_path)
        prefix = "base/lib/hello-0.0.0"
    install_dir = tmp_path / "root" / prefix

    file_created = install_dir / f"test{EXE_SUFFIX}"
    assert file_created.is_file(), f"file not found: {file_created}"

    output = run_command(tmp_path, file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
