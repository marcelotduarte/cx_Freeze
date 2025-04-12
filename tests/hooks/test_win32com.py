"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import sys

import pytest

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)


def test_win32com(tmp_package) -> None:
    """Test that the win32com is working correctly."""
    tmp_package.create_from_sample("win32com")
    # pywin32 must be installed on venv
    tmp_package.install("pywin32", isolated=False)
    output = tmp_package.run("cxfreeze --script test_win32com.py --silent")
    executable = tmp_package.executable("test_win32com")
    assert executable.is_file()

    output = tmp_package.run(executable, timeout=10)
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
command
    cxfreeze --script test.py --silent
"""


def test_win32com_shell(tmp_package) -> None:
    """Test if zoneinfo hook is working correctly."""
    tmp_package.create(SOURCE_WIN32COM_SHELL)
    # pywin32 must be installed on venv
    tmp_package.install("pywin32", isolated=False)
    output = tmp_package.run()
    executable = tmp_package.executable("test")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=10)
    print(output)
    lines = output.splitlines()
    assert lines[0].startswith("<PyIShellLink at")
