"""
This module contains utility functions shared between cx_Freeze modules.
"""

from pathlib import Path, PurePath
import types
from typing import List, Tuple, Optional, Union
import warnings

from .exception import ConfigError

IncludesList = List[
    Union[str, Path, Tuple[Union[str, Path], Optional[Union[str, Path]]]]
]
InternalIncludesList = List[Tuple[Path, PurePath]]


def get_resource_file_path(
    dirname: Union[str, Path], name: Union[str, Path], ext: str
) -> Optional[Path]:
    """
    Return the path to a resource file shipped with cx_Freeze.

    This is used to find our base executables and initscripts when they are
    just specified by name.
    """
    pname = Path(name)
    if pname.is_absolute():
        return pname
    pname = Path(__file__).resolve().parent / dirname / pname.with_suffix(ext)
    if pname.exists():
        return pname
    return None


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


def process_path_specs(specs: Optional[IncludesList]) -> InternalIncludesList:
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
    processed_specs: InternalIncludesList = []
    for spec in specs:
        if not isinstance(spec, (list, tuple)):
            source = spec
            target = None
        elif len(spec) != 2:
            error = "path spec must be a list or tuple of length two"
            raise ConfigError(error)
        else:
            source, target = spec
        source = Path(source)
        if not source.exists():
            raise ConfigError(f"cannot find file/directory named {source!s}")
        target = PurePath(target or source.name)
        if target.is_absolute():
            error = f"target path named {target!s} cannot be absolute"
            raise ConfigError(error)
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


def validate_args(arg, snake_value, camel_value):
    """
    Validate arguments from two exclusive sources.
    This is a temporary function to be used while transitioning from using
    camelCase parameters to snake_case.
    """
    if isinstance(snake_value, str):
        if isinstance(camel_value, str):
            raise ConfigError(
                f"May not pass {arg!r} as snake_case and camelCase"
            )
    elif isinstance(camel_value, str):
        warnings.warn(
            "camelCase values is obsolete and will be removed in the "
            f"next major version -> use the new name {arg!r}"
        )
    return snake_value or camel_value
