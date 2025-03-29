"""A collection of functions which are triggered automatically by finder when
pydantic package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_pydantic(finder: ModuleFinder, module: Module) -> None:
    """The pydantic package is compiled by Cython (the imports are hidden)."""
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
            finder.include_module("dataclasses")  # support in v 1.7+
        with suppress(ImportError):
            finder.include_module("typing_extensions")  # support in v 1.8+


def load_pydantic__internal__core_utils(_, module: Module) -> None:
    """Exclude optional modules."""
    module.exclude_names.add("rich")


def load_pydantic__internal__typing_extra(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("eval_type_backport")


def load_pydantic_networks(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("email_validator")


def load_pydantic_v1(_, module: Module) -> None:
    """The pydantic package is compiled by Cython (the imports are hidden)."""
    module.global_names.add("BaseModel")


def load_pydantic_v1_env_settings(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("dotenv")


def load_pydantic_v1_networks(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("email_validator")


def load_pydantic_v1_version(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("cython")
