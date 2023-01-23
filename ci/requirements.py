"""Requirements sync."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    from setuptools.extern import tomli as tomllib


def main():
    """Entry point."""

    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        print("pyproject.toml not found", file=sys.stderr)
        sys.exit(1)
    with pyproject_toml.open("rb") as file:
        config = tomllib.load(file)

    root_dir = pyproject_toml.parent
    requirements = root_dir / "requirements.txt"
    requires_dev = root_dir / "requirements-dev.txt"

    contents = [
        "--extra-index-url https://marcelotduarte.github.io/packages/",
        "",
    ]

    try:
        dependencies = config["project"]["dependencies"]
        for dependency in dependencies:
            if " and python_version < '3.10'" in dependency:
                dependency = dependency.replace(
                    " and python_version < '3.10'", ""
                )
            contents.append(dependency)
        contents.append("")
        with requirements.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(contents))
    except KeyError:
        pass
    else:
        print(requirements, "ok")

    try:
        extras_require = config["project"]["optional-dependencies"]
        for extra, dependencies in extras_require.items():
            contents.append(f"# {extra}")
            for dependency in dependencies:
                contents.append(dependency)
        contents.append("")
        with requires_dev.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(contents))
    except KeyError:
        pass
    else:
        print(requires_dev, "ok")


if __name__ == "__main__":
    main()
