"""A very simple setup script to test adding summary data stream to an MSI
file.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs

Run the build process by running the command 'python setup.py bdist_msi'
"""

from cx_Freeze import setup

bdist_msi_options = {
    "license_file": "LICENSE.rtf",
}

setup(
    name="hello",
    version="0.1",
    description="Sample cx_Freeze script to test MSI summary data stream",
    executables=["hello.py"],
    options={
        "build_exe": {"excludes": ["tkinter"]},
        "bdist_msi": bdist_msi_options,
    },
)
