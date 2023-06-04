"""A setup script to demonstrate build using ssl."""
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from __future__ import annotations

from pathlib import Path

from cx_Freeze import Executable, build_exe, setup


class DyLibFixerCommand(build_exe):
    def run(self):
        super().run()

        print("self.build_exe", self.build_exe)
        for dylib_file in Path(self.build_exe).glob("*.dylib"):
            dylib_file.rename(dylib_file.parent / "lib" / dylib_file.name)
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
