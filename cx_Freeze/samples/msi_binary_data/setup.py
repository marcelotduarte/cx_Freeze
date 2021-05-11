# A very simple setup script to test adding additional and binary data stream to
# an MSI file.
#
# This script defines a ProgId for the installed program with an associated icon
# icon.ico is the file whose binary data will be loaded in the Icon table.
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py bdist_msi'


from cx_Freeze import setup, Executable

executables = [Executable("hello.py")]

bdist_msi_options = {
    "data": {
        "ProgId": [
            ("Prog.Id", None, None, "This is a description", "IconId", None),
        ],
        "Icon": [
            ("IconId", "icon.ico"),
        ],
    },
}

setup(
    name="hello",
    version="0.1",
    description="Sample cx_Freeze script to test MSI arbitrary data stream",
    executables=executables,
    options={
        "build_exe": {"excludes": ["tkinter"]},
        "bdist_msi": bdist_msi_options,
    },
)
