"""A simple setup script to create executables using scipy.
This version requires the libs in the zip file.
"""

# test_scipy.py is a very simple scipy application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import os
import sysconfig

from cx_Freeze import setup

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

setup(
    name="scipy_samples",
    version="0.2",
    description="Sample scipy script",
    executables=["test_scipy.py"],
    options=options,
)
