"""
A setup script to create executables and demonstrate the use icons, that can be
valid or invalid icons. Also, it is used to demonstrate the use of manifests.
"""

from __future__ import annotations

from cx_Freeze import Executable, setup

executables = [
    Executable("test_icon.py", icon="icon.ico", target_name="test_icon"),
    Executable("test_icon.py", icon="ícone.ico", target_name="teste_ícone"),
    Executable("test_icon.py", icon="favicon.png", target_name="test_invalid"),
    Executable(
        "test_icon.py",
        icon="icon.ico",
        target_name="test_manifest_ação",
        uac_admin=True,  # read and write a manifest
    ),
]

setup(
    name="Icon sample",
    version="0.3",
    description="Test Icon",
    executables=executables,
)
