# A simple setup script to create an executable running wxPython. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# wxapp.py is a very simple 'Hello, world' type wxPython application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

from __future__ import annotations

import sys

from cx_Freeze import Executable, setup

base = "Win32GUI" if sys.platform == "win32" else None

options = {
    "build_exe": {
        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        "excludes": [
            "gi",
            "gtk",
            "PyQt4",
            "PyQt5",
            "PyQt6",
            "PySide2",
            "PySide6",
            "shiboken2",
            "shiboken6",
            "tkinter",
        ]
    }
}

executables = [Executable("test_wx.py", base=base)]

setup(
    name="wxapp_sample",
    version="0.1",
    description="Sample cx_Freeze wxPython script",
    executables=executables,
    options=options,
)
