# relimport.py is a very simple script that tests importing using relative
# imports (available in Python 2.5 and up)
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from cx_Freeze import Executable, setup

executables = [Executable("relimport.py")]

setup(
    name="relimport",
    version="0.1",
    description="Sample cx_Freeze script for relative imports",
    executables=executables,
)
