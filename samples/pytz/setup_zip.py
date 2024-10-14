"""A setup script to demonstrate build using pytz
This version requires the zoneinfo in the zip file.
"""

from __future__ import annotations

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
import os
import sysconfig

from cx_Freeze import setup

platform = sysconfig.get_platform()
python_version = sysconfig.get_python_version()
dir_name = f"zip.{platform}-{python_version}"
build_exe_dir = os.path.join("build", dir_name)

setup(
    name="test_pytz_zip",
    version="0.3",
    description="cx_Freeze script to test pytz",
    executables=["test_pytz.py"],
    options={
        "build_exe": {
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
            "build_exe": build_exe_dir,
        }
    },
)
