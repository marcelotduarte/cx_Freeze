# A simple setup script to create an executable using PySide2. This also
# demonstrates how to use include_files, zip_include_packages and excludes
# to get minimal package size
#
# PySide2app.py is a very simple type of PySide2 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
import os
import sys

import PySide2
from cx_Freeze import setup, Executable

plugins_path = os.path.join(PySide2.__path__[0], "plugins")


base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {
    "build_exe": {
        "include_files": [
            os.path.join(plugins_path, "platforms")
        ],  # additional plugins needed by qt at runtime
        "zip_include_packages": [
            "PySide2",
            "shiboken2",
            "encodings",
        ],  # reduce size of packages that are used
        "excludes": [
            "tkinter",
            "unittest",
            "email",
            "http",
            "xml",
            "pydoc",
            "pdb",
        ],  # exclude packages that are not really needed
    }
}

executables = [Executable("PySide2app.py", base=base)]

setup(
    name="simple_PySide2",
    version="0.1",
    description="Sample cx_Freeze PySide2 script",
    options=options,
    executables=executables,
)
