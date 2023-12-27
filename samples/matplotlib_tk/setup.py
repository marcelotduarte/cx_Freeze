"""A simple setup script to create executable using matplotlib."""

# test_matplotlib_tk.py is a very simple matplotlib application that
# demonstrates its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
from cx_Freeze import Executable, setup

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
        ]
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
