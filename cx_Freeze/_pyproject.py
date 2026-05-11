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
    executables = tool_data.pop("executables", [])
    options = {}
    for cmd, data in tool_data.items():
        for option, value in data.items():
            options.setdefault(cmd, {})
            options[cmd].setdefault(option, ("tool.cxfreeze", value))
    options["executables"] = executables
    return options
