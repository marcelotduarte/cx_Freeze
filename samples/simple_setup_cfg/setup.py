"""A very simple setup script to create a single executable.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python"""

from __future__ import annotations

from cx_Freeze import Executable, setup

setup(executables=[Executable("hello.py")])
