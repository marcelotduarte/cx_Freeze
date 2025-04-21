"""Tests for cx_Freeze.command.install_exe."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from sysconfig import get_config_var

import pytest
from setuptools import Distribution

from cx_Freeze.command.install_exe import install_exe

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "executables": ["hello.py"],
    "script_name": "setup.py",
}


@pytest.mark.parametrize(
    ("install_dir", "expected"),
    [
        pytest.param(
            None,
            os.path.normpath(
                Path(os.getenv("PROGRAMFILES"), "foo")
                if sys.platform == "win32"
                else Path(get_config_var("base"), "lib/foo-0.0")
            ),
            id="install-dir=none",
        ),
        pytest.param("dist", "dist", id="install-dir=dist"),
    ],
)
def test_install_exe_finalize_options(install_dir: str, expected: str) -> None:
    """Test the install_exe finalize_options."""
    dist = Distribution(DIST_ATTRS)
    cmd = install_exe(dist, install_dir=install_dir)
    cmd.finalize_options()
    cmd.ensure_finalized()
    returned = cmd.install_dir
    inputs = cmd.get_inputs()
    outputs = cmd.get_outputs()
    assert returned == expected
    assert len(inputs) > 0
    assert outputs == []
