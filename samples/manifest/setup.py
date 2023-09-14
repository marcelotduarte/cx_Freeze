"""
A setup script to create an executable to demonstrate the use of manifest.
"""
import sys
from cx_Freeze import Executable, setup

if sys.platform == "win32":
    icon_ok = "icon.ico"
else:
    icon_ok = "icon.png"

# uac_admin read and write a manifest
executables = [Executable("test_manifest.py", icon=icon_ok, uac_admin=True)]

setup(
    name="Manifest sample",
    version="0.1",
    description="Test use of manifest changing the uac_admin",
    executables=executables,
)
