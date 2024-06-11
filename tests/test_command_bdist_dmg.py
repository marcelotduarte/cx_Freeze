"""Tests for cx_Freeze.command.bdist_dmg."""

from __future__ import annotations

import sys
from pathlib import Path
from subprocess import run

import pytest
from generate_samples import run_command

bdist_dmg = pytest.importorskip(
    "cx_Freeze.command.bdist_dmg", reason="macOS tests"
).bdist_dmg

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
def test_bdist_dmg(datafiles: Path) -> None:
    """Test the simple sample with bdist_dmg."""
    name = "hello"
    version = "0.1.2.3"
    dist_created = datafiles / "build"

    process = run(
        [sys.executable, "setup.py", "bdist_dmg"],
        text=True,
        capture_output=True,
        check=False,
        cwd=datafiles,
    )
    if process.returncode != 0:
        expected_err = "hdiutil: create failed - Resource busy"
        if expected_err in process.stderr:
            pytest.xfail(expected_err)
        else:
            pytest.fail(process.stderr)

    base_name = f"{name}-{version}"
    file_created = dist_created / f"{base_name}.dmg"
    assert file_created.is_file(), f"{base_name}.dmg"
