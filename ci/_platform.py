"""Helper module to run tests on Linux, Windows and macOS.

Also works with variants like conda-forge and MSYS2 (Windows).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from sysconfig import get_platform, get_python_version

CI_DIR = Path(sys.argv[0]).parent.resolve()

PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")
PYVERSION = get_python_version()


def is_supported_platform(
    platform: str | list[str] | None, platform_in_use: str | None = None
) -> bool:
    if isinstance(platform, str):
        platform = platform.split(",")
    if not platform:  # if not specified, all platforms are supported
        return True
    if platform_in_use is None:
        if IS_MACOS:
            platform_in_use = "macos"
        elif IS_MINGW:
            platform_in_use = "mingw"
        elif IS_WINDOWS:
            platform_in_use = "windows"
        else:
            platform_in_use = "linux"
    platform_support = {"linux", "macos", "mingw", "windows"}
    platform_yes = {plat for plat in platform if not plat.startswith("!")}
    if platform_yes:
        platform_support = platform_yes
    platform_not = {plat[1:] for plat in platform if plat.startswith("!")}
    if platform_not:
        platform_support -= platform_not
    return platform_in_use in platform_support


def is_supported_python(
    python_versions: str | list[str] | None, python_version: str | None = None
) -> bool:
    if isinstance(python_versions, str):
        python_versions = python_versions.split(",")
    if not python_versions:  # all python_versions are supported
        return True
    return python_version in python_versions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", nargs="?")
    parser.add_argument("--py", default=PYVERSION, dest="python_versions")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--lines", action="store_true")
    parser.add_argument("--matrix", action="store_true")
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    platform = args.platform
    output = args.output
    indent = 2 if args.debug else None

    # filter the samples
    data = json.loads(CI_DIR.joinpath("build-test.json").read_bytes())
    matrix = []
    for py_version in args.python_versions.split(","):
        matrix += [
            {"sample": sample, "python-version": py_version}
            for sample, options in data.items()
            if is_supported_platform(options.get("platform"), platform)
            and is_supported_python(options.get("python-versions"), py_version)
        ]
    if args.lines:
        buffer = "\n".join(
            f"{include['sample']}\t{include['python-version']}"
            for include in matrix
        )
    elif args.plain:
        buffer = " ".join(sorted({include["sample"] for include in matrix}))
    else:
        buffer = json.dumps(matrix, indent=indent)

    # output
    if output:
        output_mode = "a+" if os.path.exists(output) else "w+"
        with open(output, output_mode, encoding="utf_8") as out:
            if args.matrix:
                out.write('matrix={"include": ')
            out.write(buffer)
            if args.matrix:
                out.write("}\n")
    elif args.matrix:
        print('matrix={"include": ' + buffer + "}")
    else:
        print(buffer)


if __name__ == "__main__":
    main()
