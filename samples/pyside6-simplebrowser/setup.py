"""A simple setup script to create an executable using PySide6 WebEngineWidgets.
This also demonstrates how to use excludes to get minimal package size.

simplebrowser.py is the "PySide6 WebEngineWidgets Example".

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

import os

from cx_Freeze import Executable, setup

options = {
    "build_exe": {
        "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
        # exclude packages that are not really needed
        "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
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

executables = [
    Executable(
        "simplebrowser.py", target_name="test_simplebrowser", base="gui"
    )
]

setup(
    name="simplebrowser",
    version="7.2",
    description="Sample cx_Freeze PySide6 simplebrowser script",
    options=options,
    executables=executables,
)
