"""A setup script to create an executable to demonstrate the use of manifest."""

from cx_Freeze import Executable, setup

executables = [
    # use default manifest
    Executable("test_manifest.py", icon="icon"),
    # write a new manifest
    Executable(
        "test_manifest.py",
        icon="icon",
        manifest="simple.manifest",
        target_name="test_simple_manifest",
    ),
    # read and write a modified manifest using uac_admin
    Executable(
        "test_manifest.py",
        icon="icon",
        uac_admin=True,
        target_name="test_uac_admin",
    ),
]

setup(
    name="Manifest sample",
    version="0.3",
    description="Test the use of manifest and uac_admin",
    executables=executables,
)
