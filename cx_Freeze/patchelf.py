"""
Implements a new `Patchelf` interface to create an abstraction for patching
ELF files.
"""

from pathlib import Path
from shutil import which
from subprocess import check_call, check_output, CalledProcessError
import re
from typing import Union


class Patchelf:
    """`Patchelf` is based on the logic around invoking `patchelf`."""

    def __init__(self) -> None:
        _verify_patchelf()

    def get_rpath(self, filename: Union[str, Path]) -> str:
        args = ["patchelf", "--print-rpath", filename]
        try:
            rpath = check_output(args).decode("utf-8").strip()
        except CalledProcessError:
            rpath = ""
        return rpath

    def replace_needed(
        self, filename: Union[str, Path], so_name: str, new_so_name: str
    ) -> None:
        args = ["patchelf", "--replace-needed", so_name, new_so_name, filename]
        check_call(args)

    def set_rpath(self, filename: Union[str, Path], rpath: str) -> None:
        args = ["patchelf", "--remove-rpath", filename]
        check_call(args)
        args = ["patchelf", "--force-rpath", "--set-rpath", rpath, filename]
        check_call(args)

    def set_soname(self, filename: Union[str, Path], new_so_name: str) -> None:
        args = ["patchelf", "--set-soname", new_so_name, filename]
        check_call(args)


def _verify_patchelf() -> None:
    """
    This function looks for the ``patchelf`` external binary in the PATH,
    checks for the required version, and throws an exception if a proper
    version can't be found. Otherwise, silence is golden.
    """
    if not which("patchelf"):
        raise ValueError("Cannot find required utility `patchelf` in PATH")
    try:
        version = check_output(["patchelf", "--version"]).decode("utf-8")
    except CalledProcessError:
        raise ValueError("Could not call `patchelf` binary") from None

    mobj = re.match(r"patchelf\s+(\d+(.\d+)?)", version)
    if mobj and tuple(int(x) for x in mobj.group(1).split(".")) >= (0, 9):
        return
    raise ValueError(
        f"patchelf {version} found. cx-freeze requires patchelf >= 0.9."
    )
