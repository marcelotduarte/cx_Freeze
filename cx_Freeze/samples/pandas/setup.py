"""A simple setup script to test pandas."""

# test_pandas.py is a very simple script.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

from cx_Freeze import setup, Executable

options = {"build_exe": {"excludes": ["tkinter"]}}

executables = [
    Executable("test_pandas.py"),
]

setup(
    name="test_pandas",
    version="0.1",
    description="Sample pandas script",
    executables=executables,
    options=options,
)
