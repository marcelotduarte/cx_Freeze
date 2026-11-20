"""The internal _typing module."""

from __future__ import annotations

from collections.abc import Sequence
from os import PathLike
from pathlib import Path, PurePath
from typing import TypeAlias

from cx_Freeze.module import Module

StrPath: TypeAlias = str | PathLike[str]

DeferredList: TypeAlias = list[tuple[Module, Module, list[str]]]

Executables: TypeAlias = list[str | dict[str, str]]

IncludesList: TypeAlias = Sequence[StrPath | tuple[StrPath, StrPath | None]]

InternalIncludesList: TypeAlias = list[tuple[Path, PurePath]]

HANDLE: TypeAlias = int | None


__all__ = [
    "HANDLE",
    "DeferredList",
    "Executables",
    "IncludesList",
    "InternalIncludesList",
    "StrPath",
]
