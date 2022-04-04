"""Create standalone executables from Python scripts, with the same performance
and is cross-platform."""
# pylint: disable=C0103

import sys

from .dist import bdist_rpm, build, build_exe, install, install_exe, setup
from .exception import ConfigError
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer

__all__ = [
    "bdist_rpm",
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
    from .windist import bdist_msi

    __all__.append(bdist_msi.__name__)
elif sys.platform == "darwin":
    from .macdist import bdist_dmg, bdist_mac

    __all__.extend([bdist_dmg.__name__, bdist_mac.__name__])

__version__ = "6.11.0-dev0"
