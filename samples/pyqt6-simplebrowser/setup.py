"""A simple setup script to create an executable using PyQt6-WebEngine.
This also demonstrates how to use excludes to get minimal package size.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

from __future__ import annotations

from cx_Freeze import Executable, setup

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

include_files = []
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

executables = [
    Executable(
        "simplebrowser.py", target_name="test_simplebrowser", base="gui"
    )
]

setup(
    name="simplebrowser",
    version="7.2",
    description="Sample cx_Freeze PyQt6 simplebrowser script",
    options={"build_exe": build_exe_options},
    executables=executables,
)
