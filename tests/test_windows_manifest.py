"""Tests for some cx_Freeze.hooks."""
from __future__ import annotations

import ctypes
import os
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import create_package

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()

SOURCE = """
test_manifest.py
    import sys

    winver = sys.getwindowsversion()
    print(f"Windows version: {winver.major}.{winver.minor}")
setup.py
    from cx_Freeze import Executable, setup
    setup(
        name="test_manifest",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=[
            Executable("test_manifest.py"),
            Executable(
                "test_manifest.py",
                manifest="simple.manifest",
                target_name="test_simple_manifest",
            ),
            Executable(
                "test_manifest.py",
                uac_admin=True,
                target_name="test_uac_admin",
            ),
        ],
    )
simple.manifest
    <?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <assembly xmlns='urn:schemas-microsoft-com:asm.v1' manifestVersion='1.0'>
      <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
          <requestedPrivileges>
            <requestedExecutionLevel level='asInvoker' uiAccess='false' />
          </requestedPrivileges>
        </security>
      </trustInfo>
    </assembly>
"""


# pylint: disable=redefined-outer-name
@pytest.fixture(scope="module")
def tmp_manifest(tmp_path_factory):
    """Temporary path to build test manifest."""
    tmp_path = tmp_path_factory.mktemp("manifest")
    create_package(tmp_path, SOURCE)
    output = check_output(
        [sys.executable, "setup.py", "build_exe", "--excludes=tkinter"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    print(output)
    return tmp_path / f"build/exe.{PLATFORM}-{PYTHON_VERSION}"


def test_manifest(tmp_manifest: Path):
    """With the correct manifest, windows version return 10.0 in Windows 10."""
    executable = tmp_manifest / "test_manifest.exe"
    assert executable.is_file()
    output = check_output([os.fspath(executable)], text=True, timeout=10)
    print(output)
    winver = sys.getwindowsversion()
    expected = f"Windows version: {winver.major}.{winver.minor}"
    assert output.splitlines()[0].strip() == expected


def test_simple_manifest(tmp_manifest: Path):
    """With simple manifest, without "supportedOS Id", windows version returned
    is the compatible version for Windows 8.1, ie, 6.2.
    """
    executable = tmp_manifest / "test_simple_manifest.exe"
    assert executable.is_file()
    output = check_output([os.fspath(executable)], text=True, timeout=10)
    print(output)
    expected = "Windows version: 6.2"
    assert output.splitlines()[0].strip() == expected


def test_uac_admin(tmp_manifest: Path):
    """With the uac_admin, should return WinError 740 - requires elevation."""
    executable = tmp_manifest / "test_uac_admin.exe"
    assert executable.is_file()
    if ctypes.windll.shell32.IsUserAnAdmin():
        pytest.xfail(reason="User is admin")
    with pytest.raises(OSError, match="[WinError 740]"):
        check_output([os.fspath(executable)], text=True, timeout=10)
