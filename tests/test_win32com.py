"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

from pathlib import Path

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


pytest.importorskip("win32com", reason="Depends on extra package: pywin32")


@pytest.mark.datafiles(SAMPLES_DIR / "win32com")
def test_win32com(datafiles: Path) -> None:
    """Test that the win32com is working correctly."""
    output = run_command(
        datafiles, "cxfreeze --script test_win32com.py --silent"
    )
    executable = datafiles / BUILD_EXE_DIR / f"test_win32com{EXE_SUFFIX}"
    assert executable.is_file()

    output = run_command(datafiles, executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("Sent and received 'Hello from cx_Freeze'")
    assert lines[-1].startswith("Everything seemed to work!")
    assert len(lines) == 5, lines


SOURCE_WIN32COM_SHELL = """
test.py
    from win32com.shell import shell
    import pythoncom
    shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink
    )
    print(shortcut)
"""


def test_win32com_shell(tmp_path: Path) -> None:
    """Test if zoneinfo hook is working correctly."""
    create_package(tmp_path, SOURCE_WIN32COM_SHELL)
    output = run_command(tmp_path, "cxfreeze --script test.py --silent")
    executable = tmp_path / BUILD_EXE_DIR / f"test{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    print(output)
    lines = output.splitlines()
    assert lines[0].startswith("<PyIShellLink at")
