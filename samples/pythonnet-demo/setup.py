"""
A setup script to create executables and demonstrate the use pythonnet.
"""

from __future__ import annotations

import sys

from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("helloform.py", icon="python-clear.ico", base=base),
    Executable("splitter.py", icon="python-clear.ico", base=base),
    Executable("wordpad.py", icon="python-clear.ico", base=base),
]

setup(
    name="pythonnet demos",
    version="0.1",
    description="https://github.com/pythonnet/pythonnet/tree/master/demo",
    executables=executables,
)
