"""A setup script to demonstrate build using bcrypt.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python
"""

from __future__ import annotations

from cx_Freeze import Executable, setup

executables = [Executable("test/__init__.py", target_name="test_bcrypt")]
options = {
    "build_exe": {
        "excludes": ["tkinter"],
        "silent": True,
        "zip_include_packages": ["*"],
        "zip_exclude_packages": [],
    },
    "bdist_rpm": {
        "quiet": True,
    },
}

setup(
    name="test_bcrypt",
    version="0.3",
    description="cx_Freeze script to test bcrypt",
    executables=executables,
    options=options,
    author="Marcelo Duarte",
    author_email="marcelotduarte@users.noreply.github.com",
    url="https://github.com/marcelotduarte/cx_Freeze/",
)
