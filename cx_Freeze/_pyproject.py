"""Internal module."""

from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def get_pyproject_tool_data() -> dict:
    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        return {}
    with pyproject_toml.open("rb") as file:
        data = tomllib.load(file)
    tool_data = data.get("tool", {}).get("cxfreeze", {})

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
