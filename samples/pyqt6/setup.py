"""A simple setup script to create an executable using PyQt6. This also
demonstrates how to use excludes to get minimal package size.

test_pyqt6.py is a very simple type of PyQt6 application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

from __future__ import annotations

from cx_Freeze import setup

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

include_files = [("logo.svg", "share/logo.svg")]

if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze automatically imports the following plugins depending on the
    # module used, but suppose we need the following:
    include_files += get_qt_plugins_paths("PyQt6", "multimedia")

build_exe_options = {
    "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
    # exclude packages that are not really needed
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
    "include_files": include_files,
}

setup(
    name="simple_pyqt6",
    version="7.2",
    description="Sample cx_Freeze PyQt6 script",
    executables=[{"script": "test_pyqt6.py", "base": "gui"}],
    options={"build_exe": build_exe_options},
)
