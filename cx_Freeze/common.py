"""Common utility functions shared between cx_Freeze modules."""

from __future__ import annotations

import importlib.resources as importlib_resources
from pathlib import Path, PurePath
from typing import TYPE_CHECKING

from cx_Freeze.exception import OptionError

if TYPE_CHECKING:
    from cx_Freeze._typing import IncludesList, InternalIncludesList


def resource_path(name: str | Path) -> Path | None:
    """Return the path to a resource file shipped with freeze-core.

    This is used to find our base executables and initscripts when they are
    just specified by name.
    """
    resource = importlib_resources.files("freeze_core") / name
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
    if specs is None:
        specs = []
    processed_specs: InternalIncludesList = []
    for spec in specs:
        if not isinstance(spec, (list, tuple)):
            source = spec
            target = None
        elif len(spec) != 2:
            msg = "path spec must be a list or tuple of length two"
            raise OptionError(msg)
        else:
            source, target = spec
        source = Path(source)
        if not source.exists():
            msg = f"cannot find file/directory named {source!s}"
            raise OptionError(msg)
        target = PurePath(target or source.name)
        if target.is_absolute():
            msg = f"target path named {target!s} cannot be absolute"
            raise OptionError(msg)
        processed_specs.append((source, target))
    return processed_specs
