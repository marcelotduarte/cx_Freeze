"""Helper module to run tests on Linux, Windows and macOS.

Also works with variants like conda-forge and MSYS2 (Windows).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from sysconfig import get_platform

CI_DIR = Path(sys.argv[0]).parent.resolve()

PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", nargs="?")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--lines", action="store_true")
    parser.add_argument("--plain", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    platform = args.platform
    output = args.output
    indent = 2 if args.debug else None

    # filter the samples
    data = json.loads(CI_DIR.joinpath("build-test.json").read_bytes())
    samples = [
        sample
        for sample, options in data.items()
        if is_supported_platform(options.get("platform"), platform)
    ]
    if args.lines:
        buffer = "\n".join(samples)
    elif args.plain:
        buffer = " ".join(samples)
    else:
        buffer = json.dumps(samples, indent=indent)

    # output
    if output:
        with open(output, "w+", encoding="utf_8") as out:
            out.write(buffer)
    else:
        if args.debug:
            print("samples = ", end="")
        print(buffer)


if __name__ == "__main__":
    main()
