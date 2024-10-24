"""A setup script to demonstrate build using requests."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import Executable, setup

setup(executables=[Executable("test_requests.py")])
