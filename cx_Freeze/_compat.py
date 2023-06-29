"""Internal compatible module."""

from __future__ import annotations

import sys
import sysconfig
from pathlib import Path

if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    try:
        from setuptools.extern import importlib_metadata
    except ImportError:
        import importlib_metadata

try:
    # pylint: disable-next=ungrouped-imports
    from setuptools.extern import packaging
except ImportError:
    import packaging

__all__ = ["importlib_metadata", "packaging"]
__all__ += ["PLATFORM", "IS_LINUX", "IS_MACOS", "IS_MINGW", "IS_WINDOWS"]
__all__ += ["IS_CONDA"]

PLATFORM = sysconfig.get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()
