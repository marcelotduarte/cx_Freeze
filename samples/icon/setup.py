"""
A setup script to create executables and demonstrate the use icons, that can be
valid or invalid icons.
"""
import sys
from cx_Freeze import Executable, setup

if sys.platform == "win32":
    icon_ok = "icon.ico"
    invalid = "icon.png"
else:
    icon_ok = "icon.png"
    invalid = "icon.ico"

executables = [
    Executable("test_icon.py", icon=icon_ok),
    Executable("test_icon.py", icon=invalid, target_name="test_invalid"),
]

setup(
    name="Icon sample",
    version="0.4",
    description="Test Icon",
    executables=executables,
)
