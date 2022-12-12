"""A collection of functions which are triggered automatically by finder when
pycryptodome package is included."""

from __future__ import annotations

import os

from ..common import code_object_replace
from ..finder import ModuleFinder
from ..module import Module


def load_crypto_cipher(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Cipher subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_hash(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Hash subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_math(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Math subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_protocol(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Protocol subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_publickey(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.PublicKey subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_util(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Util subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_crypto_util__file_system(
    finder: ModuleFinder, module: Module  # pylint: disable=unused-argument
) -> None:
    """The patch for pycryptodome package."""
    # WARNING: do not touch this code string
    code_to_inject = """
import os

def pycryptodome_filename(dir_comps, filename):
    import sys
    if dir_comps[0] != "Crypto":
        raise ValueError("Only available for modules under 'Crypto'")
    dir_comps = list(dir_comps) + [filename]
    root_lib = os.path.join(os.path.dirname(sys.executable), "lib")
    return os.path.join(root_lib, ".".join(dir_comps))
"""
    if module.in_file_system == 0 and module.code is not None:
        new_code = compile(code_to_inject, os.fspath(module.file), "exec")
        co_func = new_code.co_consts[2]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, constant in enumerate(consts):
            if isinstance(constant, type(code)) and constant.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)
