"""A simple setup script to create an executable using PySide6. This also
demonstrates how to use excludes to get minimal package size.

test_pyside6.py is a very simple type of PySide6 application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
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
    include_files += get_qt_plugins_paths("PySide6", "multimedia")

build_exe_options = {
    "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
    # exclude packages that are not really needed
    "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
    "include_files": include_files,
    "zip_include_packages": ["PySide6", "shiboken6"],
}

executables = [Executable("test_pyside6.py", base="gui")]

setup(
    name="simple_PySide6",
    version="0.3",
    description="Sample cx_Freeze PySide6 script",
    options={"build_exe": build_exe_options},
    executables=executables,
)
