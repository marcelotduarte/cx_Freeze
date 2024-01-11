"""Tests for some cx_Freeze.hooks."""
from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

from generate_samples import create_package, run_command

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"
IS_WINDOWS = sys.platform == "win32"
SUFFIX = ".exe" if IS_WINDOWS else ""

SOURCE = """
test_ssl.py
    import os
    import ssl

    print('Hello from cx_Freeze')
    print(ssl.__name__, ssl.OPENSSL_VERSION)
    ssl_paths = ssl.get_default_verify_paths()
    print(ssl_paths.openssl_cafile)
    print(os.environ.get('SSL_CERT_FILE'))
setup.py
    from cx_Freeze import Executable, setup
    setup(
        executables=[Executable("test_ssl.py")],
        options={"build_exe": {"excludes": ["tkinter"], "silent": True}}
    )
"""


def test_ssl(tmp_path: Path):
    """Test that the ssl is working correctly."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)
    executable = tmp_path / BUILD_EXE_DIR / f"test_ssl{SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("ssl")
    assert output.splitlines()[2] != ""
