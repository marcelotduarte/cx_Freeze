# A very simple setup script to test adding summary data stream to an MSI file.
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py bdist_msi'


from __future__ import annotations

from cx_Freeze import Executable, setup

executables = [Executable("hello.py")]

bdist_msi_options = {
    "summary_data": {
        "author": "Name of the author",
        "comments": "This is a comment",
        "keywords": "These Are Some Keywords",
    },
}

setup(
    name="hello",
    version="0.1",
    description="Sample cx_Freeze script to test MSI summary data stream",
    executables=executables,
    options={
        "build_exe": {"excludes": ["tkinter"]},
        "bdist_msi": bdist_msi_options,
    },
)
