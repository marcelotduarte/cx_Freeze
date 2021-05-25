"""
A setup script to create a single executable.
"""

# https://github.com/samuelcolvin/pydantic#a-simple-example
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [Executable("test_pydantic.py")]

setup(
    name="test_pydantic",
    version="0.1",
    description="Test pydantic",
    executables=executables,
)
