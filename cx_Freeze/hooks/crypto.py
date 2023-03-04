"""A collection of functions which are triggered automatically by finder when
pycryptodome package is included.
"""

from __future__ import annotations

from ..common import code_object_replace_function
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
    finder: ModuleFinder, module: Module  # noqa: ARG001
) -> None:
    """The patch for pycryptodome package."""
    code = module.code
    if module.in_file_system == 0 and code is not None:
        name = "pycryptodome_filename"
        source = f"""\
        def {name}(dir_comps, filename):
            import os, sys
            if dir_comps[0] != "Crypto":
                raise ValueError("Only available for modules under 'Crypto'")
            dir_comps = list(dir_comps) + [filename]
            root_lib = os.path.join(sys.frozen_dir, "lib")
            return os.path.join(root_lib, ".".join(dir_comps))
        """
        module.code = code_object_replace_function(code, name, source)
