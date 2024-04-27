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
    ("kwargs", "option", "result"),
    [
        pytest.param(
            {"install_dir": None},
            "install_dir",
            os.path.normpath(
                Path(os.getenv("PROGRAMFILES"), "foo")
                if sys.platform == "win32"
                else Path(get_config_var("base"), "lib/foo-0.0")
            ),
            id="install-dir=none",
        ),
        pytest.param(
            {"install_dir": "dist"},
            "install_dir",
            "dist",
            id="install-dir=dist",
        ),
    ],
)
def test_install_exe_finalize_options(
    kwargs: dict[str, ...], option: str, result
) -> None:
    """Test the install_exe finalize_options."""
    dist = Distribution(DIST_ATTRS)
    cmd = install_exe(dist, **kwargs)
    cmd.finalize_options()
    cmd.ensure_finalized()
    assert getattr(cmd, option) == result
    assert len(cmd.get_inputs()) > 0
    assert cmd.get_outputs() == []
