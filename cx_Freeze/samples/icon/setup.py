"""
A setup script to create two executables and demonstrate the use a valid and
an invalid icon.
"""

from cx_Freeze import setup, Executable

executables = [
    Executable("test_icon.py", icon="icon.ico", target_name="test_1.exe"),
    Executable("test_icon.py", icon="favicon.png", target_name="test_2.exe"),
]

setup(
    name="Icon sample",
    version="0.1",
    description="Test Icon",
    executables=executables,
)
