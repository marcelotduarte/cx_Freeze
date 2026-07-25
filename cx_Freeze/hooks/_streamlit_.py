"""Hooks triggered by finder when streamlit package is included."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for 'streamlit' package."""

    def streamlit(self, finder: ModuleFinder, module: Module) -> None:
        """Load as a package the package streamlit in the file system."""
        dist = module.distribution
        if dist is not None:
            version = tuple(map(int, dist.version))
            if version < (1, 51):  # pragma: nocover
                version_str = ".".join(tuple(map(str, dist.version)))
                msg = (
                    f"cx_Freeze does not support 'streamlit {version_str}'.\n"
                    "Please upgrade 'streamlit>=1.51'."
                )
                raise SystemExit(msg)

        module.in_file_system = 1
        finder.exclude_module("streamlit.testing")
        finder.include_package("streamlit")

    def streamlit_runtime_scriptrunner_script_runner(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Include a required submodule."""
        finder.include_module("streamlit.runtime.scriptrunner.magic_funcs")
