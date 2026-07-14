"""Hooks triggered by finder when zeroconf package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for zeroconf."""

    def zeroconf__services(
        self,
        finder: ModuleFinder,  # noqa: ARG002
        module: Module,
    ) -> None:
        """Inclide global names to zeroconf hooks."""
        module.global_names.update(
            [
                "ServiceListener",
                "ServiceStateChange",
                "Signal",
                "SignalRegistrationInterface",
            ]
        )

    def zeroconf__services_info(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include hidden module."""
        finder.include_module("zeroconf._utils.ipaddress")

    def zeroconf__listener(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include hidden module."""
        finder.include_module("zeroconf._handlers.answers")
