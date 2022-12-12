"""
A simple setup script to create an executable using PyQt5 QtWebEngineWidgets.
This also demonstrates how to use excludes to get minimal package size.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

from __future__ import annotations

import sys

from cx_Freeze import Executable, setup

base = "Win32GUI" if sys.platform == "win32" else None

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "excludes": [
            "tkinter",
            "unittest",
            "email",
            "http",
            "xml",
            "pydoc",
        ],
        "zip_include_packages": ["PyQt5"],
    },
    "bdist_mac": {"bundle_name": "PyQt5 Webengine Test"},
}

executables = [
    Executable("simplebrowser.py", target_name="test_simplebrowser")
]

setup(
    name="simplebrowser",
    version="0.1",
    description="cx_Freeze and PyQt5 Webengine sample",
    options=options,
    executables=executables,
)
