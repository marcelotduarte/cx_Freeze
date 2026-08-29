"""Internal compatible module."""

from __future__ import annotations

import os
import platform
import struct
import sys
from pathlib import Path
from sysconfig import get_config_var, get_platform, get_python_version
from typing import Final, Literal, cast

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
    "IS_MINGW_CLANG",
    "IS_MINGW_UCRT",
    "IS_UCRT",
    "IS_WINDOWS",
    "IS_X86_32",
    "IS_X86_64",
    "PLATFORM",
    "PYTHON_VERSION",
    "SOABI",
]

PLATFORM: Final[str] = get_platform()
PYTHON_VERSION: Final[str] = get_python_version()
ABI_THREAD: Final[Literal["t", ""]] = cast(
    'Literal["t", ""]', get_config_var("abi_thread") or ""
)

BUILD_EXE_DIR = Path(f"build/exe.{PLATFORM}-{PYTHON_VERSION}{ABI_THREAD}")
EXE_SUFFIX: str = cast("str", get_config_var("EXE"))
EXT_SUFFIX: str = cast("str", get_config_var("EXT_SUFFIX"))

IS_ARM_64: Final[bool] = platform.machine() in ("aarch64", "arm64", "ARM64")
IS_X86_32: Final[bool] = (
    platform.machine() in ("x86", "i686", "x64", "x86_64", "AMD64")
    and struct.calcsize("P") == 4
)
IS_X86_64: Final[bool] = (
    platform.machine() in ("x64", "x86_64", "AMD64")
    and struct.calcsize("P") == 8
)

IS_CONDA: Final[bool] = Path(sys.prefix, "conda-meta").is_dir()

IS_LINUX: Final[bool] = PLATFORM.startswith("linux")
IS_MACOS: Final[bool] = PLATFORM.startswith("macos")
IS_MINGW: Final[bool] = PLATFORM.startswith("mingw")
IS_WINDOWS: Final[bool] = PLATFORM.startswith("win")

_MSYSTEM = os.environ.get("MSYSTEM", "")
IS_MINGW_CLANG: Final[bool] = IS_MINGW and _MSYSTEM.startswith("CLANG")
IS_MINGW_UCRT: Final[bool] = IS_MINGW and _MSYSTEM.startswith("UCRT")
IS_UCRT: Final[bool] = IS_WINDOWS or IS_MINGW_CLANG or IS_MINGW_UCRT

_SOABI = get_config_var("SOABI")
if _SOABI is None:
    # Python <= 3.12 on Windows
    platform_nodot = PLATFORM.replace(".", "").replace("-", "_")
    _SOABI = f"{sys.implementation.cache_tag}-{platform_nodot}"
SOABI: Final[str] = cast("str", _SOABI)
