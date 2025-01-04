"""A very simple setup script to test adding additional and binary data stream
to an MSI file.

This script defines a ProgId for the installed program with an associated icon
icon.ico is the file whose binary data will be loaded in the Icon table.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs

Run the build process by running the command 'python setup.py bdist_msi'
"""

from cx_Freeze import Executable, setup

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("Prog.Id", None, None, "This is a description", "IconId", None),
    ],
    "Icon": [
        ("IconId", "icon.ico"),
    ],
}

bdist_msi_options = {
    "add_to_path": True,
    "data": msi_data,
    "environment_variables": [
        ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
    ],
    # use a different upgrade_code for your project
    "upgrade_code": "{6B29FC40-CA47-1067-B31D-00DD010662DA}",
}

build_exe_options = {"excludes": ["tkinter"], "include_msvcr": True}

executables = [
    Executable(
        "hello.py",
        copyright="Copyright (C) 2025 cx_Freeze",
        base="gui",
        icon="icon.ico",
        shortcut_name="My Program Name",
        shortcut_dir="MyProgramMenu",
    )
]

setup(
    name="hello",
    version="0.1.2.3",
    description="Sample cx_Freeze script to test MSI arbitrary data stream",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
)
