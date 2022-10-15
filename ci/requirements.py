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
    requirements_dev = root_dir / "requirements-dev.txt"

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
        contents_str = "\n".join(contents)
        requirements.write_text(contents_str, encoding="utf_8")
    except KeyError:
        pass
    else:
        print(requirements, "ok")

    try:
        extras_require = config["options.extras_require"]
        for k, require in extras_require.items():
            contents.append(f"#{k}\n{require}".replace("\n\n", "\n"))
        contents.append("")
        contents_str = "\n".join(contents)
        requirements_dev.write_text(contents_str, encoding="utf_8")
    except KeyError:
        pass
    else:
        print(requirements_dev, "ok")


if __name__ == "__main__":
    main()
