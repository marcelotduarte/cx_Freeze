"""Internal exception classes."""

# Only re-export setuptools errors to avoid exceptions not handled correctly
from setuptools.errors import (
    ExecError,
    FileError,
    ModuleError,
    OptionError,
    PlatformError,
    SetupError,
)

__all__ = [
    "ExecError",
    "FileError",
    "ModuleError",
    "OptionError",
    "PlatformError",
    "SetupError",
]


ExecError.__doc__ = """\
Raised when there are problems executing an external program."""

FileError.__doc__ = """\
Raised when an error is detected related to file/resource not found."""

ModuleError.__doc__ = """\
Raised when there are problems to load the module or module metadata."""

OptionError.__doc__ = """\
Raised when an error is detected in the configuration. The associated value is
a string indicating what precisely went wrong."""

PlatformError.__doc__ = """\
Raised when an error is detected in the module that is platform specific."""

SetupError.__doc__ = """\
Raised for errors that can be definitely blamed on the setup script, such as
invalid keyword arguments to 'setup()'."""
