"""Functions that operate on bytecodes."""

from __future__ import annotations

import logging
import sys
from opcode import opmap
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from types import CodeType

if sys.version_info[:2] >= (3, 13):
    from dis import _unpack_opargs
else:
    from dis import _unpack_opargs as dis_unpack_opargs

    def _unpack_opargs(co_code) -> Generator:
        for i, op, arg in dis_unpack_opargs(co_code):
            yield (i, i, op, arg)


CALL = opmap.get("CALL")  # Python 3.11+
CALL_FUNCTION = opmap.get("CALL_FUNCTION")  # Python <= 3.10
PRECALL = opmap.get("PRECALL")  # Python 3.11 only
PUSH_NULL = opmap.get("PUSH_NULL")  # Python 3.11+

EXTENDED_ARG = opmap["EXTENDED_ARG"]
LOAD_CONST = opmap["LOAD_CONST"]
LOAD_NAME = opmap["LOAD_NAME"]
LOAD_SMALL_INT = opmap.get("LOAD_SMALL_INT")  # Python 3.14

IMPORT_NAME = opmap["IMPORT_NAME"]
IMPORT_FROM = opmap["IMPORT_FROM"]
IMPORT_STAR = opmap.get("IMPORT_STAR")  # Python up to 3.11
CALL_INTRINSIC_1 = opmap.get("CALL_INTRINSIC_1")  # Python 3.12+

STORE_NAME = opmap["STORE_NAME"]
STORE_GLOBAL = opmap["STORE_GLOBAL"]
STORE_OPS = (STORE_NAME, STORE_GLOBAL)


logger = logging.getLogger(__name__)

__all__ = ["scan_code"]


def scan_code(code: CodeType) -> Generator:
    arguments = []
    names = code.co_names
    consts = code.co_consts
    for _i, _offset, opc, arg in _unpack_opargs(code.co_code):
        # keep track of constants (these are used for importing)
        # immediately restart loop so arguments are retained
        if opc == LOAD_CONST:
            arguments.append(consts[arg])
            continue
        # constants in Python 3.14
        if LOAD_SMALL_INT and opc == LOAD_SMALL_INT:
            arguments.append(arg)
            continue

        # keep track of the name which can be the name of the import func
        if opc == LOAD_NAME:
            arguments.append(names[arg])
            continue

        if PUSH_NULL and opc == PUSH_NULL:
            continue  # ignore it in Python 3.13+ (exists in 3.11+)

        if PRECALL and opc == PRECALL:
            continue  # ignore it in Python 3.11

        if (opc, arg) == (CALL or CALL_FUNCTION, 1) and len(arguments) >= 2:
            # Python 3.6-3.10 bytecode of a __import__ call:
            # 1            0 LOAD_NAME                0 (__import__)
            #              2 LOAD_CONST               0 ('pkgutil')
            #              4 CALL_FUNCTION            1
            # Python 3.11 bytecode of a __import__ call:
            # 1            2 PUSH_NULL
            #              4 LOAD_NAME                0 (__import__)
            #              6 LOAD_CONST               0 ('pkgutil')
            #              8 PRECALL                  1
            #             12 CALL                     1
            # Python 3.12 bytecode of a __import__ call:
            # 1            2 PUSH_NULL
            #              4 LOAD_NAME                0 (__import__)
            #              6 LOAD_CONST               0 ('pkgutil')
            #              8 CALL                     1
            # Python 3.13-3.14 bytecode of a __import__ call:
            # 1            2 LOAD_NAME                0 (__import__)
            #              4 PUSH_NULL
            #              6 LOAD_CONST               0 ('pkgutil')
            #              8 CALL                     1
            func = arguments[-2]
            if func in ("__import__", "import_module"):
                name = arguments[-1]
                yield func, (name, -1, [])

        # import statement: attempt to import module
        elif opc == IMPORT_NAME:
            name = names[arg]
            if len(arguments) >= 2:
                relative_import_index, from_list = arguments[-2:]
            else:
                relative_import_index = -1
                from_list = arguments[0] if arguments else None
            yield "import", (name, relative_import_index, from_list)

        # import * statement: copy all global names
        elif IMPORT_STAR and opc == IMPORT_STAR:
            # Python up to 3.11
            yield "star", ()
        elif CALL_INTRINSIC_1 and (opc, arg) == (CALL_INTRINSIC_1, 2):
            # Python 3.12+
            yield "star", ()

        # store operation: track only top level
        elif opc in STORE_OPS:
            name = names[arg]
            yield "store", (name,)

        # reset arguments; these are only needed for import statements so
        # ignore them in all other cases!
        arguments = []
