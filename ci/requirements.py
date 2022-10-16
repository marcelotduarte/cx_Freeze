"""Requirements sync."""

import sys
from configparser import ConfigParser
from pathlib import Path


def main():
    """Entry point."""

    config = ConfigParser()
    files = config.read(["setup.cfg", "../setup.cfg"])
    if not files:
        print("setup.cfg not found", file=sys.stderr)
        sys.exit(1)

    root_dir = Path(files[0]).parent
    requirements = root_dir / "requirements.txt"
    requires_dev = root_dir / "requirements-dev.txt"

    contents = [
        "--extra-index-url https://marcelotduarte.github.io/packages/",
        "",
    ]

    try:
        install_requires = config["options"]["install_requires"].splitlines()
        for line in install_requires:
            if " and python_version < '3.10'" in line:
                line = line.replace(" and python_version < '3.10'", "")
            contents.append(line)
        contents.append("")
        with requirements.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(contents))
    except KeyError:
        pass
    else:
        print(requirements, "ok")

    try:
        extras_require = config["options.extras_require"]
        for extra, require in extras_require.items():
            contents.append(f"# {extra}\n{require}".replace("\n\n", "\n"))
        contents.append("")
        with requires_dev.open(mode="w", encoding="utf_8", newline="") as file:
            file.write("\n".join(contents))
    except KeyError:
        pass
    else:
        print(requires_dev, "ok")


if __name__ == "__main__":
    main()
