"""Create standalone executables from Python scripts, with the same performance
and is cross-platform."""
# pylint: disable=C0103

import sys

from .dist import build, build_exe, install, install_exe, setup
from .exception import ConfigError
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer

__all__ = [
    "build",
    "build_exe",
    "install",
    "install_exe",
    "setup",
    "ConfigError",
    "ConstantsModule",
    "Executable",
    "Freezer",
    "Module",
    "ModuleFinder",
    "__version__",
]

if sys.platform == "win32":
    from .command.bdist_msi import BdistMSI

    __all__.append(BdistMSI.__name__)
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG, BdistMac

    __all__.extend([BdistDMG.__name__, BdistMac.__name__])
else:
    from .command.bdist_rpm import BdistRPM

    __all__.append(BdistRPM.__name__)

__version__ = "6.11.0-dev0"
