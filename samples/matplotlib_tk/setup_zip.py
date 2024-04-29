"""A simple setup script to create executable using matplotlib
This version requires the mpl-data in the zip file.
"""

# test_matplotlib_tk.py is a very simple matplotlib application that
# demonstrates its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
import os
import sysconfig

from cx_Freeze import Executable, setup

platform = sysconfig.get_platform()
python_version = sysconfig.get_python_version()
dir_name = f"zip.{platform}-{python_version}"
build_exe_dir = os.path.join("build", dir_name)

options = {
    "build_exe": {
        # Sometimes a little fine-tuning is needed
        # exclude all backends except tkinter
        "excludes": [
            "gi",
            "gtk",
            "PyQt4",
            "PyQt5",
            "PyQt6",
            "PySide2",
            "PySide6",
            "shiboken2",
            "shiboken6",
            "wx",
        ],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
        "build_exe": build_exe_dir,
    }
}

executables = [
    Executable("test_matplotlib_tk.py", base="gui"),
]

setup(
    name="matplotlib_samples",
    version="0.1",
    description="Sample matplotlib script",
    executables=executables,
    options=options,
)
