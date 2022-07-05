"""
A simple setup script to create an executable using PySide6 WebEngineWidgets.
This also demonstrates how to use excludes to get minimal package size.

simplebrowser.py is the "PySide6 WebEngineWidgets Example".

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

import sys

from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"

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
        "zip_include_packages": ["PySide6"],
    }
}

executables = [
    Executable("simplebrowser.py", target_name="test_simplebrowser")
]

setup(
    name="simplebrowser",
    version="0.1",
    description="Sample cx_Freeze PySide6 simplebrowser script",
    options=options,
    executables=executables,
)
