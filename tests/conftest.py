"""Fixtures."""

from __future__ import annotations

import argparse
import errno
import io
import json
import os
import re
import string
import subprocess
import sys
import sysconfig
from contextlib import redirect_stdout, suppress
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree, which
from textwrap import dedent
from typing import TYPE_CHECKING, Any, TypeAlias

import pytest
from filelock import BaseFileLock, FileLock
from packaging.requirements import InvalidRequirement, Requirement

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    from setuptools.compat.py310 import tomllib

if TYPE_CHECKING:
    from collections.abc import Sequence
    from os import PathLike
    from types import GeneratorType

    StrPath: TypeAlias = str | PathLike[str]

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


class FakeLock(BaseFileLock):
    """Fake lock."""

    def _acquire(self) -> None:
        pass

    def _release(self) -> None:
        pass

    @property
    def is_locked(self) -> bool:
        return True


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

        monkeypatch.setenv("PYTHONUNBUFFERED", "1")

        # environment
        sysexe = Path(sys.executable)
        prefix = Path(sys.prefix)
        self.prefix: Path = prefix
        self.python: Path = sysexe
        self.system_path: Path = Path(os.getcwd())
        self.system_prefix: Path = prefix
        self.relative_bin: str = sysexe.parent.relative_to(prefix).as_posix()
        self.relative_site: str = (
            Path(pytest.__file__).parent.parent.relative_to(prefix).as_posix()
        )

        # make a temporary directory and set it as current
        if hasattr(request, "function"):
            name: str = request.function.__name__
        else:
            name = request.node.name.replace(".py", "")
        self._name = name
        self.path: Path = tmp_path_factory.mktemp(name, numbered=True)
        os.chdir(self.path)

        # lock files
        self.backend = request.config.option.venv_backend
        if self.backend == "mingw":
            self._lock = FileLock("/var/lib/pacman/db.lck")
        elif self.backend == "pip":
            self._lock = FileLock(self.prefix / ".lock")
        else:
            # conda and uv have internal lock
            self._lock = FakeLock(self.prefix / ".lock")
        self._isolated = False

        # packages mapping
        self.map_package_to_conda: dict[str, str] = {
            "cx-logging": "cx_logging",
            "lief": "py-lief",
        }
        self.map_package_to_mingw: dict[str, str] = {}

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
        command: Sequence[str] | Path | None = None,
        cwd: StrPath | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> pytest.RunResult:
        """Execute the command to freeze the current test sample.

        The command can be specified in 'command' argument, or read from the
        file named 'command', or a default command is used.
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
            command = os.fspath(command)
        command = (
            command.split() if isinstance(command, str) else list(command)
        )

        python_path = env and env.get("PYTHONPATH")  # pop
        if python_path:
            if "build_exe" not in command and "build" in command:
                command.append("build_exe")
            try:
                build_exe = command.index("build_exe")
            except ValueError:
                build_exe = len(command)
            if build_exe > 0:
                command.insert(build_exe + 1, f"--include-path={python_path}")

        with self._lock:
            return self.run(command, cwd=cwd, env=env, timeout=timeout)

    def run(
        self,
        command: Sequence | Path,
        cwd: StrPath | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
        *,
        raise_on_timeout: bool = True,
    ) -> pytest.RunResult:
        """Execute a command, specified in 'command'."""
        __tracebackhide__ = True
        if isinstance(command, Path):
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

        if command[0] == "conda":
            command[0] = os.environ["CONDA_EXE"]

        if command[0] == "pip":
            pip = which("pip", path=self.prefix / self.relative_bin)
            if pip:
                command[0] = pip
            else:
                command = ["python", "-m", "pip", *command[1:]]

        if command[0] == "python":
            command[0] = os.fspath(self.python)
        cwd = os.fspath(self.path if cwd is None else cwd)
        try:
            process = subprocess.run(
                command,
                capture_output=True,
                check=False,
                cwd=cwd,
                env=env,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            if raise_on_timeout:
                raise
            returncode = errno.ETIMEDOUT
            stdout = exc.output or ""
            stderr = exc.stderr or ""
        else:
            returncode = process.returncode
            stdout = process.stdout or ""
            stderr = process.stderr or ""
        stdout = stdout.decode() if isinstance(stdout, bytes) else str(stdout)
        if isinstance(stderr, bytes):
            stderr = stderr.decode()
        print(stdout)
        print(stderr, file=sys.stderr)
        return pytest.RunResult(
            returncode, stdout.splitlines(), stderr.splitlines(), 0
        )

    def install(
        self,
        packages: str | list[str],
        *,
        backend: str | None = None,
        binary: bool = True,
        index: bool | StrPath | None = None,
        isolated: bool = True,
    ) -> pytest.RunResult | None:
        """Install required packages for the test."""
        if isinstance(packages, str):
            packages = [packages]
        if not packages:
            return None

        # check backend values
        if backend is None:
            backend = self.backend
        if backend in ("uv", "pip") and backend != self.backend:
            # use a different backend only in conda and mingw
            if self.backend in ("uv", "pip"):
                backend = self.backend
            else:
                # ensure that extra backend (pip or uv) is installed
                self.install(backend)

        with self._lock:
            # for pip or uv, accept -e, -r # TODO: improve -r
            if backend in ("uv", "pip") and packages[0].startswith("-"):
                names_and_specs = packages
            else:
                names = []
                names_and_specs = []
                for package in packages:
                    req = Requirement(package)
                    if req.marker is not None and not req.marker.evaluate():
                        continue
                    names.append(req.name)
                    names_and_specs.append(f"{req.name}{req.specifier!s}")
                if not names:
                    return None
                if backend == "conda":
                    return self._install_conda(names)
                if backend == "mingw":
                    return self._install_mingw(names)
            return self._install_pip(
                names_and_specs,
                backend=backend,
                binary=binary,
                index=index,
                isolated=isolated,
            )

    def install_dependencies(self, pyproject: Path | None = None) -> None:
        """Install dependencies for the test.

        The default is to read from pyproject.toml.
        """
        project_data = self._get_project(pyproject)
        self.install(project_data["dependencies"])

    def _get_project(self, pyproject: Path | None = None) -> dict[str, Any]:
        """Get project metadata (specified in the pyproject.toml)."""
        if pyproject is None:
            pyproject = self.path / "pyproject.toml"
        if pyproject.is_file():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
        else:
            data = {}
        data.setdefault("project", {})
        data["project"].setdefault("name", "undefined")
        data["project"].setdefault("dependencies", [])
        return data["project"]

    def _get_installed_packages(
        self, python: StrPath | None = None
    ) -> list[dict[str, str]]:
        """Get installed packages."""
        if python is None:
            python = self.python
        if self.backend == "uv":
            cmd = f"uv pip list --format=json --python={python} -q"
        else:
            cmd = f"{python} -m pip list --format=json"
        result = self.run(cmd, cwd=self.system_path)
        installed = json.loads(str(result.stdout))
        for i, package in enumerate(installed):
            name = normalize(package["name"])
            version = package["version"]
            if name != package["name"]:
                installed[i]["original_name"] = package["name"]
                installed[i]["name"] = name
            installed[i]["spec"] = f"{name}=={version}"
        return installed

    def _install_conda(self, packages: list[str]) -> pytest.RunResult:
        for i, package in enumerate(packages):
            with suppress(KeyError):
                packages[i] = self.map_package_to_conda[package]
        packages: str = " ".join(packages)
        cmd = f"conda install -S -q -y -p {self.prefix}"
        if not any(
            opc for opc in ("-c", "--channel", "::") if opc in packages
        ):
            cmd = f"{cmd} -c conda-forge"
        cmd = f"{cmd} {packages}"
        result = self.run(cmd, cwd=self.system_path)
        if result.ret > 0:
            raise ModuleNotFoundError(packages) from None
        return result

    def _install_mingw(self, packages: list[str]) -> pytest.RunResult:
        MINGW_PACKAGE_PREFIX = os.environ["MINGW_PACKAGE_PREFIX"]
        for i, pkg in enumerate(packages):
            try:
                package = self.map_package_to_mingw[pkg]
            except KeyError:
                package = f"python-{pkg}"
            packages[i] = f"{MINGW_PACKAGE_PREFIX}-{package}"
        packages: str = " ".join(packages)
        cmd = f"pacman -S --needed --noconfirm --quiet {packages}"
        result = self.run(cmd, cwd=self.system_path)
        if result.ret > 0:
            raise ModuleNotFoundError(packages) from None
        return result

    def _install_pip(
        self,
        packages: list[str],
        *,
        backend: str | None = None,
        binary: bool = True,
        index: bool | StrPath | None = None,
        isolated: bool = False,
    ) -> pytest.RunResult:
        # "uv pip install --prefix" install the package in the new prefix as a
        # fake venv, even if the package already exists in the real venv.
        # With "pip" if the package exists, it will be uninstalled and then
        # installed on the fake venv. To get around this situation, save a list
        # of packages that should be restored after the installation process.
        saved = []
        if isolated and backend == "pip":
            names = []
            for package in packages:
                try:
                    req = Requirement(package)
                except InvalidRequirement:
                    break
                names.append(normalize(req.name))
            if names:
                installed = self._get_installed_packages()
                saved.extend(
                    [pkg["spec"] for pkg in installed if pkg["name"] in names]
                )
        packages: str = " ".join(packages)
        if backend is None:
            backend = self.backend
        if backend == "uv":
            cmd = f"uv pip install --python={self.python} {packages}"
            if binary:
                cmd = f"{cmd} --no-build"
        else:
            cmd = f"pip install {packages}"
            if binary:
                cmd = f"{cmd} --prefer-binary"
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

        result = self.run(cmd, cwd=self.system_path)
        if result.ret > 0:
            raise ModuleNotFoundError(packages) from None

        if saved:
            self._install_pip(saved, isolated=False)

        if isolated and not self._isolated:
            tmp_site = os.path.normpath(
                self.path / ".tmp_prefix" / self.relative_site
            )
            self.monkeypatch.setenv("PYTHONPATH", tmp_site)
            self.monkeypatch.syspath_prepend(tmp_site)
            self._isolated = isolated
        return result

    def cleanup(self) -> None:
        os.chdir(self.system_path)

        # remove build directory (to reduce disk usage)
        if not self.request.config.option.venv_keep_build:
            build_dir: Path = self.path / "build"
            rmtree(build_dir, ignore_errors=True)

        # remove temporary prefix (to reduce disk usage)
        if not self.request.config.option.venv_keep_prefix:
            tmp_prefix = self.path / ".tmp_prefix"
            rmtree(tmp_prefix, ignore_errors=True)


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

        # determine the root of pytest tmp_path
        self._root: Path = tmp_path_factory.getbasetemp().parent
        self._worker: str = os.environ.get("PYTEST_XDIST_WORKER", "master")
        if self._worker != "master":
            # using xdist, the root is one level up
            self._root = self._root.parent

        # activate the venv
        self._prefix = self.prefix
        self._python = self.python
        self.venv_prefix = None
        self.venv_python = None
        self.venv_lock = None
        self._venv()

    def create(self, source: str) -> None:
        super().create(source)
        self.install_system_dependencies()
        # install dependencies
        venv_marker = self.request.node.get_closest_marker(name="venv")
        install_deps = venv_marker.kwargs.get("install_dependencies", True)
        if install_deps:
            self.install_dependencies()
        if self.venv_lock and self.venv_lock.is_locked:
            self.venv_lock.release()

    def create_from_sample(self, sample: str) -> None:
        super().create_from_sample(sample)
        self.install_system_dependencies()
        # install dependencies
        venv_marker = self.request.node.get_closest_marker(name="venv")
        install_deps = venv_marker.kwargs.get("install_dependencies", True)
        if install_deps:
            self.install_dependencies()
        if self.venv_lock and self.venv_lock.is_locked:
            self.venv_lock.release()

    def freeze(
        self,
        command: Sequence[str] | Path | None = None,
        cwd: StrPath | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> pytest.RunResult:
        if IS_CONDA or self.backend in ("uv", "pip"):
            if self.venv_prefix:
                self.prefix = self.venv_prefix
            if self.venv_python:
                self.python = self.venv_python
            try:
                return super().freeze(command, cwd, env, timeout)
            finally:
                self.prefix = self._prefix
                self.python = self._python
        # PYTHONPATH is the key here
        if env is None:
            env = os.environ.copy()
        prefix = self.venv_prefix or self.prefix
        venv_site = os.path.normpath(prefix / self.relative_site)
        env["PYTHONPATH"] = venv_site
        return super().freeze(command, cwd, env, timeout)

    def install(
        self,
        packages: str | list[str],
        *,
        backend: str | None = None,
        binary: bool = True,
        index: bool | StrPath | None = None,
        isolated: bool = False,  # noqa: ARG002
    ) -> pytest.RunResult | None:
        # install in the venv prefix
        if self.venv_prefix:
            self.prefix = self.venv_prefix
        if self.venv_python:
            self.python = self.venv_python
        try:
            return super().install(
                packages,
                backend=backend,
                binary=binary,
                index=index,
                isolated=False,
            )
        finally:
            self.prefix = self._prefix
            self.python = self._python

    def install_system_dependencies(self) -> None:
        """Install system dependencies for the project.

        The default is to read from pyproject.toml.
        """
        if self.backend not in ("uv", "pip"):
            return
        pyproject = self.system_path / "pyproject.toml"
        project_data = self._get_project(pyproject)
        name = normalize(project_data["name"])
        dependencies = project_data["dependencies"]
        valid = [name]
        for package in dependencies:
            try:
                req = Requirement(package)
            except InvalidRequirement:
                continue
            if req.marker is not None and not req.marker.evaluate():
                continue
            valid.append(normalize(req.name))

        # get installed packages in the host environment
        # compare them with the declared dependencies in pyproject.toml
        # check for editable packages in development environment
        # use the wheels in wheelhouse
        packages = []
        editables = []
        name_in_editables = False
        for pkg in self._get_installed_packages():
            if pkg["name"] in valid:
                try:
                    editables.append(pkg["editable_project_location"])
                    if pkg["name"] == name:
                        name_in_editables = True
                except KeyError:
                    if pkg["name"] != name:
                        packages.append(pkg["spec"])
        print(packages)
        self.install(packages)
        for package in editables:
            self.install(f"-e{package}")
        if not name_in_editables:
            self.install(
                f"--no-deps --prerelease=allow {name}",
                index=self.system_path / "wheelhouse",
            )
        print(editables)

    def _venv(self) -> None:
        venv_marker = self.request.node.get_closest_marker(name="venv")
        scope = venv_marker.kwargs.get("scope", "function")

        # activate the venv
        if self.backend == "mingw":
            # do not use venv in mingw
            self.venv_prefix = self._prefix
            self.venv_python = self._python
            self.venv_lock = self._lock
        else:
            # point to the new environment (or reuse an existing one)
            if scope == "function":
                prefix = self.path / ".venv"
            else:
                prefix = self._root / f".{self.backend}-{self._name}"
                prefix_lock = prefix.with_name(f"{prefix.name}.lock")
                self.venv_lock = FileLock(prefix_lock)
                self.venv_lock.acquire()
            self.venv_prefix = prefix
            self.venv_python = prefix / self.relative_bin / self.python.name

            # if python file does not exists, create the new venv
            if not self.venv_python.is_file():
                if self.backend == "conda":
                    self._venv_conda_clone()
                else:
                    self._venv_pip()
            # reuse the venv - point to the existing lock file
            elif self.backend == "pip":
                self._lock = FileLock(self.venv_prefix / ".lock")

    def _venv_conda_clone(self) -> None:
        # create a clone venv
        conda_env = os.environ["CONDA_DEFAULT_ENV"]
        cmd = f"conda create --clone {conda_env} -p {self.venv_prefix} -q -y"
        self.run(cmd, cwd=self.system_path)

    def _venv_pip(self) -> None:
        # create venv
        prefix = self.venv_prefix
        if self.backend == "uv":
            python = f"{PYTHON_VERSION}{ABI_THREAD}"
            cmd = f"uv venv --clear --python={python} {prefix}"
        else:
            cmd = f"{self.python} -m venv --clear --upgrade-deps {prefix}"
        self.run(cmd, cwd=self.system_path)

    def cleanup(self) -> None:
        super().cleanup()

        # release lock
        if self.venv_lock and self.venv_lock.is_locked:
            self.venv_lock.release()

        # remove venv prefix (to reduce disk usage)
        if not self.request.config.option.venv_keep_prefix:
            prefix = self.venv_prefix
            if self.backend == "conda":

                def _conda_cleanup() -> None:
                    cmd = f"conda remove --all -p {prefix} -q -y --offline"
                    with io.StringIO() as f, redirect_stdout(f):
                        self.run(cmd, cwd=self.system_path)

                self.request.config.add_cleanup(_conda_cleanup)
            elif self.backend == "mingw":
                # venv is not used in mingw
                pass
            elif isinstance(prefix, Path) and prefix.is_dir():
                rmtree(prefix, ignore_errors=True)


def normalize(name: str) -> str:
    """Normalize a package name."""
    return re.sub(r"[-_.]+", "-", name).lower()


@pytest.fixture
def _tmp_package(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> GeneratorType[TempPackage]:
    """Create package in temporary path, based on source (or sample)."""
    tmp_pkg = TempPackage(request, tmp_path_factory, monkeypatch)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture
def _tmp_package_venv(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> GeneratorType[TempPackage]:
    """Create package in temporary path, based on source (or sample).

    Using a virtual environment.
    """
    tmp_pkg = TempPackageVenv(request, tmp_path_factory, monkeypatch)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture
def tmp_package(request: pytest.FixtureRequest) -> GeneratorType[TempPackage]:
    """Create package in temporary path, based on source (or sample)."""
    # activate venv if has a venv mark using fixture dispatch
    venv_marker = request.node.get_closest_marker(name="venv")
    if venv_marker:
        if not isinstance(venv_marker.kwargs, dict):
            msg = "venv marker kwargs must be a dictionary"
            raise ValueError(msg)
        scope = venv_marker.kwargs.get("scope", "function")
        if scope not in {"function", "module"}:
            msg = "venv marker scope must be 'function' or 'module'"
            raise ValueError(msg)
        install_deps = venv_marker.kwargs.get("install_dependencies", True)
        if not isinstance(install_deps, bool):
            msg = "venv marker install_dependencies must be a boolean"
            raise ValueError(msg)

        yield request.getfixturevalue("_tmp_package_venv")
    else:
        yield request.getfixturevalue("_tmp_package")


def pytest_configure(config: pytest.Config) -> None:
    """Register an additional marker."""
    config.addinivalue_line(
        "markers",
        """venv(scope="function"):
        Mark test to run in a virtual environment.

        Args:
            scope: function [default] or module
        """,
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add options to control venv backend."""
    group = parser.getgroup("venv", "venv backend")
    group.addoption(
        "--venv-backend",
        action="store",
        metavar="BACKEND",
        type=_validate_backend,
        help="Venv backend to use. Default to current venv.",
    )
    group.addoption(
        "--venv-keep-build",
        action="store_true",
        help="Keep build directory of the test.",
    )
    group.addoption(
        "--venv-keep-prefix",
        action="store_true",
        help="Keep venv directory (aka prefix).",
    )


def _validate_backend(arg: str) -> str:
    valid = {"conda", "mingw", "pip", "uv", "venv"}
    if arg not in valid:
        msg = f"The supported value are: {', '.join(valid)}."
        raise argparse.ArgumentTypeError(msg)
    # TODO: check if arg is really valid, if the backend is installed
    return arg


@pytest.hookimpl(tryfirst=True)
def pytest_cmdline_main(config: pytest.Config) -> None:
    """Set default values to options to control venv backend."""
    if config.option.venv_backend is None:
        if IS_CONDA:
            config.option.venv_backend = "conda"
        elif IS_MINGW:
            config.option.venv_backend = "mingw"
        else:
            virtual_env = os.environ.get("VIRTUAL_ENV")
            if virtual_env is not None:
                pyvenv = Path(virtual_env, "pyvenv.cfg")
                if pyvenv.is_file():
                    if b"uv =" in pyvenv.read_bytes():
                        config.option.venv_backend = "uv"
                    else:
                        config.option.venv_backend = "pip"
            # if not set yet
            if config.option.venv_backend is None:
                if HAVE_UV:
                    config.option.venv_backend = "uv"
                else:
                    config.option.venv_backend = "pip"
    elif config.option.venv_backend == "venv":
        config.option.venv_backend = "pip"
