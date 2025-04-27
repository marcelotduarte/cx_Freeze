"""A collection of functions which are triggered automatically by finder when
zeroconf package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_zeroconf__services(
    finder: ModuleFinder,  # noqa: ARG001
    module: Module,
) -> None:
    """The zeroconf hooks."""
    module.global_names.update(
        [
            "ServiceListener",
            "ServiceStateChange",
            "Signal",
            "SignalRegistrationInterface",
        ]
    )


def load_zeroconf__services_info(
    finder: ModuleFinder,
    module: Module,  # noqa: ARG001
) -> None:
    """The zeroconf hooks."""
    finder.include_module("zeroconf._utils.ipaddress")


def load_zeroconf__listener(
    finder: ModuleFinder,
    module: Module,  # noqa: ARG001
) -> None:
    """The zeroconf hooks."""
    finder.include_module("zeroconf._handlers.answers")
