"""Tests for cx_Freeze.command.bdist_mac."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from generate_samples import run_command

bdist_mac = pytest.importorskip(
    "cx_Freeze.command.bdist_mac", reason="macOS tests"
).bdist_mac

if sys.platform != "darwin":
    pytest.skip(reason="macOS tests", allow_module_level=True)

DIST_ATTRS = {
    "name": "foo",
    "version": "0.0",
    "description": "cx_Freeze script to test bdist_mac",
    "executables": ["hello.py"],
    "script_name": "setup.py",
    "author": "Marcelo Duarte",
    "author_email": "marcelotduarte@users.noreply.github.com",
    "url": "https://github.com/marcelotduarte/cx_Freeze/",
}
SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"


@pytest.mark.datafiles(SAMPLES_DIR / "simple")
def test_bdist_mac(datafiles: Path) -> None:
    """Test the simple sample with bdist_mac."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = datafiles / "build"

    run_command(datafiles, "python setup.py bdist_mac")

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}.app"
    assert file_created.is_dir(), f"{base_name}.app"
