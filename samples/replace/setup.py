"""A very simple setup script to create a single executable.

test_replace.py is a very simple script which also displays the
environment in which the script runs.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python
"""

from cx_Freeze import setup

setup(
    name="hello",
    version="0.1.2.3",
    description="Sample cx_Freeze script",
    executables=["test_replace.py"],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "replace_paths": [("*", "")],
            "silent": True,
        }
    },
)
