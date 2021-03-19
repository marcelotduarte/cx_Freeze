"""
Implements a new `Patchelf` interface to create an abstraction for patching
ELF files.
"""

from distutils.spawn import find_executable
from subprocess import check_call, check_output, CalledProcessError
import re


class Patchelf:
    """`Patchelf` is based on the logic around invoking `patchelf`."""

    def __init__(self) -> None:
        _verify_patchelf()

    def replace_needed(
        self, file_name: str, so_name: str, new_so_name: str
    ) -> None:
        check_call(
            ["patchelf", "--replace-needed", so_name, new_so_name, file_name]
        )

    def set_soname(self, file_name: str, new_so_name: str) -> None:
        check_call(["patchelf", "--set-soname", new_so_name, file_name])

    def set_rpath(self, file_name: str, rpath: str) -> None:
        check_call(["patchelf", "--remove-rpath", file_name])
        check_call(
            ["patchelf", "--force-rpath", "--set-rpath", rpath, file_name]
        )

    def get_rpath(self, file_name: str) -> str:
        try:
            rpath = (
                check_output(["patchelf", "--print-rpath", file_name])
                .decode("utf-8")
                .strip()
            )
        except CalledProcessError:
            rpath = ""
        return rpath


def _verify_patchelf() -> None:
    """
    This function looks for the ``patchelf`` external binary in the PATH,
    checks for the required version, and throws an exception if a proper
    version can't be found. Otherwise, silence is golden.
    """
    if not find_executable("patchelf"):
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
