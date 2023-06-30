"""Common utility functions shared between cx_Freeze modules."""

from __future__ import annotations

import shutil
from contextlib import suppress
from pathlib import Path, PurePath
from tempfile import TemporaryDirectory
from textwrap import dedent
from types import CodeType
from typing import List, Optional, Tuple, Union

from .exception import OptionError

IncludesList = List[
    Union[str, Path, Tuple[Union[str, Path], Optional[Union[str, Path]]]]
]

InternalIncludesList = List[Tuple[Path, PurePath]]


class FilePath(Path):
    """Subclass of concrete Path to be used in TemporaryPath."""

    _flavour = type(Path())._flavour

    def replace(self, target):
        """Rename this path to the target path, overwriting if that path
        exists. Extended to support move between file systems.
        """
        with suppress(OSError):
            return super().replace(target)
        shutil.copyfile(self, target)
        with suppress(FileNotFoundError):
            self.unlink()
        return self.__class__(target)


class TemporaryPath(TemporaryDirectory):
    """Create and return a Path-like temporary directory."""

    def __init__(
        self, filename=None, suffix=None, prefix=None, dir=None  # noqa: A002
    ):
        super().__init__(suffix, prefix or "cxfreeze-", dir)
        if filename:
            if Path(filename).parent.name:
                raise ValueError("filename cannot contain directory")
            self.path = FilePath(self.name, filename)
        else:
            self.path = FilePath(self.name)

    def __enter__(self):
        return self.path


def get_resource_file_path(
    dirname: str | Path, name: str | Path, ext: str
) -> Path | None:
    """Return the path to a resource file shipped with cx_Freeze.

    This is used to find our base executables and initscripts when they are
    just specified by name.
    """
    pname = Path(name)
    if pname.is_absolute():
        return pname
    pname = Path(__file__).resolve().parent / dirname / pname.with_suffix(ext)
    if pname.exists():
        return pname
    # Support for name argument in the old Camelcase value
    pname = pname.with_name(pname.name.lower())
    if pname.exists():
        return pname
    return None


def normalize_to_list(
    value: str | list[str] | tuple[str, ...] | None
) -> list[str]:
    """Takes the different formats of options containing multiple values and
    returns the value as a list object.
    """
    if value is None:
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
            error = "path spec must be a list or tuple of length two"
            raise OptionError(error)
        else:
            source, target = spec
        source = Path(source)
        if not source.exists():
            raise OptionError(f"cannot find file/directory named {source!s}")
        target = PurePath(target or source.name)
        if target.is_absolute():
            error = f"target path named {target!s} cannot be absolute"
            raise OptionError(error)
        processed_specs.append((source, target))
    return processed_specs


def code_object_replace(code: CodeType, **kwargs) -> CodeType:
    """Return a copy of the code object with new values for the specified
    fields.
    """
    with suppress(ValueError, KeyError):
        kwargs["co_consts"] = tuple(kwargs["co_consts"])
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
    return CodeType(*params)


def code_object_replace_function(
    code: CodeType, name: str, source: str
) -> CodeType:
    """Return a copy of the code object with the function 'name' replaced."""
    if code is None:
        return code

    new_code = compile(dedent(source), code.co_filename, "exec")
    new_co_func = None
    for constant in new_code.co_consts:
        if isinstance(constant, CodeType) and constant.co_name == name:
            new_co_func = constant
            break
    if new_co_func is None:
        return code

    consts = list(code.co_consts)
    for i, constant in enumerate(consts):
        if isinstance(constant, CodeType) and constant.co_name == name:
            consts[i] = code_object_replace(
                new_co_func, co_firstlineno=constant.co_firstlineno
            )
            break
    return code_object_replace(code, co_consts=consts)
