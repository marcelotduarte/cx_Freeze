"""A setup script to demonstrate build using orjson."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from cx_Freeze import setup

setup(
    name="test_orjson",
    version="0.1",
    description="cx_Freeze script to test orjson",
    executables=["test_orjson.py"],
    options={"build_exe": {"excludes": ["tkinter"]}},
)
