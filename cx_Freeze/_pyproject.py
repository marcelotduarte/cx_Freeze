"""Internal module."""

from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    from setuptools.compat.py310 import tomllib


def get_pyproject_tool_data() -> dict:
    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        return {}
    with pyproject_toml.open("rb") as file:
        config = tomllib.load(file)
    tool_data = config.get("tool", {}).get("cxfreeze", {})
    executables = []
    for executable in tool_data.pop("executables", []):
        if isinstance(executable, dict):
            executables.append(
                {json_compatible_key(k): v for k, v in executable.items()}
            )
        else:
            executables.append(executable)

    options = {}
    for cmd, data in tool_data.items():
        options.setdefault(cmd, {})
        for option, value in data.items():
            norm_key = json_compatible_key(option)
            options[cmd].setdefault(norm_key, ("tool.cxfreeze", value))
    options["executables"] = executables
    return options


def json_compatible_key(key: str) -> str:
    """As defined in :pep:`566#json-compatible-metadata`."""
    return key.lower().replace("-", "_")
