"""A setup script to create a single executable."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
import sys

from cx_Freeze import Executable, setup

script = (
    "test_pydantic.py"
    if sys.version_info < (3, 10)
    else "test_pydantic_py310.py"
)
executables = [Executable(script, target_name="test_pydantic")]

setup(
    name="test_pydantic",
    version="0.1",
    description="Test pydantic",
    executables=executables,
)
