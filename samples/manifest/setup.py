"""
A setup script to create an executable to demonstrate the use of manifest.
"""
import sys
from cx_Freeze import Executable, setup

if sys.platform == "win32":
    icon_ok = "icon.ico"
else:
    icon_ok = "icon.png"

executables = [
    # use default manifest
    Executable("test_manifest.py", icon=icon_ok),
    # write a new manifest
    Executable(
        "test_manifest.py",
        icon=icon_ok,
        manifest="simple.manifest",
        target_name="test_simple_manifest",
    ),
    # read and write a modified manifest using uac_admin
    Executable(
        "test_manifest.py",
        icon=icon_ok,
        uac_admin=True,
        target_name="test_uac_admin",
    ),
]

setup(
    name="Manifest sample",
    version="0.2",
    description="Test the use of manifest and uac_admin",
    executables=executables,
)
