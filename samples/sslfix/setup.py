"""A setup script to demonstrate build using ssl."""

#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

import shutil
from pathlib import Path

from cx_Freeze import Executable, build_exe, setup


class DyLibFixerCommand(build_exe):
    def run(self) -> None:
        super().run()

        print("self.build_exe", self.build_exe)
        build_exe = Path(self.build_exe)
        for src in build_exe.joinpath("lib").glob("libpython*.dylib"):
            dst = build_exe / src.name
            shutil.copy(src, dst)
            shutil.copystat(src, dst)
        print("self.build_exe", self.build_exe)


COMMAND_CLASS = {"build_exe": DyLibFixerCommand}
setup(
    cmdclass=COMMAND_CLASS,
    name="test_ssl",
    version="0.2",
    description="cx_Freeze script to test ssl",
    executables=[Executable("test_sslfix.py")],
    options={
        "build_exe": {
            "zip_include_packages": ["*"],
            "zip_exclude_packages": [],
        }
    },
)
