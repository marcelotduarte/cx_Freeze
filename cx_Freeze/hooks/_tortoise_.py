"""A collection of functions which are triggered automatically by finder when
tortoise-orm package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_tortoise(finder: ModuleFinder, module: Module) -> None:
    """Add the tortoise-orm metadata."""
    # Ignore optional modules
    module.ignore_names.add("yaml")
    # Fix the metadata
    module.update_distribution("tortoise-orm")

    finder.exclude_module("tortoise.testing")
    finder.include_package("tortoise.backends")


def load_tortoise_backends_asyncpg_client(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(["asyncpg", "asyncpg.transaction"])


def load_tortoise_backends_asyncpg_executor(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.add("asyncpg")


def load_tortoise_backends_mysql_client(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(
        [
            "aiomysql",
            "asyncmy",
            "asyncmy.charset",
            "pymysql",
            "pymysql.charset",
        ]
    )


def load_tortoise_backends_odbc_client(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(["asyncodbc", "pyodbc"])


def load_tortoise_backends_oracle_client(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(["asyncodbc", "ciso8601", "pyodbc"])


def load_tortoise_backends_psycopg_client(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(
        [
            "psycopg",
            "psycopg.conninfo",
            "psycopg.pq",
            "psycopg.rows",
            "psycopg_pool",
        ]
    )


def load_tortoise_fields_data(_, module: Module) -> None:
    """Ignore optional modules."""
    module.ignore_names.update(["ciso8601", "orjson"])
