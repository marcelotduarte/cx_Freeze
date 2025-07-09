"""Fixtures."""

from __future__ import annotations

import json
import os
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

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

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
        if hasattr(request, "function"):
            name: str = request.function.__name__
        else:
            name = request.node.name
        self._name = name
        self.path: Path = tmp_path_factory.mktemp(name, numbered=True)
        os.chdir(self.path)

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

    def freeze(
        self,
        command: Sequence | Path | None = None,
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> pytest.RunResult:
        """Execute the command to freeze the current test sample, which can be
        specified in 'command', or read the command contained in the file named
        'command', or detect the default command to use.
        """
        __tracebackhide__ = True
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
                command = ["python", "-m", "cx_Freeze", *command[1:]]
        if command[0] == "python":
            command[0] = self.sys_executable
        return self.run(command, cwd=cwd, env=env, timeout=timeout)

    def run(
        self,
        command: Sequence | Path,
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> pytest.RunResult:
        """Execute a command, specified in 'command'."""
        __tracebackhide__ = True
        if isinstance(command, Path):
            command = [os.fspath(command)]
        command = (
            command.split() if isinstance(command, str) else list(command)
        )
        cwd = os.fspath(self.path if cwd is None else cwd)
        output = check_output(
            command, cwd=cwd, env=env, text=True, timeout=timeout
        )
        return pytest.RunResult(0, output.splitlines(), [], 0)

    def install(
        self,
        packages: str | list[str],
        *,
        binary: bool = True,
        index: bool | str | None = None,
        isolated=True,
    ) -> str:
        if isinstance(packages, str):
            packages = [packages]
        names = []
        names_and_specs = []
        for package in packages:
            require = Requirement(package)
            if require.marker is not None and not require.marker.evaluate():
                continue
            names.append(require.name)
            names_and_specs.append(f"{require.name}{require.specifier!s}")
        if not names:
            return None
        if IS_CONDA:
            return self._install_conda(names)
        if IS_MINGW:
            return self._install_mingw(names)
        if HAVE_UV:
            return self._install_uv(names_and_specs, binary, index, isolated)
        request = self.request
        pytest.skip(
            f"{request.config.args[0]}::{request.node.name} - {names} "
            "must be installed"
        )

    def install_dependencies(self, pyproject: Path | None = None) -> None:
        """Install dependencies for the test, as specified in the
        pyproject.toml.
        """
        if pyproject is None:
            pyproject = self.path / "pyproject.toml"
        if pyproject.is_file():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            dependencies = data.get("project", {}).get("dependencies", [])
            self.install(dependencies)

    def _install_conda(self, packages: list[str]) -> pytest.RunResult:
        CONDA_EXE = os.environ["CONDA_EXE"]
        packages = " ".join(packages)
        cmd = (
            f"{CONDA_EXE} install -c conda-forge -S -q -y -p {self.prefix} "
            f"{packages}"
        )
        with FileLock(self.prefix / ".lock"):
            try:
                output = self.run(cmd, cwd=self.system_path)
            except CalledProcessError:
                raise ModuleNotFoundError(packages) from None
        return output

    def _install_mingw(self, packages: list[str]) -> pytest.RunResult:
        MINGW_PACKAGE_PREFIX = os.environ["MINGW_PACKAGE_PREFIX"]
        for i, package in enumerate(packages):
            packages[i] = f"{MINGW_PACKAGE_PREFIX}-python-{package}"
        packages = " ".join(packages)
        cmd = f"pacman -S --needed --noconfirm --quiet {packages}"
        with FileLock("/var/lib/pacman/db.lck"):
            try:
                output = self.run(cmd, cwd=self.system_path)
            except CalledProcessError:
                raise ModuleNotFoundError(packages) from None
        return output

    def _install_uv(
        self,
        packages: list[str],
        binary: bool = True,
        index: bool | str | Path | None = None,
        isolated: bool = False,
    ) -> pytest.RunResult:
        packages = " ".join(packages)
        cmd = f"uv pip install --python={self.sys_executable} {packages}"
        if binary:
            cmd = f"{cmd} --no-build"
        if index is False:
            cmd = f"{cmd} --no-index"
        elif isinstance(index, str):
            cmd = f"{cmd} --index {index}"
        elif isinstance(index, Path):
            cmd = f"{cmd} -f {index} --no-index"
        if isolated:
            cmd = f"{cmd} --prefix={self.path / '.tmp_prefix'}"
        else:
            cmd = f"{cmd} --prefix={self.prefix}"
        try:
            output = self.run(cmd, cwd=self.system_path)
        except CalledProcessError:
            raise ModuleNotFoundError(packages) from None
        if isolated:
            tmp_site = os.path.normpath(
                self.path / ".tmp_prefix" / self.relative_site
            )
            self.monkeypatch.setenv("PYTHONPATH", tmp_site)
            self.monkeypatch.syspath_prepend(tmp_site)
        return output

    def cleanup(self) -> None:
        # remove the temporary prefix to reduce disk usage
        tmp_prefix = self.path / ".tmp_prefix"
        if tmp_prefix.is_dir():
            rmtree(tmp_prefix, ignore_errors=True)
        os.chdir(self.system_path)


class TempPackageVenv(TempPackage):
    """Base class to create package in temporary path using venv."""

    def __init__(
        self,
        request: pytest.FixtureRequest,
        tmp_path_factory: pytest.TempPathFactory,
        monkeypatch: pytest.MonkeyPatch | None = None,
    ) -> None:
        if monkeypatch is None:
            monkeypatch = pytest.MonkeyPatch()
        super().__init__(request, tmp_path_factory, monkeypatch)
        # make prefix
        # using loadfile, the prefix is on top of the pytest tmp_path and
        # is shared by test functions on the same module
        dist = os.environ["PYTEST_XDIST_DIST"]
        if dist in ("no", "loadfile"):
            root_tmp_dir = self.path.parent.parent
            if dist == "loadfile":
                root_tmp_dir = root_tmp_dir.parent
        else:  # probably dist = "load"
            root_tmp_dir = self.path
        self._dist = dist
        self._lock = None
        if IS_MINGW:
            return
        vname = request.module.__name__.replace(".", "_")
        if IS_CONDA:
            self.prefix = root_tmp_dir / f".conda_{vname}"
        elif HAVE_UV:
            self.prefix = root_tmp_dir / f".venv_{vname}"
        self._lock = FileLock(f"{self.prefix}.lock")
        self._lock.acquire()
        # create venv
        if IS_CONDA:
            self._venv_conda()
        elif HAVE_UV:
            self._venv_uv()

    def create(self, source: str) -> None:
        if self._dist == "loadfile":
            self.path = self.tmp_path_factory.mktemp(self._name, numbered=True)
            os.chdir(self.path)
        super().create(source)
        self.install_dependencies()

    def create_from_sample(self, sample: str) -> None:
        if self._dist == "loadfile":
            self.path = self.tmp_path_factory.mktemp(self._name, numbered=True)
            os.chdir(self.path)
        super().create_from_sample(sample)
        self.install_dependencies()

    def _install_uv(
        self,
        packages: list[str],
        binary: bool = True,
        index: bool | str | Path | None = None,
        isolated: bool = False,  # noqa:ARG002
    ) -> pytest.RunResult:
        return super()._install_uv(packages, binary, index, isolated=False)

    def _venv_conda(self) -> None:
        CONDA_EXE = os.environ["CONDA_EXE"]
        CONDA_ENV = os.environ["CONDA_DEFAULT_ENV"]
        # create a clone venv
        self.run(
            f"{CONDA_EXE} create --clone {CONDA_ENV} -p {self.prefix} -q -y",
            cwd=self.system_path,
        )
        # point to the new environment
        self.sys_executable = (
            self.prefix / self.relative_bin / self.sys_executable.name
        )

    def _venv_uv(self) -> None:
        # get the list of packages
        result = self.run("uv pip list --format=json -q", cwd=self.system_path)
        packages = json.loads(result.outlines[0])
        # create venv
        cmd = f"uv venv --python={PYTHON_VERSION}{ABI_THREAD} {self.prefix}"
        self.run(cmd, cwd=self.system_path)
        # point to the new environment
        self.sys_executable = (
            self.prefix / self.relative_bin / self.sys_executable.name
        )
        # install cx_Freeze and dependencies in the new environment
        # using cx_Freeze pyproject.toml
        pyproject = self.system_path / "pyproject.toml"
        if pyproject.is_file():
            self.install_dependencies(pyproject)
            # install cx-freeze, editable or from wheelhouse
            for pkg in packages:
                if pkg["name"] != "cx-freeze":
                    continue
                project_location = pkg.get("editable_project_location")
                if project_location:
                    self._install_uv(["-e", project_location])
                else:
                    wheelhouse = self.system_path / "wheelhouse"
                    pkg_spec = f"cx-freeze=={pkg['version']}"
                    self._install_uv([pkg_spec], index=wheelhouse)

    def cleanup(self) -> None:
        # remove the venv to reduce disk usage
        if IS_CONDA:
            CONDA_EXE = os.environ["CONDA_EXE"]
            # remove conda env
            self.run(
                f"{CONDA_EXE} remove --all -p {self.prefix} -q -y",
                cwd=self.system_path,
            )
        elif self.prefix.is_relative_to(self.path):
            rmtree(self.prefix, ignore_errors=True)
        if self._lock:
            self._lock.release()
        os.chdir(self.system_path)


@pytest.fixture
def _tmp_package(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> TempPackage:
    """Create package in temporary path, based on source (or sample)."""
    tmp_pkg = TempPackage(request, tmp_path_factory, monkeypatch)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture
def _tmp_package_venv(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> TempPackage:
    """Create package in temporary path, based on source (or sample)
    using a virtual environment.
    """
    tmp_pkg = TempPackageVenv(request, tmp_path_factory, monkeypatch)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture(scope="module")
def _tmp_package_venv_module(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> TempPackage:
    """Create package in temporary path, based on source (or sample)
    using a virtual environment per module (for use with --dist=loadfile).
    """
    tmp_pkg = TempPackageVenv(request, tmp_path_factory)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture
def tmp_package(request: pytest.FixtureRequest) -> TempPackage:
    """Create package in temporary path, based on source (or sample)."""
    # activate venv if has a venv mark
    is_venv = len(list(request.node.iter_markers(name="venv"))) > 0
    dist = os.environ["PYTEST_XDIST_DIST"]
    # fixture dispatch
    if is_venv and dist in ("no", "loadfile"):
        yield request.getfixturevalue("_tmp_package_venv_module")
    elif is_venv:
        yield request.getfixturevalue("_tmp_package_venv")
    else:
        yield request.getfixturevalue("_tmp_package")


def pytest_configure(config: pytest.Config) -> None:
    """Register an additional marker."""
    config.addinivalue_line(
        "markers", "venv: mark test to run in a virtual environment"
    )
    # pytest-xdist uses subprocess
    # so a environment variable can be use to pass data
    os.environ["PYTEST_XDIST_DIST"] = getattr(config.option, "dist", "no")
