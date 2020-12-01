"""
This module contains utility functions shared between cx_Freeze modules.
"""

import os.path
import types
from typing import Any, List, Tuple, Optional, Union


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
    specs: List[Union[str, Tuple[str, str]]]
) -> List[Tuple[str, str]]:
    """
    Prepare paths specified as config.

    The input is a list of either strings, or 2-tuples (source, target).
    Where single strings are supplied, the basenames are used as targets.
    Where targets are given explicitly, they must not be absolute paths.

    Returns a list of 2-tuples, or throws ConfigError if something is wrong
    in the input.
    """
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


def rebuild_code_object(
    code: types.CodeType,
    codestring: Optional[bytes] = None,
    constants: Optional[Tuple[Any, ...]] = None,
    filename: Optional[str] = None,
) -> types.CodeType:
    """Rebuild the code object."""
    codestring: bytes = codestring or code.co_code
    constants: Tuple[Any, ...] = tuple(constants or code.co_consts)
    filename: str = filename or code.co_filename
    params = [
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_nlocals,
        code.co_stacksize,
        code.co_flags,
        codestring,
        constants,
        code.co_names,
        code.co_varnames,
        filename,
        code.co_name,
        code.co_firstlineno,
        code.co_lnotab,
        code.co_freevars,
        code.co_cellvars,
    ]
    if hasattr(code, "co_posonlyargcount"):
        # PEP570 added "positional only arguments" in Python 3.8
        params.insert(1, code.co_posonlyargcount)
    return types.CodeType(*params)


class ConfigError(Exception):
    """
    Raised when an error is detected in the configuration.
    The associated value is a string indicating what precisely went wrong.
    """

    def __init__(self, msg: str):
        self.what = msg
        super().__init__()

    def __str__(self):
        return self.what
