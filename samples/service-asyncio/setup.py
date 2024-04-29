"""A simple setup script for creating a Windows service.
See the comments in the Config.py and ServiceHandler.py files for more
information on how to set this up.

Installing the service is done with the option --install <Name> and
uninstalling the service is done with the option --uninstall <Name>. The
value for <Name> is intended to differentiate between different invocations
of the same service code -- for example for accessing different databases or
using different configuration files.
"""

from __future__ import annotations

from cx_Freeze import Executable, setup

options = {
    "build_exe": {
        "includes": ["ServiceHandler", "cx_Logging"],
        "excludes": ["tkinter"],
    }
}

executables = [
    Executable(
        "Config.py",
        base="Win32Service",
        target_name="cx_FreezeSampleServiceAsyncio.exe",
    )
]

setup(
    name="cx_FreezeSampleServiceAsyncio",
    version="0.1",
    description="Sample cx_Freeze Windows service with asyncio",
    executables=executables,
    options=options,
)
