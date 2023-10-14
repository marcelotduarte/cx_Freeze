"""Tests for some cx_Freeze.hooks."""
from __future__ import annotations

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
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SOURCE = """
test_manifest.py
    import sys

    winver = sys.getwindowsversion()
    print(f"Windows version: {winver.major}.{winver.minor}")
setup.py
    from cx_Freeze import Executable, setup
    setup(
        name="test_multiprocessing",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=[
            Executable("test_manifest.py"),
            Executable(
                "test_manifest.py",
                manifest="simple.manifest",
                target_name="test_simple_manifest",
            )
        ],
        options={"build_exe": {"excludes": ["tkinter"], "silent": True}}
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


def test_manifest(tmp_path: Path):
    """Test that the manifest is working correctly."""
    create_package(tmp_path, SOURCE)
    output = check_output(
        [sys.executable, "setup.py", "build_exe"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""

    # With the correct manifest, windows version return 10.0 for Windows 10
    executable = tmp_path / BUILD_EXE_DIR / f"test_manifest{suffix}"
    assert executable.is_file()
    output = check_output(
        [os.fspath(executable)], text=True, timeout=10, cwd=os.fspath(tmp_path)
    )
    print(output)
    winver = sys.getwindowsversion()
    expected = f"Windows version: {winver.major}.{winver.minor}"
    assert output.splitlines()[0].strip() == expected

    # With simple manifest, without "supportedOS Id", windows version returned
    # is the compatible version for Windows 8.1, ie, 6.2
    executable = tmp_path / BUILD_EXE_DIR / f"test_simple_manifest{suffix}"
    assert executable.is_file()
    output = check_output(
        [os.fspath(executable)], text=True, timeout=10, cwd=os.fspath(tmp_path)
    )
    print(output)
    expected = "Windows version: 6.2"
    assert output.splitlines()[0].strip() == expected
