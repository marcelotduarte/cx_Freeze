"""
A setup script to create executables and demonstrate the use pythonnet.
"""

from cx_Freeze import setup, Executable

executables = [
    Executable("helloform.py", icon="python-clear.ico"),
    Executable("splitter.py", icon="python-clear.ico"),
    Executable("wordpad.py", icon="python-clear.png"),
]

setup(
    name="pythonnet demos",
    version="0.1",
    description="https://github.com/pythonnet/pythonnet/tree/master/demo",
    executables=executables,
)
