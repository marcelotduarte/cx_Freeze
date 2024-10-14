"""An advanced setup script to create multiple executables and demonstrate a
few of the features available to setup scripts.
"""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
import sys

from cx_Freeze import setup

options = {
    "build_exe": {
        "includes": ["testfreeze_1", "testfreeze_2"],
        "path": [*sys.path, "modules"],
    }
}

executables = ["advanced_1.py", "advanced_2.py"]

setup(
    name="advanced_cx_Freeze_sample",
    version="0.1",
    description="Advanced sample cx_Freeze script",
    options=options,
    executables=executables,
)
