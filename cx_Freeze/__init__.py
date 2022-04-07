"""Create standalone executables from Python scripts, with the same performance
and is cross-platform."""
# pylint: disable=C0103

import sys

from .command.build import Build as build
from .command.install import Install as install
from .dist import build_exe, install_exe, setup
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
    from .command.bdist_msi import BdistMSI as bdist_msi

    __all__.append(bdist_msi.__name__)
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG as bdist_dmg
    from .command.bdist_mac import BdistMac as bdist_mac

    __all__.extend([bdist_dmg.__name__, bdist_mac.__name__])
else:
    from .command.bdist_rpm import BdistRPM as bdist_rpm

    __all__.append(bdist_rpm.__name__)

__version__ = "6.11.0-dev0"
