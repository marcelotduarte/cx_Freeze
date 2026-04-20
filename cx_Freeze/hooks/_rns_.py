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
        loader = module.loader
        path = loader.get_filename(module.name)
        source_code = loader.get_source(module.name)
        source_code = source_code.replace('"/*.py"', '"/*.pyc"')
        source_code = source_code.replace("'__init__.py'", '"__init__.pyc"')
        source_code = source_code.replace('"__init__.py"', '"__init__.pyc"')
        source_code = source_code.replace(
            "basename(f)[:-3]", "basename(f)[:-4]"
        )
        module.code = loader.source_to_code(
            source_code, path, _optimize=finder.optimize
        )
