"""A simple setup script to create an executable using pandas. This also
demonstrates how to use excludes to get minimal package size.

test_pandas.py is a very simple type of pandas application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

import sys

from cx_Freeze import setup

sys.setrecursionlimit(sys.getrecursionlimit() * 10)

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
    },
}

setup(
    name="test_pandas",
    version="0.1.0.1",
    description="Sample pandas script",
    executables=["test_pandas.py"],
    options=options,
)
