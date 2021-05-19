"""
A setup script to create executables and demonstrate the use icons, that can be
valid or invalid icons.
"""

from cx_Freeze import setup, Executable

executables = [
    Executable("test_icon.py", icon="icon.ico", target_name="test_icon"),
    Executable("test_icon.py", icon="ícone.ico", target_name="teste_ícone"),
    Executable("test_icon.py", icon="favicon.png", target_name="test_invalid"),
]

setup(
    name="Icon sample",
    version="0.3",
    description="Test Icon",
    executables=executables,
)
