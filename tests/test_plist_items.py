"""Code to test that the plist_items option is working correctly."""
from __future__ import annotations

import os
import plistlib
import sys
from importlib import import_module
from pathlib import Path
from subprocess import check_output

import pytest
from generate_samples import PLIST_ITEMS_TEST, create_package


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS tests")
def test_plist_items(tmp_path: Path):
    """Test that the plist_items option is working correctly."""
    create_package(tmp_path, source=PLIST_ITEMS_TEST[4])
    output = check_output(
        [sys.executable, "setup.py", "bdist_mac"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    print(output)
    # Test that the additional keys were correctly added to the plist.
    sys.path.insert(0, os.fspath(tmp_path))
    data = import_module("plist_data")
    path = f"{data.BUILD_DIR}/{data.BUNDLE_NAME}.app/Contents/Info.plist"
    contents = plistlib.loads(tmp_path.joinpath(path).read_bytes())
    assert contents[data.TEST_KEY] == data.TEST_VALUE
