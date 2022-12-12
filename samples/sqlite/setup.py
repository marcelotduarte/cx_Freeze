"""A setup script to demonstrate the use of sqlite3"""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from cx_Freeze import Executable, setup

setup(
    name="test_sqlite3",
    version="0.3",
    description="cx_Freeze script to test sqlite3",
    executables=[Executable("test_sqlite3.py")],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "replace_paths": [("*", "")],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
