"""Code to test that the plist_items option is working correctly."""

from __future__ import annotations

import os
import plistlib
import sys
from importlib import import_module

import pytest

from cx_Freeze._compat import IS_MACOS

PLIST_TEST = """\
plist_data.py
    TEST_KEY = "TestKey"
    TEST_VALUE = "TextValue"
    BUILD_DIR = "Built_App"
    BUNDLE_NAME = "Bundle"
hello.py
    import sys
    from datetime import datetime
    print("Hello from cx_Freeze")
    print(f"The current date is {datetime.today():%B %d, %Y %H:%M:%S}")
    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print("ARGUMENTS:")
    for a in sys.argv: print(f"{a}")
    print()
    print("PATH:")
    for p in sys.path: print(f"{p}")
    print()
setup.py
    from plist_data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE
    from cx_Freeze import setup
    executables = ["hello.py"]
    setup(
        name="hello",
        version="0.1",
        description="Sample cx_Freeze script",
        options={
            "build": {"build_base": BUILD_DIR},
            "bdist_mac": {
                "bundle_name": BUNDLE_NAME,
                "plist_items": [(TEST_KEY, TEST_VALUE)],
            },
        },
        executables=executables,
    )
command
    python setup.py bdist_mac
"""


@pytest.mark.skipif(not IS_MACOS, reason="macOS test")
def test_plist_items(tmp_package) -> None:
    """Test that the plist_items option is working correctly."""
    tmp_package.create(PLIST_TEST)
    tmp_package.run()
    # Test that the additional keys were correctly added to the plist.
    sys.path.insert(0, os.fspath(tmp_package.path))
    data = import_module("plist_data")
    path = f"{data.BUILD_DIR}/{data.BUNDLE_NAME}.app/Contents/Info.plist"
    contents = plistlib.loads(tmp_package.path.joinpath(path).read_bytes())
    assert contents[data.TEST_KEY] == data.TEST_VALUE
