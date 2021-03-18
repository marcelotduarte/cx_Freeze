import setuptools
import sys

from .dist import bdist_rpm, build, build_exe, install, install_exe, setup
from .exception import ConfigError
from .finder import Module, ModuleFinder
from .freezer import ConstantsModule, Executable, Freezer
import importlib_metadata

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
]

if sys.platform == "win32":
    from .windist import bdist_msi

    __all__.append("bdist_msi")
elif sys.platform == "darwin":
    from .macdist import bdist_dmg, bdist_mac

    __all__.extend(["bdist_dmg", "bdist_mac"])

__version__ = importlib_metadata.version("cx_Freeze")
version = __version__
__all__.extend(["__version__", "version"])
