"""Internal module."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, TypeAlias

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    from setuptools.compat.py310 import tomllib

if TYPE_CHECKING:
    _CommandOptions: TypeAlias = dict[str, dict[str, tuple[str, str]]]
    _Executables: TypeAlias = list[str | dict[str, str]]
    _Options: TypeAlias = dict[str, dict[str, str]]


def get_pyproject_options() -> tuple[_Options, _Executables]:
    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        return {}, []
    with pyproject_toml.open("rb") as file:
        config = tomllib.load(file)
    tool_cxfreeze = config.get("tool", {}).get("cxfreeze", {})
    executables: _Executables = tool_cxfreeze.pop("executables", [])
    for i, executable in enumerate(executables):
        if isinstance(executable, dict):
            executables[i] = {
                json_compatible_key(k): v for k, v in executable.items()
            }
    return tool_cxfreeze, executables


def json_compatible_key(key: str) -> str:
    """As defined in :pep:`566#json-compatible-metadata`."""
    return key.lower().replace("-", "_")


def update_command_options(
    command_options: _CommandOptions,
    pyproject_options: _Options,
    setup_options: _Options,
) -> _CommandOptions:
    for cmd, config in setup_options.items():
        norm_cmd = json_compatible_key(cmd)
        command_options.setdefault(norm_cmd, {})
        for key, value in config.items():
            norm_key = json_compatible_key(key)
            command_options[norm_cmd][norm_key] = ("setup script", value)
    for cmd, config in pyproject_options.items():
        norm_cmd = json_compatible_key(cmd)
        command_options.setdefault(norm_cmd, {})
        for key, value in config.items():
            norm_key = json_compatible_key(key)
            command_options[norm_cmd][norm_key] = ("tool.cxfreeze", value)
    return command_options
