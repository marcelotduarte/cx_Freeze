"""A setup script to demonstrate build using cffi (used by cryptography)."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from cx_Freeze import setup

setup(
    name="test_crypt",
    version="0.2",
    description="cx_Freeze script to test cryptography",
    executables=["test_crypt.py"],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
