"""Tests for some cx_Freeze.hooks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path


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
    from cx_Freeze import setup
    setup(
        executables=["test_ssl.py"],
        options={"build_exe": {"excludes": ["tkinter"], "silent": True}}
    )
"""


def test_ssl(tmp_path: Path) -> None:
    """Test that the ssl is working correctly."""
    create_package(tmp_path, SOURCE)
    output = run_command(tmp_path)
    executable = tmp_path / BUILD_EXE_DIR / f"test_ssl{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    assert output.splitlines()[0] == "Hello from cx_Freeze"
    assert output.splitlines()[1].startswith("ssl")
    assert output.splitlines()[2] != ""
