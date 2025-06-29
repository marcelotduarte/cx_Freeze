"""A collection of functions which are triggered automatically by finder when
pydantic package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for pydantic."""

    def pydantic(self, finder: ModuleFinder, module: Module) -> None:
        """The pydantic package is compiled by Cython
        (the imports are hidden).
        """
        module.global_names.update(
            [
                "BaseModel",
                "PydanticSchemaGenerationError",
                "PydanticUndefinedAnnotation",
                "PydanticUserError",
            ]
        )
        if module.distribution.version < (2,):
            finder.include_module("colorsys")
            finder.include_module("datetime")
            finder.include_module("decimal")
            finder.include_module("functools")
            finder.include_module("ipaddress")
            finder.include_package("json")
            finder.include_module("pathlib")
            finder.include_module("uuid")
            with suppress(ImportError):
                finder.include_module("dataclasses")  # support in v1.7+
            with suppress(ImportError):
                finder.include_module("typing_extensions")  # support in v1.8+

    def pydantic__internal__core_utils(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Exclude optional modules."""
        module.exclude_names.add("rich")

    def pydantic__internal__typing_extra(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("eval_type_backport")

    def pydantic_networks(self, _finder: ModuleFinder, module: Module) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("email_validator")

    def pydantic_v1(self, _finder: ModuleFinder, module: Module) -> None:
        """The pydantic package is compiled by Cython
        (the imports are hidden).
        """
        module.global_names.add("BaseModel")

    def pydantic_v1_env_settings(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("dotenv")

    def pydantic_v1_networks(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("email_validator")

    def pydantic_v1_version(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("cython")
