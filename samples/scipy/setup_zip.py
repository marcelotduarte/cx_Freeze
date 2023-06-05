"""A simple setup script to create executables using scipy.
   This version requires the libs in the zip file."""

from __future__ import annotations

# scipy_eg.py is a very simple scipy application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
import os
import sys
import sysconfig

from cx_Freeze import Executable, setup

base = "Win32GUI" if sys.platform == "win32" else None

platform = sysconfig.get_platform()
python_version = sysconfig.get_python_version()
dir_name = f"zip.{platform}-{python_version}"
build_exe_dir = os.path.join("build", dir_name)

options = {
    "build_exe": {
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "build_exe": build_exe_dir,
    }
}

executables = [
    Executable("scipy_eg.py", base=base),
]

setup(
    name="scipy_samples",
    version="0.2",
    description="Sample scipy script",
    executables=executables,
    options=options,
)
