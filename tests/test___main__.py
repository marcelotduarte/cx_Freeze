"""Tests for 'python -m cx_Freeze'."""

from __future__ import annotations

SOURCE = """
test.py
    print("Hello from cx_Freeze")
pyproject.toml
    [project]
    name = "test"
    version = "0.1.2.3"
    description = "Sample cx_Freeze script"

    [[tool.cxfreeze.executables]]
    script = "test.py"

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
command
    python -m cx_Freeze build_exe --target-dir=dist
"""


def test___main__(tmp_package) -> None:
    """Test __main__."""
    tmp_package.create(SOURCE)
    tmp_package.freeze()

    file_created = tmp_package.executable_in_dist("test")
    assert file_created.is_file(), f"file not found: {file_created}"

    result = tmp_package.run(file_created, timeout=10)
    result.stdout.fnmatch_lines("Hello from cx_Freeze")
