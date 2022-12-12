"""Code to test that the plist_items option is working correctly."""

from __future__ import annotations

import plistlib
import sys

import pytest
from data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE

from cx_Freeze.sandbox import run_setup


@pytest.mark.skipif(sys.platform != "darwin", reason="Macos tests")
def test_plist_items(fix_test_samples_path):
    """Test that the plist_items option is working correctly."""

    setup_path = fix_test_samples_path / "plist_items"

    run_setup(setup_path / "setup.py", ["bdist_mac"])

    # Test that the additional keys were correctly added to the plist.
    path = setup_path / f"{BUILD_DIR}/{BUNDLE_NAME}.app/Contents/Info.plist"
    contents = plistlib.loads(path.read_bytes())
    assert contents[TEST_KEY] == TEST_VALUE
