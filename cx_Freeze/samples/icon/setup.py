"""
A setup script to create two executables and demonstrate the use a valid and
an invalid icon.
"""

from cx_Freeze import setup, Executable

executables = [
    Executable("test_icon.py", icon="icon.ico", target_name="test_icon"),
    Executable(
        "test_icon.py", icon="favicon.png", target_name="test_icon-invalid"
    ),
]

setup(
    name="Icon sample",
    version="0.2",
    description="Test Icon",
    executables=executables,
)
