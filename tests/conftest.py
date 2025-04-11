"""Fixtures."""

from __future__ import annotations

import os
import re
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

    def __init__(
        self,
        request: pytest.FixtureRequest,
        tmp_path_factory: pytest.TempPathFactory,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self.request = request
        self.tmp_path_factory = tmp_path_factory
        self.monkeypatch = monkeypatch

        # make a temporary directory and set it as current
        name = request.node.name
        name = re.sub(r"[\W]", "_", name)
        MAXVAL = 30
        name = name[:MAXVAL]
        self.path = tmp_path_factory.mktemp(name, numbered=True)
        monkeypatch.chdir(self.path)

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

    def create_from_sample(self, sample: str) -> None:
        """Create package in path, based on sample."""
        copytree(
            SAMPLES_DIR / sample,
            self.path,
            symlinks=True,
            ignore=ignore_patterns("build", "dist"),
            dirs_exist_ok=True,
        )

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

    def install(self, package) -> None:
        if which("uv") is None:
            pytest.skip(reason=f"{package} must be installed")

        tmp_prefix = self.path / ".tmp_prefix"  # type: Path
        self.run(
            f"uv pip install {package}"
            f" --prefix={tmp_prefix} --python={sys.executable}"
        )
        tmp_site = tmp_prefix.joinpath(
            Path(pytest.__file__).parent.parent.relative_to(sys.prefix)
        )
        self.monkeypatch.setenv("PYTHONPATH", os.path.normpath(tmp_site))


@pytest.fixture
def tmp_package(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> TempPackage:
    """Create package in temporary path, based on source (or sample)."""
    return TempPackage(request, tmp_path_factory, monkeypatch)
