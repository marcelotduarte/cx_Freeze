"""A very simple setup script to create a single executable.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python"""

from __future__ import annotations

from cx_Freeze import Executable, setup

executables = [Executable("hello.py")]

setup(
    name="hello",
    version="0.1.2.3",
    description="Sample cx_Freeze script",
    executables=executables,
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "replace_paths": [("*", "")],
            "silent": True,
        }
    },
)
