# Code to test that the plist_items option is working correctly.

import setuptools
import distutils.core
import os, platform, sys
from data import TEST_KEY, TEST_VALUE, BUILD_DIR, BUNDLE_NAME

if platform.system() != "Darwin":
    print("Test only applies to Darwin.")
    sys.exit(1)

import plistlib

print("Testing plist_items option with bdist_mac.")

distutils.core.run_setup("setup.py", ["bdist_mac"])

# Test that the additional keys were correctly added to the plist.
name = os.path.join(BUILD_DIR, f"{BUNDLE_NAME}.app", "Contents", "Info.plist")
with open(name, "rb") as f:
    contents = plistlib.load(f, fmt=None, use_builtin_types=False)

try:
    assert contents[TEST_KEY] == TEST_VALUE
    print("Test Successful")
except AssertionError:
    print("Error, keys not correctly added to plist.")
