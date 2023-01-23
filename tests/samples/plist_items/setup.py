"""A simple script demonstrating use of plist_items option."""

# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from data import BUILD_DIR, BUNDLE_NAME, TEST_KEY, TEST_VALUE

from cx_Freeze import Executable, setup

executables = [Executable("hello.py")]

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
