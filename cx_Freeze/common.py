"""Common utility functions shared between cx_Freeze modules."""

from __future__ import annotations

from collections.abc import Sequence
from importlib import resources
from pathlib import Path, PurePath
from typing import TYPE_CHECKING

from cx_Freeze.exception import OptionError

if TYPE_CHECKING:
    from cx_Freeze._typing import IncludesList, InternalIncludesList, StrPath


def resource_path(name: StrPath) -> Path | None:
    """Return the path to a resource file shipped with freeze-core.

    This is used to find our base executables and initscripts when they are
    just specified by name.
    """
    resource = Path(str(resources.files("freeze_core"))) / name
    if resource.exists():
        return resource
    return None


def normalize_to_list(
    value: str | list[str] | tuple[str, ...] | None,
) -> list[str]:
    """Takes the different formats of options containing multiple values and
    returns the value as a list object.
    """
    if not value:  # empty or None
        return []
    if isinstance(value, str):
        return value.split(",")
    return list(value)


def process_path_specs(specs: IncludesList | None) -> InternalIncludesList:
    """Prepare paths specified as config.

    The input is a list of either strings, or 2-tuples (source, target).
    Where single strings are supplied, the basenames are used as targets.
    Where targets are given explicitly, they must not be absolute paths.

    Returns a list of 2-tuples, or throws OptionError if something is wrong
    in the input.
    """
    processed_specs: InternalIncludesList = []
    if specs is None:
        return processed_specs
    for spec in specs:
        if isinstance(spec, str) or not isinstance(spec, Sequence):
            source = Path(spec)
            target = PurePath(source.name)
        elif isinstance(spec, Sequence) and len(spec) == 2:
            source = Path(str(spec[0]))
            target = PurePath(str(spec[1]))
        else:
            msg = "path spec must be a list or tuple of length two"
            raise OptionError(msg)
        if not source.exists():
            msg = f"cannot find file/directory named {source!s}"
            raise OptionError(msg)
        if target.is_absolute():
            msg = f"target path named {target!s} cannot be absolute"
            raise OptionError(msg)
        processed_specs.append((source, target))
    return processed_specs
