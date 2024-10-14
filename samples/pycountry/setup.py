"""A setup script to demonstrate build using pycountry."""

from __future__ import annotations

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
from cx_Freeze import setup

setup(
    name="test",
    version="0.1",
    description="cx_Freeze script to test pycountry",
    executables=["test.py"],
)
