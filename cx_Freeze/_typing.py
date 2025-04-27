"""The internal _typing module."""

from __future__ import annotations

from pathlib import Path, PurePath

from cx_Freeze.module import Module

try:
    from typing import TypeAlias  # 3.10+
except ImportError:
    from typing import Any as TypeAlias


DeferredList: TypeAlias = list[tuple[Module, Module, list[str]]]

IncludesList: TypeAlias = list[
    str | Path | tuple[str | Path, str | Path | None]
]

InternalIncludesList: TypeAlias = list[tuple[Path, PurePath]]

HANDLE: TypeAlias = int | None

__all__ = ["HANDLE", "DeferredList", "IncludesList", "InternalIncludesList"]
