"""Internal compatible module."""

from __future__ import annotations

import platform
import sys
from pathlib import Path
from sysconfig import get_config_var, get_platform, get_python_version

__all__ = [
    "ABI_THREAD",
    "BUILD_EXE_DIR",
    "EXE_SUFFIX",
    "EXT_SUFFIX",
    "IS_ARM_64",
    "IS_CONDA",
    "IS_LINUX",
    "IS_MACOS",
    "IS_MINGW",
    "IS_WINDOWS",
    "IS_X86_32",
    "IS_X86_64",
    "PLATFORM",
    "PYTHON_VERSION",
    "SOABI",
]

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
ABI_THREAD = get_config_var("abi_thread") or ""

BUILD_EXE_DIR = Path(f"build/exe.{PLATFORM}-{PYTHON_VERSION}{ABI_THREAD}")
EXE_SUFFIX = get_config_var("EXE")
EXT_SUFFIX = get_config_var("EXT_SUFFIX")

IS_ARM_64 = platform.machine() in ("aarch64", "arm64", "ARM64")
IS_X86_32 = platform.machine() in ("x86", "i686")
IS_X86_64 = platform.machine() in ("x64", "x86_64", "AMD64")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()

IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")

SOABI = get_config_var("SOABI")
if SOABI is None or IS_MINGW:
    # Python <= 3.12 on Windows
    # Python 3.12 MSYS2 incorrectly returns only sys.implementation.cache_tag
    platform_nodot = PLATFORM.replace(".", "").replace("-", "_")
    SOABI = f"{sys.implementation.cache_tag}-{platform_nodot}"
