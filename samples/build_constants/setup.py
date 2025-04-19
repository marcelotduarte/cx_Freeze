"""A very simple setup script to create a single executable, and test the
BUILD_CONSTANTS functionality.

hello.py is a very simple 'Hello, world' type script which also displays
certains constants stored in BUILD_CONSTANTS.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python
"""

from cx_Freeze import setup

setup(
    name="hello",
    version="0.1",
    description="Sample cx_Freeze script",
    executables=[
        {"script": "hello.py", "copyright": "Copyright (C) 2025 cx_Freeze"}
    ],
    options={
        "build_exe": {
            "constants": [
                "USER_UNDEFINED",
                "USERDEFINED_A=7",
                'USERDEFINED_B="hello=7"',
                "USERDEFINED_C=",
            ],
            "excludes": ["tkinter", "unittest"],
            "silent": True,
        },
    },
)
