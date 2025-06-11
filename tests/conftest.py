"""Fixtures."""

from __future__ import annotations

import json
import os
import re
import string
import sys
import sysconfig
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree, which
from subprocess import CalledProcessError, check_output
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from filelock import FileLock
from packaging.requirements import Requirement

if TYPE_CHECKING:
    from collections.abc import Sequence

# copied from cx_Freeze._compat
PLATFORM = sysconfig.get_platform()
PYTHON_VERSION = sysconfig.get_python_version()
ABI_THREAD = sysconfig.get_config_var("abi_thread") or ""
BUILD_EXE_DIR = Path(f"build/exe.{PLATFORM}-{PYTHON_VERSION}{ABI_THREAD}")
EXE_SUFFIX = sysconfig.get_config_var("EXE")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()
IS_MINGW = PLATFORM.startswith("mingw")
HAVE_UV = which("uv") is not None

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

        # environment
        self.prefix: Path = Path(sys.prefix)
        self.prefix_is_venv: bool = False
        self.sys_executable: Path = Path(sys.executable)
        self.system_path: Path = Path(os.getcwd())
        self.system_prefix: Path = Path(sys.prefix)
        self.relative_bin: str = self.sys_executable.parent.relative_to(
            self.system_prefix
        ).as_posix()
        self.relative_site: str = (
            Path(pytest.__file__)
            .parent.parent.relative_to(self.system_prefix)
            .as_posix()
        )

        # make a temporary directory and set it as current
        name = request.node.name
        name = re.sub(r"[\W]", "_", name)
        MAXVAL = 30
        name = name[:MAXVAL]
        self.path: Path = tmp_path_factory.mktemp(name, numbered=True)
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

    def run(
        self,
        command: Sequence | Path | None = None,
        cwd: str | Path | None = None,
        timeout=None,
    ) -> str:
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
            cxfreeze = which("cxfreeze", path=self.prefix / self.relative_bin)
            if cxfreeze:
                command[0] = cxfreeze
            else:
                command = ["python", "-m", "cx_Freeze"] + command[1:]
        if command[0] == "python":
            command[0] = self.sys_executable
        cwd = os.fspath(self.path if cwd is None else cwd)
        return check_output(command, text=True, timeout=timeout, cwd=cwd)

    def install(
        self,
        package,
        *,
        binary: bool = True,
        index: bool | str | None = None,
        isolated=True,
    ) -> str:
        require = Requirement(package)
        if require.marker is not None and not require.marker.evaluate():
            return None
        pkg_name = require.name
        pkg_spec = str(require.specifier)
        if IS_CONDA:
            return self._install_conda(pkg_name)
        if IS_MINGW:
            return self._install_mingw(pkg_name)
        if HAVE_UV:
            return self._install_uv(
                pkg_name,
                pkg_spec,
                binary,
                index,
                isolated=isolated and not self.prefix_is_venv,
            )
        request = self.request
        pytest.skip(
            f"{request.config.args[0]}::{request.node.name} - {pkg_name} "
            "must be installed"
        )

    def _install_conda(self, pkg_name) -> str:
        CONDA_EXE = os.environ["CONDA_EXE"]
        cmd = f"{CONDA_EXE} install -c conda-forge {pkg_name} -S -q -y"
        with FileLock(self.system_path / "conda.lock"):
            try:
                output = self.run(cmd, cwd=self.system_path)
            except CalledProcessError:
                raise ModuleNotFoundError(pkg_name) from None
        return output

    def _install_mingw(self, pkg_name) -> str:
        MINGW_PACKAGE_PREFIX = os.environ["MINGW_PACKAGE_PREFIX"]
        cmd = (
            "pacman -S --needed --noconfirm --quiet "
            f"{MINGW_PACKAGE_PREFIX}-python-{pkg_name}"
        )
        with FileLock("/var/lib/pacman/db.lck"):
            try:
                output = self.run(cmd, cwd=self.system_path)
            except CalledProcessError:
                raise ModuleNotFoundError(pkg_name) from None
        return output

    def _install_uv(
        self,
        pkg_name: str,
        pkg_spec: str,
        binary: bool = True,
        index: bool | str | Path | None = None,
        isolated: bool = False,
    ) -> str:
        package = f"{pkg_name}{pkg_spec}"
        cmd = f"uv pip install {package}"
        if binary:
            cmd = f"{cmd} --no-build"
        if index is False:
            cmd = f"{cmd} --no-index"
        elif isinstance(index, str):
            cmd = f"{cmd} --index {index}"
        elif isinstance(index, Path):
            cmd = f"{cmd} -f {index} --no-index"
        if isolated:
            self.prefix = self.path / ".tmp_prefix"
        if self.prefix_is_venv or isolated:
            cmd += f" --prefix={self.prefix} --python={self.sys_executable}"
        try:
            output = self.run(cmd, cwd=self.system_path)
        except CalledProcessError:
            raise ModuleNotFoundError(pkg_name) from None
        if isolated:
            tmp_site = os.path.normpath(self.prefix / self.relative_site)
            self.monkeypatch.setenv("PYTHONPATH", tmp_site)
            self.monkeypatch.syspath_prepend(tmp_site)
        return output

    def venv(self) -> None:
        if IS_CONDA or IS_MINGW:
            return
        if HAVE_UV:
            self._venv_uv()

    def _venv_uv(self) -> None:
        # get the list of packages
        output = self.run("uv pip list --format=json -q")
        packages = json.loads(output)
        # create venv
        venv_prefix = self.path / ".venv"
        pyproject = self.system_path.joinpath("pyproject.toml")
        if pyproject.is_file():
            self.run(f"uv venv --python={PYTHON_VERSION}")
        else:
            # use a venv clone
            if sys.prefix != sys.base_prefix:
                copytree(
                    sys.prefix,  # self.system_prefix
                    venv_prefix,
                    symlinks=True,
                    ignore=ignore_patterns(".lock"),
                )
            self.run(f"uv venv --python={PYTHON_VERSION} --allow-existing")
        # point to the new environment
        self.sys_executable = (
            venv_prefix / self.relative_bin / self.sys_executable.name
        )
        self.prefix = venv_prefix
        self.prefix_is_venv = True
        # install the packages in the new environment
        if pyproject.is_file():
            self._install_uv("-r", pyproject)
            for pkg in packages:
                if pkg["name"] != "cx-freeze":
                    continue
                project_location = pkg.get("editable_project_location")
                if project_location:
                    self._install_uv("-e", project_location)
                else:
                    wheelhouse = self.system_path / "wheelhouse"
                    pkg_spec = f"=={pkg['version']}"
                    self._install_uv("cx-freeze", pkg_spec, index=wheelhouse)


@pytest.fixture
def tmp_package(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> TempPackage:
    """Create package in temporary path, based on source (or sample)."""
    tmp_package = TempPackage(request, tmp_path_factory, monkeypatch)
    # activate venv if has a venv mark
    for _marker in request.node.iter_markers(name="venv"):
        tmp_package.venv()
    yield tmp_package
    # remove the venv or temporary prefix to reduce disk usage
    try:
        tmp_package.prefix.relative_to(tmp_package.path)
    except ValueError:
        pass
    else:
        rmtree(tmp_package.prefix, ignore_errors=True)


def pytest_configure(config: pytest.Config) -> None:
    """Register an additional marker."""
    config.addinivalue_line(
        "markers", "venv: mark test to run in a virtual environment"
    )
