"""A collection of functions which are triggered automatically by finder when
RNS package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for RNS."""

    def rns(self, finder: ModuleFinder, module: Module) -> None:
        """Patch RNS."""
        self._fix_init(finder, module)

    def rns_cryptography(self, finder: ModuleFinder, module: Module) -> None:
        """Patch RNS.Cryptography."""
        self._fix_init(finder, module)

    def rns_interfaces(self, finder: ModuleFinder, module: Module) -> None:
        """Patch RNS.Interface."""
        self._fix_init(finder, module)

    def rns_interfaces_android(
        self, finder: ModuleFinder, module: Module
    ) -> None:
        """Patch RNS.Interface."""
        self._fix_init(finder, module)

    def rns_utilities(self, finder: ModuleFinder, module: Module) -> None:
        """Patch RNS.Utilities."""
        self._fix_init(finder, module)

    def rns_vendor(self, finder: ModuleFinder, module: Module) -> None:
        """Patch RNS.vendor."""
        self._fix_init(finder, module)

    def _fix_init(self, finder: ModuleFinder, module: Module) -> None:
        """Patch the __init__ of the modules."""
        code_string = module.file.read_text(encoding="utf_8")
        code_string = code_string.replace('"/*.py"', '"/*.pyc"')
        code_string = code_string.replace("'__init__.py'", '"__init__.pyc"')
        code_string = code_string.replace('"__init__.py"', '"__init__.pyc"')
        code_string = code_string.replace(
            "basename(f)[:-3]", "basename(f)[:-4]"
        )
        module.code = compile(
            code_string,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )
