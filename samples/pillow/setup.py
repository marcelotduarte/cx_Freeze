# A setup script to demonstrate the use of pillow
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from cx_Freeze import Executable, setup

setup(
    name="test_pillow",
    version="0.2",
    description="cx_Freeze script to test pillow (PIL)",
    executables=[Executable("test_pillow.py")],
    options={
        "build_exe": {
            "include_files": ["favicon.png"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
