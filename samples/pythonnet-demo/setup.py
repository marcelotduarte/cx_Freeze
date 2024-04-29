"""A setup script to create executables and demonstrate the use pythonnet."""

from cx_Freeze import Executable, setup

executables = [
    Executable("helloform.py", icon="python-clear.ico", base="gui"),
    Executable("splitter.py", icon="python-clear.ico", base="gui"),
    Executable("wordpad.py", icon="python-clear.ico", base="gui"),
]

setup(
    name="pythonnet demos",
    version="0.1",
    description="https://github.com/pythonnet/pythonnet/tree/master/demo",
    executables=executables,
)
