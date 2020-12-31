"""A simple setup script to create two executables using matplotlib
   This version requires the mpl-data in the zip file."""

# matplotlib_eg.py is a very simple matplotlib application that demonstrates
# its use.
#
# matplotlib_afm.py is a very simple matplotlib console application that show
# some values of a font.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import distutils
import os
import sys
from cx_Freeze import setup, Executable

base = "Console"
if sys.platform == "win32":
    base = "Win32GUI"

dir_name = "zip.{}-{}".format(distutils.util.get_platform(), sys.version[0:3])
build_exe_dir = os.path.join("build", dir_name)

options = {
    "build_exe": {
        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        "excludes": ["gtk", "PyQt4", "PyQt5", "tkinter"],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "build_exe": build_exe_dir,
    }
}

executables = [
    Executable("matplotlib_afm.py"),
    Executable("matplotlib_eg.py", base=base),
]

setup(
    name="matplotlib_samples",
    version="0.1",
    description="Sample matplotlib script",
    executables=executables,
    options=options,
)
