"""Internal compatible module."""

from __future__ import annotations

import sys
import sysconfig
from pathlib import Path

__all__ = [
    "ABI_THREAD",
    "BUILD_EXE_DIR",
    "EXE_SUFFIX",
    "EXT_SUFFIX",
    "IS_CONDA",
    "IS_LINUX",
    "IS_MACOS",
    "IS_MINGW",
    "IS_WINDOWS",
    "PLATFORM",
    "PYTHON_VERSION",
]

PLATFORM = sysconfig.get_platform()
PYTHON_VERSION = sysconfig.get_python_version()
ABI_THREAD = sysconfig.get_config_var("abi_thread") or ""

BUILD_EXE_DIR = Path(f"build/exe.{PLATFORM}-{PYTHON_VERSION}{ABI_THREAD}")
EXE_SUFFIX = sysconfig.get_config_var("EXE")
EXT_SUFFIX = sysconfig.get_config_var("EXT_SUFFIX")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()

IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_MINGW64 = PLATFORM.startswith("mingw_x86_64")
IS_WINDOWS = PLATFORM.startswith("win")
