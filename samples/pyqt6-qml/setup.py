"""A simple setup script to create an executable using PyQt6. This also
demonstrates how to use excludes to get minimal package size.

test_qml.py is a very simple type of PyQt6 application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

from cx_Freeze import setup

build_exe_options = {
    "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
    # exclude packages that are not really needed
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
}

setup(
    name="qml_test",
    version="7.2.2",
    description="Sample cx_Freeze PyQt6 script",
    executables=[{"script": "test_qml.py", "base": "gui"}],
    options={"build_exe": build_exe_options},
)
