"""
A simple setup script to create an executable using Zope which demonstrates
the use of namespace packages (auto detected).

qotd.py is a very simple type of Zope application

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

from __future__ import annotations

from cx_Freeze import Executable, setup

options = {
    "build_exe": {
        "excludes": ["tkinter"],
    }
}

executables = [Executable("qotd.py")]

setup(
    name="QOTD sample",
    version="1.1",
    description="QOTD sample for demonstrating use of namespace packages",
    options=options,
    executables=executables,
)
