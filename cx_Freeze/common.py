"""
This module contains utility functions shared between cx_Freeze modules.
"""

import types


def normalize_to_list(value) -> list:
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


def rebuild_code_object(co, code=None, constants=None, filename=None):
    """Rebuild the code object."""
    code = code or co.co_code
    constants = tuple(constants or co.co_consts)
    filename = filename or co.co_filename
    params = [
        co.co_argcount,
        co.co_kwonlyargcount,
        co.co_nlocals,
        co.co_stacksize,
        co.co_flags,
        code,
        constants,
        co.co_names,
        co.co_varnames,
        filename,
        co.co_name,
        co.co_firstlineno,
        co.co_lnotab,
        co.co_freevars,
        co.co_cellvars,
    ]
    if hasattr(co, "co_posonlyargcount"):
        # PEP570 added "positional only arguments" in Python 3.8
        params.insert(1, co.co_posonlyargcount)
    return types.CodeType(*params)
