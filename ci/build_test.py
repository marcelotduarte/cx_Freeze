"""Helper module to build tests on Linux, Windows and macOS.

Also works with variants like conda-forge and MSYS2 (Windows).
"""
from __future__ import annotations

# ruff: noqa: D103
# pylint: disable=missing-function-docstring
import argparse
import contextlib
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from shutil import which
from sysconfig import (
    get_config_var,
    get_path,
    get_platform,
    get_python_version,
)

try:
    from tomllib import load as toml_load
except ImportError:
    try:
        from setuptools.extern.tomli import load as toml_load
    except ImportError:
        toml_load = None

CI = bool(os.environ.get("CI", "") == "true")
CI_DIR = Path(sys.argv[0]).parent.resolve()
TOP_DIR = CI_DIR.parent
PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")
IS_FINAL_VERSION = sys.version_info.releaselevel == "final"

RE_PYTHON_VERSION = re.compile(r"\s*\"*\'*(\d+)\.*(\d*)\.*(\d*)\"*\'*")
RE_CONDA_BUILD_PYVER = re.compile(r"(py)(\d*)\s*")

IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()
CONDA_EXE = os.environ.get("CONDA_EXE", "conda")
PIP_UPGRADE = os.environ.get("PIP_UPGRADE", False)
PIPENV_ACTIVE = bool(os.environ.get("PIPENV_ACTIVE", 0))


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
    python_version_in_use = sys.version_info[:3]
    numbers = RE_PYTHON_VERSION.split(python_version)
    operator = numbers[0]
    python_version_required = tuple(int(num) for num in numbers[1:] if num)
    evaluate = f"{python_version_in_use}{operator}{python_version_required}"
    return eval(evaluate)  # pylint: disable=eval-used # noqa: PGH001


def install_requirements(
    requires: str | list[str] | set[str],
    extra_index_url: list[str] | None = None,
    find_links: list[str] | None = None,
) -> list[str]:
    if isinstance(requires, str):
        requires = requires.split(",")
    if isinstance(requires, list):
        requires = set(requires)
    if IS_MINGW:
        host_gnu_type = get_config_var("HOST_GNU_TYPE").split("-")
        host_type = host_gnu_type[0]  # i686,x86_64
        mingw_w64_hosttype = f"mingw-{host_gnu_type[1]}-"  # mingw-w64-
        basic_platform = f"mingw_{host_type}"  # mingw_x86_64
        if len(PLATFORM) > len(basic_platform):
            msys_variant = PLATFORM[len(basic_platform) + 1 :]
            mingw_w64_hosttype += msys_variant + "-"  # clang,ucrt
        mingw_w64_hosttype += host_type

    pip_install = [sys.executable, "-m", "pip", "install"]
    pipenv_install = ["pipenv", "install"]
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
        require = None
        for req_data in req.split(" "):
            if req_data.startswith("--conda="):
                # alias_for_conda accepts version
                alias_for_conda = req_data.split("=", 1)[1]
            elif req_data.startswith("--mingw="):
                alias_for_mingw = req_data.split("=")[1]
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
            else:
                require = req_data
        if not is_supported_platform(platform):
            continue
        if python_version and not is_supported_python(python_version):
            continue
        if IS_CONDA:
            # minimal support for conda
            # NOTE: do not implement: no-deps, find-links
            if alias_for_conda:
                require = alias_for_conda
            if require is None:
                continue
            args = []
            if extra_index_url:
                for extra in extra_index_url:
                    packages_url = extra[:-1] if extra[-1] == "/" else extra
                    args2 = ["-c", f"{packages_url}/conda", require, "--json"]
                    process = subprocess.run(
                        conda_search + args2,
                        check=False,
                        stdout=subprocess.PIPE,
                    )
                    if process.returncode == 0:
                        output = json.loads(process.stdout)
                        pyver = get_config_var("py_version_nodot")
                        for file in output[require]:
                            build = file["build"]
                            match = RE_CONDA_BUILD_PYVER.search(build)
                            if match and match.group(2) == pyver:
                                require = file["url"]
                                args = [require]
                                break
            if args:
                process = subprocess.run(conda_install + args, check=False)
                if process.returncode == 0:
                    installed_packages.append(require)
                    installed = True
                continue
            conda_pkgs.append(require)
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
            # TODO: use regex
            if alias_for_mingw:
                require = alias_for_mingw
            if require is None:
                continue
            package = require.split(";")[0].split("!=")[0]
            package = package.split(">")[0].split("<")[0].split("=")[0]
            packages = [f"python-{package}", package]
            if package != package.lower():
                packages.insert(0, package.lower())
                packages.insert(0, f"python-{package.lower()}")
            for package_name in packages:
                package = f"{mingw_w64_hosttype}-{package_name}"
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
        if no_deps and not PIPENV_ACTIVE:
            args.append("--no-deps")
        if only_binary and not PIPENV_ACTIVE:
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
                # FIXME: w/o --upgrade causes a bug with pyqt5.
                # FIXME: --upgrade causes a bug with pyqt6.
                # args.append("--upgrade")
                # args.append("--upgrade-strategy=eager")
            else:
                args.append(f"--only-binary={require}")
        if pre_release:
            args.append("--pre")
        if prefer_binary and not PIPENV_ACTIVE:
            args.append("--prefer-binary")
        if args:
            if PIPENV_ACTIVE:
                if extra_index_url:
                    args += [f"--index={extra_index_url[0]}"]
                args = pipenv_install[:] + args + [require]
            else:
                if extra_index_url:
                    args += [
                        f"--extra-index-url={url}" for url in extra_index_url
                    ]
                if find_links:
                    args += [f"--find-links={link}" for link in find_links]
                if PIP_UPGRADE:
                    args.append("--upgrade")
                args = pip_install + args + [require]
            print("args", args)
            process = subprocess.run(args, check=False)
            if process.returncode == 0:
                installed_packages.append(require)
                installed = True
            elif not IS_FINAL_VERSION and not pre_release:
                # in python preview, try a pre-release of the package too
                args.append("--pre")
                process = subprocess.run(args, check=False)
                if process.returncode == 0:
                    installed_packages.append(require)
                    installed = True
        else:
            pip_pkgs.append(require)
    if pip_pkgs:
        if extra_index_url:
            args = [f"--extra-index-url={extra}" for extra in extra_index_url]
        else:
            args = []
        if find_links:
            args = [f"--find-links={link}" for link in find_links] + args
        if PIP_UPGRADE:
            args.append("--upgrade")
        if PIPENV_ACTIVE:
            # ignore extra args
            args = pipenv_install[:] + pip_pkgs
        else:
            args = pip_install[:] + args + pip_pkgs
        print("args", args)
        process = subprocess.run(args, check=False)
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
        cx_freeze = __import__("cx_Freeze")
        version = cx_freeze.__version__
        installed = True
    except (ModuleNotFoundError, AttributeError):
        cx_freeze = TOP_DIR / "cx_Freeze" / "__init__.py"
        version = ""
        for line in cx_freeze.read_text().splitlines():
            if line.startswith("__version__"):
                version = line.split("=")[1].replace("-", ".")
                break
        version = version.strip().replace('"', "")
        installed = False
    return version, installed


def cibuildwheel_only() -> str:
    pyver = get_python_version().replace(".", "")
    platform = PLATFORM.replace("linux", "manylinux").replace("-", "_")
    return f"cp{pyver}-{platform}"


def cibuildwheel_file() -> Path | None:
    pyver = get_python_version().replace(".", "")
    platform = PLATFORM.replace("linux", "manylinux").replace("-", "*_")
    cx_freeze_version, _ = cx_freeze_status()
    pattern = f"cx_Freeze-{cx_freeze_version}-*-cp{pyver}-{platform}.whl"
    files = list(TOP_DIR.joinpath("wheelhouse").glob(pattern))
    if files:
        return files[0]
    return None


def install_requires(test_data: dict | None):
    """Process the install requirements."""
    cx_freeze_version, cx_freeze_installed = cx_freeze_status()

    if PIPENV_ACTIVE or IS_CONDA or IS_MINGW:
        basic_requirements = set()
    else:
        basic_requirements = {"pip", "build", "wheel"}
    installed_packages = []

    # Get the basic requirements from pyproject.toml
    pyproject_toml = TOP_DIR / "pyproject.toml"
    if not pyproject_toml.exists():
        print("pyproject.toml not found", file=sys.stderr)
        sys.exit(1)

    with pyproject_toml.open("rb") as file:
        if toml_load is None:
            installed_packages = install_requirements("tomli")
            config = __import__("tomli").load(file)
        else:
            config = toml_load(file)

    try:
        dependencies = config["project"]["dependencies"]
        for dependency in dependencies:  # type: str
            if ";sys_platform == 'linux'" in dependency:
                add_platform = "--platform=linux"
            elif ";sys_platform == 'win32'" in dependency:
                add_platform = "--platform=windows,mingw"
            else:
                add_platform = ""
            package = dependency.partition(";")[0] + add_platform
            if package.startswith("lief"):
                package += " --conda=py-lief --only-binary"
            basic_requirements.add(package)
    except KeyError:
        pass

    extra_index_url = ["https://marcelotduarte.github.io/packages/"]
    installed_packages += install_requirements(
        basic_requirements,
        extra_index_url,
        # find_links=["https://lief.s3-website.fr-par.scw.cloud/latest/lief/"],
    )

    # install cx_Freeze if needed, and requirements for sample
    if test_data:
        if not CI and not IS_CONDA and not PIPENV_ACTIVE:
            # in development mode
            if cx_freeze_installed:
                cmd = [sys.executable, "-m", "pip", "uninstall", "-y"]
                cmd.append("cx_Freeze")
                process = subprocess.run(cmd, cwd=TOP_DIR, check=False)
            # install editable
            cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
            cmd += ["--no-build-isolation", "--no-deps"]
            process = subprocess.run(cmd, cwd=TOP_DIR, check=False)
            if IS_LINUX:
                # build a manylinux to extract the binaries (simulate editable)
                installed_packages += install_requirements("cibuildwheel")
                cmd = [sys.executable, "-m", "cibuildwheel"]
                cmd += ["--only", cibuildwheel_only()]
                env = dict(os.environ)
                podman = which("podman")
                if podman:
                    env["CIBW_CONTAINER_ENGINE"] = podman
                process = subprocess.run(
                    cmd, cwd=TOP_DIR, check=False, env=env
                )
                wheelfile = cibuildwheel_file()
                if wheelfile:
                    with zipfile.ZipFile(wheelfile) as wheelzip:
                        members = [
                            name
                            for name in wheelzip.namelist()
                            if name.startswith("cx_Freeze/bases/")
                        ]
                        wheelzip.extractall(TOP_DIR, members)
            # update the status
            cx_freeze_version, cx_freeze_installed = cx_freeze_status()
        if not cx_freeze_installed:
            require = f"cx_Freeze~={cx_freeze_version[:-1]}0 --conda=cx_freeze"
            installed_packages += install_requirements(
                f"{require} --pre --no-deps", extra_index_url
            )

        # install requirements for sample
        extra_index_url = test_data.get("extra_index_url", [])
        find_links = test_data.get("find_links", [])
        requires = test_data.get("requirements", [])
        if requires:
            installed_packages += install_requirements(
                requires, extra_index_url, find_links
            )

        if 0:  # pylint: disable=using-constant-test
            # code disabled for now
            # if require not in installed_packages:
            if IS_CONDA:
                platform_opt = "--platform=darwin,linux"
                conda_requirements = [
                    f"c-compiler {platform_opt}",
                    f"libpython-static --python-version>=3.8 {platform_opt}",
                ]
                installed_packages += install_requirements(conda_requirements)
                cmd = [sys.executable, "-m", "pip", "install"]
                cmd += [".", "--no-deps", "--no-cache-dir", "-vvv"]
                process = subprocess.run(cmd, cwd=TOP_DIR, check=False)
            if process.returncode == 0:
                # update the status
                cx_freeze_version, cx_freeze_installed = cx_freeze_status()

    if installed_packages:
        print("Requirements installed:", " ".join(installed_packages))


@contextlib.contextmanager
def pushd(target):
    saved = os.getcwd()
    os.chdir(target)
    try:
        yield saved
    finally:
        os.chdir(saved)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sample")
    parser.add_argument("--basic-requirements", action="store_true")
    parser.add_argument("--all-requirements", action="store_true")
    args = parser.parse_args()
    path = TOP_DIR / "samples" / args.sample
    test_sample = path.name

    # verify if platform to run is in use
    test_json = CI_DIR / "build-test.json"
    test_data = json.loads(test_json.read_text()).get(
        test_sample, {"test_app": f"test_{test_sample}"}
    )
    if not is_supported_platform(test_data.get("platform")):
        sys.exit(-1)

    if args.basic_requirements or args.all_requirements:
        # work in samples directory
        with pushd(path):
            install_requires(test_data if args.all_requirements else None)
    else:
        parser.error("invalid parameters.")


if __name__ == "__main__":
    main()
