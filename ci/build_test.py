"""Helper module to build tests on Linux, Windows and macOS.

Also works with variants like conda-forge and MSYS2 (Windows).
"""

from __future__ import annotations

# ruff: noqa: D103
import argparse
import contextlib
import importlib.metadata as importlib_metadata
import json
import os
import re
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from shutil import which
from sysconfig import (
    get_config_var,
    get_path,
    get_platform,
    get_python_version,
)
from typing import TYPE_CHECKING
from urllib.request import urlcleanup, urlretrieve

if TYPE_CHECKING:
    from collections.abc import Generator
    from types import ModuleType


CI = bool(os.environ.get("CI", "") == "true")
CI_DIR = Path(sys.argv[0]).parent.resolve()
TOP_DIR = CI_DIR.parent
PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")
IS_FINAL_VERSION = sys.version_info.releaselevel == "final"
IS_MANYLINUX = os.environ.get("AUDITWHEEL_PLAT", "").startswith("manylinux")
PYTHON_VERSION = get_config_var("py_version")

PLATFORM_SYSTEM = PLATFORM.split("-")[0].replace("linux", "manylinux")
PLATFORM_ARCH = PLATFORM.split("-")[-1]
PLATFORM_TAG = f"{PLATFORM_SYSTEM}_{PLATFORM_ARCH}"
PYTHON_TAG = f"cp{get_config_var('py_version_nodot')}"

RE_PYTHON_VERSION = re.compile(r"\s*\"*\'*(\d+)\.*(\d*)\.*(\d*)\"*\'*")
RE_CONDA_BUILD_PYVER = re.compile(r"(py)(\d*)\s*")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()
CONDA_EXE = os.environ.get("CONDA_EXE", "conda")
MINGW_PACKAGE_PREFIX = os.environ.get("MINGW_PACKAGE_PREFIX", "")
UV = which("uv")
PIP_COMMAND = (
    [UV, "pip"]
    if UV and not os.environ.get("WINEPREFIX")
    else [sys.executable, "-m", "pip"]
)
PIP_UPGRADE = os.environ.get("PIP_UPGRADE", False)


def import_module_or_none(module_name) -> ModuleType | None:
    try:
        return import_module(module_name)
    except ImportError:
        return None


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


def is_supported_python(python_version: str) -> bool:
    packaging_specifiers = import_module_or_none("packaging.specifiers")
    if packaging_specifiers is None:
        return True
    python_version = python_version.replace("'", "").replace('"', "")
    return PYTHON_VERSION in packaging_specifiers.SpecifierSet(python_version)


def install_requirements(
    requires: str | list[str] | set[str],
    extra_index_url: list[str] | None = None,
    find_links: list[str] | None = None,
) -> list[str]:
    if isinstance(requires, str):
        requires = requires.split(",")
    if isinstance(requires, list):
        requires = set(requires)

    packaging_requirements = import_module_or_none("packaging.requirements")
    if packaging_requirements is None:

        class Requirement:
            def __init__(self, req: str) -> None:
                self.name = req

            def __str__(self) -> str:
                return self.name

    else:
        Requirement = packaging_requirements.Requirement

    pip_install = [*PIP_COMMAND, "install"]
    pacman_args = ["pacman", "--noconfirm", "--needed", "-S"]
    pacman_search = ["pacman", "--noconfirm", "-Ss"]
    conda_install = [CONDA_EXE, "install", "--prefix", sys.prefix, "-y", "-q"]
    conda_install += ["--no-channel-priority", "-S"]
    conda_search = [CONDA_EXE, "search", "--override-channels"]

    installed_packages = []
    conda_pkgs = []
    pip_pkgs = []
    for req in requires:
        installed = False
        alias_for_conda = None
        alias_for_mingw = None
        no_deps = False
        platform = None
        python_version = None
        only_binary = False
        pre_release = False
        prefer_binary = False
        require: Requirement | None = None
        upgrade = PIP_UPGRADE
        for req_data in req.split(" "):
            if req_data.startswith("--conda="):
                # alias_for_conda accepts version
                alias_for_conda = req_data.split("=", 1)[1]
            elif req_data.startswith("--mingw="):
                # alias_for_mingw discards version
                alias_for_mingw = req_data.split("=", 1)[1]
            elif req_data == "--no-deps":
                no_deps = True
            elif req_data.startswith("--platform="):
                platform = req_data.split("=")[1]
            elif req_data.startswith("--python-version"):
                python_version = req_data[len("--python-version") :]
            elif req_data == "--only-binary":
                only_binary = True
            elif req_data == "--pre":
                pre_release = True
            elif req_data == "--prefer-binary":
                prefer_binary = True
            elif req_data == "--upgrade":
                upgrade = True
            elif req_data:
                require = Requirement(req_data)
        if not is_supported_platform(platform):
            continue
        if python_version and not is_supported_python(python_version):
            continue
        if IS_CONDA:
            # minimal support for conda
            # NOTE: do not implement: no-deps, find-links
            if alias_for_conda is not None:
                if alias_for_conda == "":
                    continue
                require = Requirement(alias_for_conda)
            elif require is None:
                continue
            args = []
            if extra_index_url:
                for extra in extra_index_url:
                    packages_url = extra[:-1] if extra[-1] == "/" else extra
                    args2 = [
                        "-c",
                        f"{packages_url}/conda",
                        require.name,
                        "--json",
                    ]
                    process = subprocess.run(
                        conda_search + args2,
                        check=False,
                        stdout=subprocess.PIPE,
                    )
                    if process.returncode == 0:
                        output = json.loads(process.stdout)
                        pyver = get_config_var("py_version_nodot")
                        for file in output[require.name]:
                            build = file["build"]
                            match = RE_CONDA_BUILD_PYVER.search(build)
                            if match and match.group(2) == pyver:
                                args = [file["url"]]
                                break
            if args:
                process = subprocess.run(conda_install + args, check=False)
                if process.returncode == 0:
                    installed_packages.extend(args)
                    installed = True
                continue
            conda_pkgs.append(str(require))
            continue
        if IS_MINGW:
            # create a list of possible names of the package, because in
            # MSYS2 some packages are mapped to python-package or
            # lowercased, etc, for instance:
            # Cython is not mapped
            # cx_Logging is python-cx-logging
            # Pillow is python-Pillow
            # and so on.
            # TODO: emulate find_links support
            # TODO: emulate no_deps support only for python packages
            if alias_for_mingw is not None:
                if alias_for_mingw == "":
                    continue
                require = Requirement(alias_for_mingw)
            elif require is None:
                continue
            package = require.name
            packages = [f"python-{package}", package]
            if not package.islower():
                packages += [
                    package_name.lower() for package_name in packages[:]
                ]
            if "_" in package:
                packages += [
                    package_name.replace("_", "-")
                    for package_name in packages[:]
                ]
            elif "-" in package:
                packages += [
                    package_name.replace("-", "_")
                    for package_name in packages[:]
                ]
            for package_name in packages:
                package = f"{MINGW_PACKAGE_PREFIX}-{package_name}"
                args = [*pacman_search, package]
                process = subprocess.run(
                    args, stdout=subprocess.PIPE, encoding="utf_8", check=False
                )
                if process.returncode == 1:
                    continue  # does not exist with this name
                if process.returncode == 0 and "installed" in process.stdout:
                    installed_packages.append(package)
                    installed = True
                    break
                process = subprocess.run([*pacman_args, package], check=False)
                if process.returncode == 0:
                    installed_packages.append(package)
                    installed = True
                    break
            if installed:
                continue
        # use pip
        if require is None:
            continue
        args = []
        env = os.environ.copy()
        env["UV_PYTHON"] = sys.executable
        if no_deps:
            args.append("--no-deps")
        if only_binary:
            if 0:  # pylint: disable=using-constant-test
                # if IS_LINUX:
                # prefer manylinux2014 wheels
                platform = get_platform()
                for mod in ["_2_17_", "2014_", "_2_5_", "1_", "_2_28_"]:
                    linux2014 = platform.replace("-", mod)
                    args.append(f"--platform=many{linux2014}")
                args.append(f"--python-version={get_python_version()}")
                args.append("--only-binary=:all:")
                target = get_path("platlib")
                args.append(f"--target={target}")
                # FIXME: without '--upgrade' causes a bug with pyqt5.
                # FIXME: '--upgrade' causes a bug with pyqt6.
                # args extend(["--upgrade", "--upgrade-strategy=eager"])
            else:
                args.append(f"--only-binary={require.name}")
        if pre_release:
            env["PIP_PRE"] = "1"
            env["UV_PRERELEASE"] = "explicit"
        if prefer_binary:
            args.append("--prefer-binary")
        if upgrade:
            args.append("--upgrade")
        if args:
            if extra_index_url:
                args += [f"--extra-index-url={url}" for url in extra_index_url]
            if find_links:
                args += [f"--find-links={link}" for link in find_links]
            args = pip_install + args + [str(require)]
            print("args", args)
            process = subprocess.run(args, check=False, env=env)
            if process.returncode == 0:
                installed_packages.append(require.name)
                installed = True
            elif not IS_FINAL_VERSION and not pre_release:
                # in python preview, try a pre-release of the package too
                env["PIP_PRE"] = "1"
                env["UV_PRERELEASE"] = "allow"
                process = subprocess.run(args, check=False, env=env)
                if process.returncode == 0:
                    installed_packages.append(require.name)
                    installed = True
        else:
            pip_pkgs.append(str(require))
    if pip_pkgs:
        if extra_index_url:
            args = [f"--extra-index-url={extra}" for extra in extra_index_url]
        else:
            args = []
        if find_links:
            args = [f"--find-links={link}" for link in find_links] + args
        args = pip_install[:] + args + pip_pkgs
        print("args", args)
        env = os.environ.copy()
        env["UV_PYTHON"] = sys.executable
        process = subprocess.run(args, check=False, env=env)
        if process.returncode == 0:
            installed_packages.extend(pip_pkgs)
    if conda_pkgs:
        conda_forge = ["--override-channels", "-c", "conda-forge"]
        process = subprocess.run(
            conda_install + conda_forge + conda_pkgs, check=False
        )
        if process.returncode == 0:
            installed_packages.extend(conda_pkgs)
        # TODO: fallback to pip on error
    return installed_packages


def cx_freeze_status() -> tuple[str, bool]:
    # working in samples directory
    try:
        version = importlib_metadata.version("cx_Freeze")
        installed = True
    except importlib_metadata.PackageNotFoundError:
        cx_freeze = TOP_DIR / "cx_Freeze" / "__init__.py"
        version = ""
        for line in cx_freeze.read_text(encoding="utf_8").splitlines():
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().replace('"', "")
                if "-" in version:
                    version = "".join(version.replace("-", ".").rsplit(".", 1))
                break
        installed = False
    return version, installed


def cibuildwheel_file() -> Path | None:
    cx_freeze_version, _ = cx_freeze_status()
    pattern = f"cx_Freeze-{cx_freeze_version}-{PYTHON_TAG}-{PYTHON_TAG}-"
    if IS_WINDOWS:
        pattern += PLATFORM.replace("-", "_") + ".whl"
    else:
        pattern += f"{PLATFORM_SYSTEM}_*_{PLATFORM_ARCH}.whl"
    files = sorted(TOP_DIR.joinpath("wheelhouse").glob(pattern), reverse=True)
    return files[0] if files else None


def install_requires(
    test_data: dict | None = None,
    extra_index_url: list | None = None,
    find_links: list | None = None,
    requirements: list | None = None,
    dist: bool = False,
    editable: bool = False,
    latest: bool = False,
    debug: bool = False,  # noqa: ARG001
    verbose: bool = False,
) -> None:
    """Process the install requirements."""
    # Check for pyproject.toml
    pyproject_toml = TOP_DIR / "pyproject.toml"
    if not pyproject_toml.exists():
        print("pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    basic_requirements = set()
    installed_packages = []

    packaging_req = import_module_or_none("packaging.requirements")
    if packaging_req is None:
        installed_packages += install_requirements(["packaging"])
        packaging_req = import_module_or_none("packaging.requirements")
    Requirement = packaging_req.Requirement

    if IS_MINGW:
        basic_requirements.add("ca-certificates")

    if UV is None:
        basic_requirements.add("pip --upgrade")

    # Get the basic requirements from pyproject.toml
    tomllib = import_module_or_none("tomllib")
    if tomllib is None:  # only py 3.11+ has tomllib
        installed_packages += install_requirements(["tomli"])
        tomllib = import_module_or_none("tomli")
    config = tomllib.loads(pyproject_toml.read_bytes().decode())
    try:
        bs_requires = {
            require.name: require
            for require in map(Requirement, config["build-system"]["requires"])
        }
        for dependency in map(Requirement, config["project"]["dependencies"]):
            # the dependency must match the current environment
            if dependency.marker and not dependency.marker.evaluate():
                continue
            # clean the marker to get dependency with specifiers only
            dependency.marker = None
            # prefer the required to build dependency
            dependency_in_bs = bs_requires.get(dependency.name)
            if dependency_in_bs:
                dependency_in_bs.marker = None
                package = str(dependency_in_bs)
            else:
                package = str(dependency)
            if package.startswith("lief"):
                package += " --conda=py-lief --only-binary"
            basic_requirements.add(package)
    except KeyError:
        pass

    packages_index_url = "https://marcelotduarte.github.io/packages/"
    installed_packages += install_requirements(
        basic_requirements,
        extra_index_url=[] if IS_FINAL_VERSION else [packages_index_url],
    )

    # install cx_Freeze and requirements for sample
    cx_freeze_version, cx_freeze_installed = cx_freeze_status()
    if test_data:
        # prepare environ
        env = os.environ.copy()
        env["UV_PYTHON"] = sys.executable
        # uninstall
        if cx_freeze_installed:
            if IS_CONDA:
                conda_remove = [CONDA_EXE, "remove", "-p", sys.prefix, "-y"]
                process = subprocess.run(
                    [*conda_remove, "--force-remove", "cx_freeze"], check=False
                )
            elif IS_MINGW:
                pacman_remove = ["pacman", "--noconfirm", "-R"]
                package = f"{MINGW_PACKAGE_PREFIX}-python-cx-freeze"
                process = subprocess.run(
                    [*pacman_remove, package], check=False
                )

            cmd = [*PIP_COMMAND, "uninstall", "cx_Freeze"]
            if PIP_COMMAND[0] == sys.executable:  # python -m pip
                cmd.append("-y")
            process = subprocess.run(cmd, check=False, env=env)
        # cx_freeze in distribution mode?
        if dist:
            if IS_CONDA:
                # DISABLED
                if 0:  # pylint: disable=using-constant-test
                    # if require not in installed_packages:
                    platform_opt = "--platform=darwin,linux"
                    conda_requirements = [f"c-compiler {platform_opt}"]
                    installed_packages += install_requirements(
                        conda_requirements
                    )
                    cmd = [
                        *PIP_COMMAND,
                        *"install . --no-deps --no-cache-dir -vvv".split(),
                    ]
                    process = subprocess.run(cmd, cwd=TOP_DIR, check=False)
                    if process.returncode == 0:
                        # update the status
                        cx_freeze_version, cx_freeze_installed = (
                            cx_freeze_status()
                        )
                editable = True  # for now
            elif IS_MINGW:
                editable = True  # for now
            elif IS_LINUX or IS_MACOS or IS_WINDOWS:
                wheel_file = cibuildwheel_file()
                if wheel_file is None and not IS_MANYLINUX:
                    if IS_MACOS or IS_WINDOWS:
                        installed_packages += install_requirements("build")
                        cmd = "build -n -x -w -o wheelhouse".split()
                    else:
                        installed_packages += install_requirements(
                            "cibuildwheel"
                        )
                        cmd = [
                            "cibuildwheel",
                            "--only",
                            f"{PYTHON_TAG}-{PLATFORM_TAG}",
                        ]
                        if not IS_FINAL_VERSION:
                            cmd.append("--prerelease-pythons")
                        if IS_LINUX and which("podman"):  # prefer podman
                            env["CIBW_CONTAINER_ENGINE"] = "podman"
                    process = subprocess.run(
                        [sys.executable, "-m", *cmd],
                        check=False,
                        cwd=TOP_DIR,
                        env=env,
                    )
                    wheel_file = cibuildwheel_file()
                if wheel_file is None:
                    print(
                        "ERROR: wheel file not found - build it",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                cmd = [*PIP_COMMAND, "install", wheel_file]
                if PIP_COMMAND[0] == UV:
                    cmd.append("--reinstall")
                else:
                    cmd.append("--force-reinstall")
                if verbose:
                    cmd.append("--verbose")
                process = subprocess.run(
                    cmd, check=False, cwd=os.fspath(TOP_DIR), env=env
                )
        # cx_freeze in editable (development) mode?
        if editable:
            # install editable
            cmd = [
                *PIP_COMMAND,
                *"install -e. --no-build-isolation --no-deps".split(),
            ]
            if PIP_COMMAND[0] == UV:
                cmd.append("--reinstall")
            else:
                cmd.append("--force-reinstall")
            if verbose:
                cmd.append("--verbose")
            if IS_WINDOWS and bool(env.get("CI", None)):
                env["CIBUILDWHEEL"] = "1"  # to force build_ext in GHA
            process = subprocess.run(
                cmd, check=False, cwd=os.fspath(TOP_DIR), env=env
            )
        # cx_freeze latest
        elif latest:
            # install from official repository
            installed_packages += install_requirements("cx_Freeze")
        # update the status
        cx_freeze_version, cx_freeze_installed = cx_freeze_status()
        if not cx_freeze_installed:
            # install cx_Freeze from packages
            if IS_MINGW:
                # download and install
                packages_url = packages_index_url[:-1]
                package = f"{MINGW_PACKAGE_PREFIX}-python-cx-freeze"
                filename = f"{package}-{cx_freeze_version}-1-any.pkg.tar.zst"
                file_url = f"{packages_url}/msys2/{filename}"
                print("download:", file_url)
                file_tmp, headers = urlretrieve(file_url)  # noqa: S310
                print(headers)
                cmd = ["pacman", "--noconfirm", "-U", file_tmp]
                process = subprocess.run(cmd, check=False)
                if process.returncode == 0:
                    installed_packages.append(package)
                urlcleanup()
            else:
                if IS_CONDA:
                    require = "cx_freeze"
                else:
                    require = f"cx_Freeze~={cx_freeze_version[:-1]}0"
                installed_packages += install_requirements(
                    f"{require} --pre --no-deps",
                    extra_index_url=[packages_index_url],
                )

        # install requirements for sample
        if requirements:
            installed_packages += install_requirements(
                requirements, extra_index_url or [], find_links or []
            )

    if installed_packages:
        print("Requirements installed:", " ".join(installed_packages))


@contextlib.contextmanager
def pushd(target) -> Generator:
    saved = os.getcwd()
    os.chdir(target)
    try:
        yield saved
    finally:
        os.chdir(saved)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sample")
    parser.add_argument("--basic-requirements", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dist", action="store_true")
    parser.add_argument("--editable", action="store_true")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    path = TOP_DIR / "samples" / args.sample
    test_sample = path.name

    # verify if platform to run is in use
    test_json = CI_DIR / "build-test.json"
    test_data = {"test_app": f"test_{test_sample}"}  # default test_data
    test_data = json.loads(test_json.read_bytes()).get(test_sample, test_data)
    if not is_supported_platform(test_data.get("platform")):
        return -1
    # check parameters
    if args.basic_requirements:
        install_requires()
        return 0
    kw = {
        "extra_index_url": test_data.pop("extra_index_url", None),
        "find_links": test_data.pop("find_links", None),
        "requirements": test_data.pop("requirements", None),
        "dist": args.dist,
        "editable": args.editable,
        "latest": args.latest,
        "debug": args.debug,
        "verbose": args.verbose,
    }

    print("args:", args)
    print("data:", test_data)
    print("kw:", kw)

    # work in samples directory
    with pushd(path):
        install_requires(test_data, **kw)
        return None


if __name__ == "__main__":
    sys.exit(main())
