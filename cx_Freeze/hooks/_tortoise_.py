"""A collection of functions which are triggered automatically by finder when
tortoise-orm package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for tortoise-orm."""

    def tortoise(self, finder: ModuleFinder, module: Module) -> None:
        """Add the tortoise-orm metadata."""
        # Fix the metadata
        module.update_distribution("tortoise-orm")
        # Ignore optional modules
        module.ignore_names.add("yaml")

        finder.exclude_module("tortoise.testing")
        finder.include_package("tortoise.backends")

    def tortoise_backends_asyncpg_client(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["asyncpg", "asyncpg.transaction"])

    def tortoise_backends_asyncpg_executor(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.add("asyncpg")

    def tortoise_backends_mysql_client(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
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

    def tortoise_backends_odbc_client(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["asyncodbc", "pyodbc"])

    def tortoise_backends_oracle_client(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["asyncodbc", "ciso8601", "pyodbc"])

    def tortoise_backends_psycopg_client(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
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

    def tortoise_fields_data(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        """Ignore optional modules."""
        module.ignore_names.update(["ciso8601", "orjson"])
