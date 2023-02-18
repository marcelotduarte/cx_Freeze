"""A setup script to demonstrate the use of sqlite3"""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

import sys
from pathlib import Path
from sysconfig import get_platform

from cx_Freeze import Executable, setup

arch_dir = Path.cwd() / f"lib-{get_platform()}"
search_path = [arch_dir] + sys.path

setup(
    name="test_sqlite3",
    version="0.4",
    description="cx_Freeze script to test sqlite3",
    executables=[Executable("test_sqlite3.py")],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "path": search_path,
            "replace_paths": [("*", "")],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
