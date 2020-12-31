"""
A setup script to demonstrate build using pytz
This version requires the zoneinfo in the file system
"""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

setup(
    name="test_pytz_zip",
    version="0.3",
    description="cx_Freeze script to test pytz",
    executables=[Executable("test_pytz.py")],
)
