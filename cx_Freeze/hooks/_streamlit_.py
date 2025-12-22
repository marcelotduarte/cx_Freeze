"""A collection of functions which are triggered automatically by finder when
streamlit package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for 'streamlit' package."""

    def streamlit(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """The streamlit must be loaded as a package."""
        finder.exclude_module("streamlit.testing")
        finder.include_package("streamlit")

    def streamlit_runtime_scriptrunner_script_runner(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include a required submodule."""
        finder.include_module("streamlit.runtime.scriptrunner.magic_funcs")
