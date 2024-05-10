"""A collection of functions which are triggered automatically by finder when
RNS package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_rns(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS."""
    _fix_init(finder, module)


def load_rns_cryptography(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS.Cryptography."""
    _fix_init(finder, module)


def load_rns_interfaces(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS.Interface."""
    _fix_init(finder, module)


def load_rns_interfaces_android(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS.Interface."""
    _fix_init(finder, module)


def load_rns_utilities(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS.Utilities."""
    _fix_init(finder, module)


def load_rns_vendor(finder: ModuleFinder, module: Module) -> None:
    """Patch RNS.vendor."""
    _fix_init(finder, module)


def _fix_init(finder: ModuleFinder, module: Module) -> None:
    """Patch the __init__ of the modules."""
    code_string = module.file.read_text(encoding="utf_8")
    code_string = code_string.replace('"/*.py"', '"/*.pyc"')
    code_string = code_string.replace("'__init__.py'", '"__init__.pyc"')
    code_string = code_string.replace('"__init__.py"', '"__init__.pyc"')
    code_string = code_string.replace("basename(f)[:-3]", "basename(f)[:-4]")
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )
