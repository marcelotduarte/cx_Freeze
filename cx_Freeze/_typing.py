"""The internal _typing module."""

from __future__ import annotations

from pathlib import Path, PurePath
from typing import TypeAlias

from cx_Freeze.module import Module

DeferredList: TypeAlias = list[tuple[Module, Module, list[str]]]

IncludesList: TypeAlias = list[
    str | Path | tuple[str | Path, str | Path | None]
]

InternalIncludesList: TypeAlias = list[tuple[Path, PurePath]]

HANDLE: TypeAlias = int | None

__all__ = ["HANDLE", "DeferredList", "IncludesList", "InternalIncludesList"]
