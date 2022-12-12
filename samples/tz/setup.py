"""
A setup script to demonstrate build using zoneinfo/tzdata
This version requires the zoneinfo in the file system
"""
from __future__ import annotations

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
from cx_Freeze import Executable, setup

setup(
    name="test_tz",
    version="0.1",
    description="cx_Freeze script to test zoneinfo/tzdata",
    executables=[Executable("test_tz.py")],
)
