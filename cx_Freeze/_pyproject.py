"""Internal module."""

from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def get_pyproject_options() -> dict:
    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        return {}
    with pyproject_toml.open("rb") as file:
        data = tomllib.load(file)
    config = data.get("tool", {}).get("cxfreeze", {})

    executables = []
    for executable in config.pop("executables", []):
        if isinstance(executable, dict):
            executables.append(
                {json_compatible_key(k): v for k, v in executable.items()}
            )
        else:
            executables.append(executable)
    config["executables"] = executables
    return config

    options = {}
    for cmd, data in config.items():
        options.setdefault(cmd, {})
        for option, value in data.items():
            norm_key = json_compatible_key(option)
            options[cmd].setdefault(norm_key, value)
    options["executables"] = executables
    return options


def json_compatible_key(key: str) -> str:
    """As defined in :pep:`566#json-compatible-metadata`."""
    return key.lower().replace("-", "_")


def update_command_options(
    command_options: dict, pyproject_options: dict
) -> dict:
    for cmd, config in pyproject_options.items():
        norm_cmd = json_compatible_key(cmd)
        command_options.setdefault(norm_cmd, {})
        for key, value in config.items():
            norm_key = json_compatible_key(key)
            command_options[norm_cmd][norm_key] = ("tool.cxfreeze", value)
    return command_options
