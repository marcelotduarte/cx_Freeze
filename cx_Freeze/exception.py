"""Internal exception classes."""

from setuptools.errors import ExecError as _ExecError
from setuptools.errors import FileError as _FileError
from setuptools.errors import OptionError as _OptionError
from setuptools.errors import PlatformError as _PlatformError
from setuptools.errors import SetupError as _SetupError

__all__ = [
    "ExecError",
    "FileError",
    "OptionError",
    "PlatformError",
    "SetupError",
]


class ExecError(_ExecError):
    """Raised when there are problems executing an external program."""


class FileError(_FileError):
    """Raised when an error is detected related to file/resource not found."""


class OptionError(_OptionError):
    """Raised when an error is detected in the configuration.
    The associated value is a string indicating what precisely went wrong.
    """


class PlatformError(_PlatformError):
    """Raised when an error is detected in the module that is platform
    specific.
    """


class SetupError(_SetupError):
    """Raised for errors that can be definitely blamed on the setup script,
    such as invalid keyword arguments to 'setup()'.
    """
