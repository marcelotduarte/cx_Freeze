"""
Implements a new `Patchelf` interface to create an abstraction for patching
ELF files.
"""

from pathlib import Path
from shutil import which
from subprocess import check_call, check_output, run, CalledProcessError, PIPE
import re
from typing import Any, Dict, Set, Union


class Patchelf:
    """`Patchelf` is based on the logic around invoking `patchelf`."""

    def __init__(self) -> None:
        _verify_patchelf()

    def get_needed(
        self,
        path: Union[str, Path],
        linker_warnings: Dict[Path, Any],
        show_warnings: bool,
    ) -> Set[Path]:
        dependent_files: Set[Path] = set()
        split_string = " => "
        dependent_file_index = 1
        args = ("ldd", path)
        process = run(args, encoding="utf-8", stdout=PIPE, stderr=PIPE)
        for line in process.stdout.splitlines():
            parts = line.expandtabs().strip().split(split_string)
            if len(parts) != 2:
                continue
            dependent_file = parts[dependent_file_index].strip()
            if dependent_file == path.name:
                continue
            if dependent_file in ("not found", "(file not found)"):
                filename = parts[0]
                if filename not in linker_warnings:
                    linker_warnings[filename] = None
                    if show_warnings:
                        print(f"WARNING: cannot find {filename!r}")
                continue
            if dependent_file.startswith("("):
                continue
            pos = dependent_file.find(" (")
            if pos >= 0:
                dependent_file = dependent_file[:pos].strip()
            if dependent_file:
                dependent_files.add(Path(dependent_file))
        if process.returncode and show_warnings:
            print("WARNING:", *args, "returns:")
            print(process.stderr, end="")
        return dependent_files

    def get_rpath(self, filename: Union[str, Path]) -> str:
        args = ["patchelf", "--print-rpath", filename]
        try:
            rpath = check_output(args, encoding="utf-8").strip()
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
        version = check_output(["patchelf", "--version"], encoding="utf-8")
    except CalledProcessError:
        raise ValueError("Could not call `patchelf` binary") from None

    mobj = re.match(r"patchelf\s+(\d+(.\d+)?)", version)
    if mobj and tuple(int(x) for x in mobj.group(1).split(".")) >= (0, 9):
        return
    raise ValueError(
        f"patchelf {version} found. cx-freeze requires patchelf >= 0.9."
    )
