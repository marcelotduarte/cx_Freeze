"""Fixtures."""

from __future__ import annotations

import os
import string
import sys
from pathlib import Path
from shutil import copytree, ignore_patterns, which
from subprocess import check_output
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from collections.abc import Sequence

HERE = Path(__file__).resolve().parent
SAMPLES_DIR = HERE.parent / "samples"


class TempPackage:
    """Base class to create package in temporary path."""

    def __init__(self, path: Path) -> None:
        self.path: Path = path
        self.monkeypatch = pytest.MonkeyPatch()

    def __del__(self) -> None:
        self.monkeypatch.undo()

    def create(self, source: str) -> None:
        """Create package in temporary path, based on source."""
        buf = []
        filename: Path | None = None
        for line in [*source.splitlines(), "EOF"]:
            if not line.startswith(tuple(string.ascii_letters)):
                buf.append(line)
            else:
                if filename:
                    buf.append("")
                    filename.parent.mkdir(parents=True, exist_ok=True)
                    filename.write_bytes(
                        dedent("\n".join(buf)).encode("utf_8")
                    )
                    buf = []
                filename = self.path / line.strip()
        self.monkeypatch.chdir(self.path)

    def create_from_sample(self, sample: str) -> None:
        """Create package in path, based on sample."""
        self.path = self.path / sample
        copytree(
            SAMPLES_DIR / sample,
            self.path,
            symlinks=True,
            ignore=ignore_patterns("build", "dist"),
            dirs_exist_ok=True,
        )
        self.monkeypatch.chdir(self.path)

    def executable(self, base_name: str) -> Path:
        return self.path / BUILD_EXE_DIR / f"{base_name}{EXE_SUFFIX}"

    def executable_in_dist(self, base_name: str) -> Path:
        return self.path / "dist" / f"{base_name}{EXE_SUFFIX}"

    def run(self, command: Sequence | Path | None = None, timeout=None) -> str:
        """Execute a command, specified in 'command', or read the command
        contained in the file named 'command', or execute the default
        command.
        """
        if command is None:
            command_file = self.path / "command"
            if command_file.exists():
                command = command_file.read_bytes().decode()
            elif self.path.joinpath("pyproject.toml").exists():
                command = "cxfreeze build"
            else:
                command = "python setup.py build"
        elif isinstance(command, Path):
            command = [os.fspath(command)]

        command = (
            command.split() if isinstance(command, str) else list(command)
        )
        if command[0] == "cxfreeze":
            cxfreeze = which("cxfreeze")
            if not cxfreeze:
                cxfreeze = which("cxfreeze", path=os.pathsep.join(sys.path))
            if cxfreeze:
                command[0] = cxfreeze
            else:
                command = ["python", "-m", "cx_Freeze"] + command[1:]
        if command[0] == "python":
            command[0] = sys.executable
        return check_output(
            command, text=True, timeout=timeout, cwd=os.fspath(self.path)
        )


@pytest.fixture
def tmp_package(tmp_path: Path) -> TempPackage:
    """Create package in temporary path, based on source (or sample)."""
    return TempPackage(tmp_path)
