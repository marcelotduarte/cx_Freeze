"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

import ctypes
import os
import sys
from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR
from cx_Freeze.dep_parser import PEParser

if TYPE_CHECKING:
    from pathlib import Path

if sys.platform != "win32":
    pytest.skip(reason="Windows tests", allow_module_level=True)

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
            Executable(
                "test_manifest.py",
                uac_admin=True,
                uac_uiaccess=True,
                target_name="test_uac_uiaccess",
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
command
    python setup.py build_exe --excludes=tkinter
"""


@pytest.fixture(scope="module")
def tmp_manifest(tmp_path_factory) -> Path:
    """Temporary path to build test manifest."""
    tmp_path = tmp_path_factory.mktemp("manifest")
    create_package(tmp_path, SOURCE)
    run_command(tmp_path)
    return tmp_path / BUILD_EXE_DIR


def test_manifest(tmp_manifest: Path) -> None:
    """With the correct manifest, windows version return 10.0 in Windows 10."""
    executable = tmp_manifest / "test_manifest.exe"
    assert executable.is_file()
    output = run_command(tmp_manifest, executable, timeout=10)
    winver = sys.getwindowsversion()
    expected = f"Windows version: {winver.major}.{winver.minor}"
    assert output.splitlines()[0].strip() == expected


def test_simple_manifest(tmp_manifest: Path) -> None:
    """With simple manifest, without "supportedOS Id", windows version returned
    is the compatible version for Windows 8.1, ie, 6.2.
    """
    if os.environ.get("CX_FREEZE_BIND", "") == "imagehlp":
        pytest.skip(reason="Use of lief is disabled")
    pytest.importorskip("lief", reason="Depends on extra package: lief")

    executable = tmp_manifest / "test_simple_manifest.exe"
    assert executable.is_file()
    output = run_command(tmp_manifest, executable, timeout=10)
    expected = "Windows version: 6.2"
    assert output.splitlines()[0].strip() == expected

    parser = PEParser([], [])
    manifest = parser.read_manifest(executable)
    simple = tmp_manifest.parent.parent.joinpath("simple.manifest")
    assert manifest == simple.read_bytes().decode()


def test_uac_admin(tmp_manifest: Path) -> None:
    """With the uac_admin, should return WinError 740 - requires elevation."""
    if os.environ.get("CX_FREEZE_BIND", "") == "imagehlp":
        pytest.skip(reason="Use of lief is disabled")
    pytest.importorskip("lief", reason="Depends on extra package: lief")

    executable = tmp_manifest / "test_uac_admin.exe"
    assert executable.is_file()
    if ctypes.windll.shell32.IsUserAnAdmin():
        pytest.xfail(reason="User is admin")
    with pytest.raises(OSError, match="[WinError 740]"):
        run_command(tmp_manifest, executable, timeout=10)


def test_uac_uiaccess(tmp_manifest: Path) -> None:
    """With the uac_uiaccess, should return WinError 740."""
    if os.environ.get("CX_FREEZE_BIND", "") == "imagehlp":
        pytest.skip(reason="Use of lief is disabled")
    pytest.importorskip("lief", reason="Depends on extra package: lief")

    executable = tmp_manifest / "test_uac_uiaccess.exe"
    assert executable.is_file()
    if ctypes.windll.shell32.IsUserAnAdmin():
        pytest.xfail(reason="User is admin")
    with pytest.raises(OSError, match="[WinError 740]"):
        run_command(tmp_manifest, executable, timeout=10)
