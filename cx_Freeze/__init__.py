"""
Create standalone executables from Python scripts, with the same performance
and is cross-platform.
"""
import sys

from .dist import build, build_exe, bdist_rpm, install, install_exe, setup
from .exception import ConfigError
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer
from .version import __version__

__all__ = [
    "build",
    "build_exe",
    "bdist_rpm",
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
