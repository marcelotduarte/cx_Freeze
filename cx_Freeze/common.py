"""
This module contains utility functions shared between cx_Freeze modules.
"""

import os.path
import types
from typing import List, Tuple, Optional, Union
import warnings

from .exception import ConfigError


def get_resource_file_path(dirname: str, name: str, ext: str) -> str:
    """
    Return the path to a resource file shipped with cx_Freeze.

    This is used to find our base executables and initscripts when they are
    just specified by name.
    """
    if os.path.isabs(name):
        return name
    name = os.path.normcase(name)
    full_dir = os.path.join(os.path.dirname(__file__), dirname)
    if os.path.isdir(full_dir):
        for filename in os.listdir(full_dir):
            base_name, base_ext = os.path.splitext(os.path.normcase(filename))
            if name == base_name and ext == base_ext:
                return os.path.join(full_dir, filename)


def normalize_to_list(
    value: Optional[Union[str, List[str], Tuple[str, ...]]]
) -> List[str]:
    """
    Takes the different formats of options containing multiple values and
    returns the value as a list object.
    """
    if value is None:
        normalized_value = []
    elif isinstance(value, str):
        normalized_value = value.split(",")
    else:
        normalized_value = list(value)

    return normalized_value


def process_path_specs(
    specs: Optional[List[Union[str, Tuple[str, str]]]]
) -> List[Tuple[str, str]]:
    """
    Prepare paths specified as config.

    The input is a list of either strings, or 2-tuples (source, target).
    Where single strings are supplied, the basenames are used as targets.
    Where targets are given explicitly, they must not be absolute paths.

    Returns a list of 2-tuples, or throws ConfigError if something is wrong
    in the input.
    """
    if specs is None:
        specs = []
    processed_specs: List[Tuple[str, str]] = []
    for spec in specs:
        if not isinstance(spec, (list, tuple)):
            source = spec
            target = None
        elif len(spec) != 2:
            raise ConfigError(
                "path spec must be a list or tuple of length two"
            )
        else:
            source, target = spec
        source = os.path.normpath(source)
        if not target:
            target = os.path.basename(source)
        elif os.path.isabs(target):
            raise ConfigError(
                "target path for include file may not be an absolute path"
            )
        processed_specs.append((source, target))
    return processed_specs


def code_object_replace(code: types.CodeType, **kwargs) -> types.CodeType:
    """
    Return a copy of the code object with new values for the specified fields.
    """
    try:
        kwargs["co_consts"] = tuple(kwargs["co_consts"])
    except ValueError:
        pass
    # Python 3.8+
    if hasattr(code, "replace"):
        return code.replace(**kwargs)
    params = [
        kwargs.get("co_argcount", code.co_argcount),
        kwargs.get("co_kwonlyargcount", code.co_kwonlyargcount),
        kwargs.get("co_nlocals", code.co_nlocals),
        kwargs.get("co_stacksize", code.co_stacksize),
        kwargs.get("co_flags", code.co_flags),
        kwargs.get("co_code", code.co_code),
        kwargs.get("co_consts", code.co_consts),
        kwargs.get("co_names", code.co_names),
        kwargs.get("co_varnames", code.co_varnames),
        kwargs.get("co_filename", code.co_filename),
        kwargs.get("co_name", code.co_name),
        kwargs.get("co_firstlineno", code.co_firstlineno),
        kwargs.get("co_lnotab", code.co_lnotab),
        kwargs.get("co_freevars", code.co_freevars),
        kwargs.get("co_cellvars", code.co_cellvars),
    ]
    return types.CodeType(*params)


def validate_args(arg, snake_value, camelValue):
    """
    Validate arguments from two exclusive sources.
    This is a temporary function to be used while transitioning from using
    camelCase parameters to snake_case.
    """
    if isinstance(snake_value, str):
        if isinstance(camelValue, str):
            raise ConfigError(
                f"May not pass {arg!r} as snake_case and camelCase"
            )
    elif isinstance(camelValue, str):
        warnings.warn(
            "camelCase values is obsolete and will be removed in the "
            f"next major version -> use the new name {arg!r}"
        )
    return snake_value or camelValue
