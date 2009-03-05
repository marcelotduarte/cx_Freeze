# A simple setup script for creating a Windows service. See the comments in the
# Config.py and ServiceHandler.py files for more information on how to set this
# up.

from cx_Freeze import setup, Executable

buildOptions = dict(includes = ["ServiceHandler"])
executable = Executable("Config.py", base = "Win32Service",
        targetName = "cx_FreezeSampleService.exe")

setup(
        name = "cx_FreezeSampleService",
        version = "0.1",
        description = "Sample cx_Freeze Windows serice",
        executables = [executable],
        options = dict(build_exe = buildOptions))

