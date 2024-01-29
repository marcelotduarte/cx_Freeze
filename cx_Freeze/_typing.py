"""The internal _typing module."""

from __future__ import annotations

from pathlib import Path, PurePath
from typing import List, Optional, Tuple, Union

from cx_Freeze.module import Module

DeferredList = List[Tuple[Module, Module, List[str]]]

IncludesList = List[
    Union[str, Path, Tuple[Union[str, Path], Optional[Union[str, Path]]]]
]

InternalIncludesList = List[Tuple[Path, PurePath]]
