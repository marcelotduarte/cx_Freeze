"""A very simple setup script to test adding extension handling to an MSI file.

This script defines three ways for the hello.py executable to handle text
files, that are registered in the operating system.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs

Run the build process by running the command 'python setup.py bdist_msi'
"""

from cx_Freeze import setup

bdist_msi_options = {
    "extensions": [
        # open / print / view text files
        {
            "extension": "txt",
            "verb": "open",
            "executable": "hello.exe",
            "context": "Edit with hello.py",
        },
        {
            "extension": "txt",
            "verb": "print",
            "executable": "hello.exe",
            "context": "Print with hello.py",
            "argument": '--print "%1"',
        },
        {
            "extension": "txt",
            "verb": "view",
            "executable": "hello.exe",
            "context": "View with hello.py",
            "argument": '--read-only "%1"',
        },
        # open / print / view log files
        {
            "extension": "log",
            "verb": "open",
            "executable": "hello.exe",
            "context": "Edit with hello.py",
        },
        {
            "extension": "log",
            "verb": "print",
            "executable": "hello.exe",
            "context": "Print with hello.py",
            "argument": '--print "%1"',
        },
        {
            "extension": "log",
            "verb": "view",
            "executable": "hello.exe",
            "context": "View with hello.py",
            "argument": '--read-only "%1"',
        },
    ],
}

setup(
    name="Hello Program",
    version="0.1",
    author="cx_Freeze",
    description="Sample cx_Freeze script to test MSI extension registration",
    executables=["hello.py"],
    options={
        "build_exe": {"excludes": ["tkinter"]},
        "bdist_msi": bdist_msi_options,
    },
)
