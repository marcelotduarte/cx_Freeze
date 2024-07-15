"""A simple setup script to create an executable using opencv-python. This also
demonstrates how to use excludes to get minimal package size.

test_opencv.py is a very simple type of opencv-python application.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application.
"""

from cx_Freeze import Executable, setup

options = {
    "build_exe": {
        # exclude packages that are not really needed
        "excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],
        "include_files": [("image.png", "share/image.png")],
    }
}

executables = [Executable("test_opencv.py", base="gui")]

setup(
    name="simple_opencv",
    version="0.1",
    description="Sample cx_Freeze opencv-python script",
    options=options,
    executables=executables,
)
