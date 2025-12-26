"""Fixtures."""

from __future__ import annotations

import argparse
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
from typing import TYPE_CHECKING

import pytest
from filelock import BaseFileLock, FileLock
from packaging.requirements import InvalidRequirement, Requirement

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
        command: Sequence | None = None,
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
            command[0] = self.python
        cwd = os.fspath(self.path if cwd is None else cwd)
        process = subprocess.run(
            command,
            capture_output=True,
            check=False,
            cwd=cwd,
            env=env,
            text=True,
            timeout=timeout,
        )
        print(process.stdout)
        print(process.stderr)
        return pytest.RunResult(
            process.returncode,
            process.stdout.splitlines(),
            process.stderr.splitlines(),
            0,
        )

    def install(
        self,
        packages: str | list[str],
        *,
        backend: str | None = None,
        binary: bool = True,
        index: bool | str | None = None,
        isolated: bool = True,
    ) -> pytest.RunResult:
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
        """Install dependencies for the test, as specified in the
        pyproject.toml.
        """
        self.install(self._get_dependencies(pyproject))

    def _get_dependencies(self, pyproject: Path | None = None) -> list[str]:
        """Get dependencies for the test (specified in the pyproject.toml)."""
        if pyproject is None:
            pyproject = self.path / "pyproject.toml"
        if pyproject.is_file():
            with pyproject.open("rb") as f:
                data = tomllib.load(f)
            return data.get("project", {}).get("dependencies", [])
        return []

    def _get_installed_packages(
        self, python: str | Path | None = None
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
        packages = " ".join(packages)
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
        packages = " ".join(packages)
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
        index: bool | str | Path | None = None,
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
        packages = " ".join(packages)
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
            if build_dir.is_dir():
                rmtree(build_dir, ignore_errors=True)

        # remove temporary prefix (to reduce disk usage)
        if not self.request.config.option.venv_keep_prefix:
            tmp_prefix = self.path / ".tmp_prefix"
            if tmp_prefix.is_dir():
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
        # install dependencies
        venv_marker = self.request.node.get_closest_marker(name="venv")
        install_deps = venv_marker.kwargs.get("install_dependencies", True)
        if install_deps:
            self.install_dependencies()
        if self.venv_lock and self.venv_lock.is_locked:
            self.venv_lock.release()

    def create_from_sample(self, sample: str) -> None:
        super().create_from_sample(sample)
        # install dependencies
        venv_marker = self.request.node.get_closest_marker(name="venv")
        install_deps = venv_marker.kwargs.get("install_dependencies", True)
        if install_deps:
            self.install_dependencies()
        if self.venv_lock and self.venv_lock.is_locked:
            self.venv_lock.release()

    def freeze(
        self,
        command: Sequence | Path | None = None,
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> pytest.RunResult:
        if IS_CONDA:
            self.prefix = self.venv_prefix
            self.python = self.venv_python
            try:
                return super().freeze(command, cwd, env, timeout)
            finally:
                self.prefix = self._prefix
                self.python = self._python
        # PYTHONPATH is the key here
        if env is None:
            env = os.environ.copy()
        venv_site = os.path.normpath(self.venv_prefix / self.relative_site)
        env["PYTHONPATH"] = venv_site
        return super().freeze(command, cwd, env, timeout)

    def install(
        self,
        packages: str | list[str],
        *,
        backend: str | None = None,
        binary: bool = True,
        index: bool | str | None = None,
        isolated: bool = False,  # noqa: ARG002
    ) -> pytest.RunResult:
        # install in the venv prefix
        self.prefix = self.venv_prefix
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
            prefix = self._root / f".{self.backend}-{self._name}"
            if scope == "function":
                prefix = prefix.with_name(
                    f"{prefix.name}-{self.request.function.__name__}"
                )
            self.venv_prefix = prefix
            self.venv_python = prefix / self.relative_bin / self.python.name
            self.venv_lock = FileLock(prefix.with_suffix(".lock"))
            self.venv_lock.acquire()

            if not self.venv_python.is_file():
                # create venv
                if self.backend == "conda":
                    self._venv_conda_clone()
                else:
                    self._venv_pip()
            # point to the existing lock file
            elif self.backend == "pip":
                self._lock = FileLock(self.venv_prefix / ".lock")

    def _venv_conda_clone(self) -> None:
        # create a clone venv
        conda_env = os.environ["CONDA_DEFAULT_ENV"]
        cmd = f"conda create --clone {conda_env} -p {self.venv_prefix} -q -y"
        self.run(cmd, cwd=self.system_path)

    def _venv_pip(self) -> None:
        # create venv
        prefix = os.path.normpath(self.venv_prefix)
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
            elif prefix.is_dir():
                rmtree(prefix, ignore_errors=True)


def normalize(name: str) -> str:
    """Normalize a package name."""
    return re.sub(r"[-_.]+", "-", name).lower()


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
    """Create package in temporary path, based on source (or sample),
    using a virtual environment.
    """
    tmp_pkg = TempPackageVenv(request, tmp_path_factory, monkeypatch)
    yield tmp_pkg
    tmp_pkg.cleanup()


@pytest.fixture
def tmp_package(request: pytest.FixtureRequest) -> TempPackage:
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
