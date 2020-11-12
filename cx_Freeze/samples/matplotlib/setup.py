"""A simple setup script to create two executables using matplotlib."""

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

import sys
from cx_Freeze import setup, Executable

base = "Console"
if sys.platform == "win32":
    base = "Win32GUI"

options = {
    "build_exe": {
        # Sometimes a little fine-tuning is needed
        # exclude all backends except wx
        "excludes": ["gtk", "PyQt4", "PyQt5", "tkinter"]
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
