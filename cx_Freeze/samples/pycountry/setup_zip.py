"""
A setup script to demonstrate build using pycountry
"""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import distutils
import sys
import os

from cx_Freeze import setup, Executable

dir_name = f"exe.{distutils.util.get_platform()}-{sys.version[0:3]}.zip"
build_exe = os.path.join("build", dir_name)

setup(
    name="test_zip",
    version="0.1",
    description="cx_Freeze script to test pycountry",
    executables=[Executable("test.py")],
    options={
        "build_exe": {
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
            "build_exe": build_exe,
        }
    },
)
