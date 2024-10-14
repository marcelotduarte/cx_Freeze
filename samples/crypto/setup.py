"""A setup script to demonstrate build using pycryptodome."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup

setup(
    name="test_cryptodome",
    version="0.1",
    description="cx_Freeze script to test pycryptodome",
    executables=["test_crypto.py"],
    options={
        "build_exe": {
            "excludes": ["tkinter"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
