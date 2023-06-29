"""Code to test that the plist_items option is working correctly."""

from __future__ import annotations

import plistlib
import sys
from pathlib import Path

import pytest
from data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE

from cx_Freeze.sandbox import run_setup

FIXTURE_DIR = Path(__file__).resolve().parent


@pytest.mark.skipif(sys.platform != "darwin", reason="Macos tests")
@pytest.mark.datafiles(FIXTURE_DIR)
def test_plist_items(datafiles: Path):
    """Test that the plist_items option is working correctly."""
    run_setup(datafiles / "setup.py", ["bdist_mac"])
    # Test that the additional keys were correctly added to the plist.
    path = datafiles / f"{BUILD_DIR}/{BUNDLE_NAME}.app/Contents/Info.plist"
    contents = plistlib.loads(path.read_bytes())
    assert contents[TEST_KEY] == TEST_VALUE
