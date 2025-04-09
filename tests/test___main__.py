"""Tests for 'python -m cx_Freeze'."""

from __future__ import annotations

SOURCE = """
test.py
    print("Hello from cx_Freeze")
command
    python -m cx_Freeze test.py --target-dir=dist --excludes=tkinter
"""


def test___main__(tmp_package) -> None:
    """Test __main__."""
    tmp_package.create(SOURCE)
    output = tmp_package.run()

    file_created = tmp_package.executable_in_dist("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    output = tmp_package.run(file_created, timeout=10)
    assert output.startswith("Hello from cx_Freeze")
