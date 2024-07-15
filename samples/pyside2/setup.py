"""A simple setup script to create an executable using PySide2. This also
demonstrates how to use excludes to get minimal package size.

test_pyside2.py is a very simple type of PySide2 application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

from __future__ import annotations

import os

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
    include_files += get_qt_plugins_paths("PySide2", "multimedia")

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
        "include_files": include_files,
    },
    "bdist_mac": {
        "custom_info_plist": None,  # Set this to use a custom info.plist file
        "codesign_entitlements": os.path.join(
            os.path.dirname(__file__), "codesign-entitlements.plist"
        ),
        "codesign_identity": None,  # Set this to enable signing with custom identity (replaces adhoc signature)
        "codesign_options": "runtime",  # Ensure codesign uses 'hardened runtime'
        "codesign_verify": False,  # Enable to get more verbose logging regarding codesign
        "spctl_assess": False,  # Enable to get more verbose logging regarding codesign
    },
}
executables = [Executable("test_pyside2.py", base="gui")]

setup(
    name="simple_PySide2",
    version="7.2",
    description="Sample cx_Freeze PySide2 script",
    options=options,
    executables=executables,
)
