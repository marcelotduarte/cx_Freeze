"""A setup script to demonstrate build using pytz
This version requires the zoneinfo in the file system.
"""

from __future__ import annotations

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
from cx_Freeze import setup

setup(
    name="test_pytz_zip",
    version="0.3",
    description="cx_Freeze script to test pytz",
    executables=["test_pytz.py"],
)
