"""Requirements sync."""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

try:
    from tomllib import load as toml_load
except ImportError:
    from tomli import load as toml_load


def main() -> None:
    """Entry point."""
    pyproject_toml = Path("pyproject.toml")
    if not pyproject_toml.exists():
        print("pyproject.toml not found", file=sys.stderr)
        sys.exit(1)
    with pyproject_toml.open("rb") as file:
        config = toml_load(file)

    root_dir = pyproject_toml.parent
    requirements = root_dir / "requirements.txt"

    try:
        dependencies = config["project"]["dependencies"]
        contents = list(dependencies)
        contents.append("")
        with requirements.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(contents))
    except KeyError:
        pass
    else:
        print(requirements, "ok")

    dependency_groups = []
    with contextlib.suppress(KeyError):
        dependency_groups.append(config["project"]["optional-dependencies"])
    with contextlib.suppress(KeyError):
        dependency_groups.append(config["dependency-groups"])
    for groups in dependency_groups:
        for extra, dependencies in groups.items():
            if root_dir.joinpath(extra).is_dir():
                requirements = root_dir / extra / "requirements.txt"
            else:
                requirements = root_dir / f"requirements-{extra}.txt"
            contents = dependencies.copy()
            contents.append("")
            with requirements.open(
                mode="w", encoding="utf_8", newline=""
            ) as file:
                file.write("\n".join(contents))
            print(requirements, "ok")


if __name__ == "__main__":
    main()
