"""Helper module to run tests on Linux, Windows and macOS.

Also works with variants like conda-forge and MSYS2 (Windows).
"""

from __future__ import annotations

# ruff: noqa: D103
import argparse
import asyncio
import contextlib
import json
import os
import sys
from asyncio.subprocess import PIPE, Process
from base64 import b64encode
from pathlib import Path
from shutil import get_terminal_size, which
from sysconfig import get_platform, get_python_version
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

CI = bool(os.environ.get("CI", "") == "true")
CI_DIR = Path(sys.argv[0]).parent.resolve()
TOP_DIR = CI_DIR.parent
PLATFORM = get_platform()
IS_LINUX = PLATFORM.startswith("linux")
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith(("cygwin", "mingw"))
IS_WINDOWS = PLATFORM.startswith("win")
IS_FINAL_VERSION = sys.version_info.releaselevel == "final"

PY_VERSION = get_python_version()
TIMEOUT = 10
TIMEOUT_FOR_GUI = 20
COLUMNS = get_terminal_size()[0]
GROUP = "::group::"
ENDGROUP = "::endgroup::"


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


def get_app(
    data: list, sample: str, number: int
) -> tuple[str, str, tuple[str, ...]] | None:
    test_app = data.get("test_app", [f"test_{sample}"])
    if isinstance(test_app, str):
        test_app = [test_app]
    line = int(number or 0)
    if 0 <= line < len(test_app):
        full_line = test_app[line]
    else:
        return None

    if full_line.startswith(("cmd:", "cli:", "cui:", "gui:", "svc:")):
        apptype, name = full_line.split(":", 1)
    else:
        apptype, name = "cui", full_line

    # cmd
    if apptype == "cmd":
        if name.startswith("win:"):
            if IS_WINDOWS:
                name = name.split(":", 1)[1]
                popenargs = f"chcp 65001>nul && {name}"
            else:
                popenargs = name = "true"
        elif IS_WINDOWS:
            popenargs = name = "true"
        else:
            popenargs = name
        return apptype, name.split(" ", 1)[0], (popenargs,)

    # cli, cui, gui and svc
    try:
        name, args = name.split(" ", 1)
    except ValueError:
        args = None
    app = Path(name)
    if IS_WINDOWS or IS_MINGW:
        if not app.match("*.exe"):
            app = app.with_suffix(".exe")
        popenargs = [app.name]
    else:
        popenargs = [app.resolve()]
    if args is not None:
        popenargs.append(args)
    return apptype, app.stem, tuple(popenargs)


def get_command_line(command: tuple[Path | str, ...]) -> str:
    return " ".join(list(map(os.fspath, command)))


@contextlib.contextmanager
def pushd(target: Path | str) -> Generator:
    saved = os.getcwd()
    os.chdir(target)
    try:
        yield saved
    finally:
        os.chdir(saved)


async def run_cmd(command: tuple[str, ...], output: str) -> Process:
    if command[0] == "true":
        return None

    command_line = get_command_line(command)
    process = await asyncio.create_subprocess_shell(
        command_line, stdout=PIPE, stderr=PIPE
    )

    try:
        await asyncio.wait_for(process.wait(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        process.kill()
    stdout, stderr = await process.communicate()

    write_log(output, ".log", stdout, [f"Run shell command '{command_line}'"])
    if stderr:
        write_log(output, ".err", stderr)
    return process


async def run_cui(command: tuple[str, ...], output: str) -> Process:
    env = os.environ.copy()
    if IS_WINDOWS or IS_MINGW:
        env["PATH"] = r"C:\Windows;C:\Windows\System32"
    process = await asyncio.create_subprocess_exec(
        *command, stdout=PIPE, stderr=PIPE, env=env
    )

    try:
        await asyncio.wait_for(process.wait(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        process.kill()
    stdout, stderr = await process.communicate()

    command_line = get_command_line(command)
    write_log(output, ".log", stdout, [f"Run console app '{command_line}'"])
    if stderr:
        write_log(output, ".err", stderr)
    return process


async def run_gui(command: tuple[str, ...], output: str) -> Process:
    env = os.environ.copy()
    if IS_WINDOWS or IS_MINGW:
        env["PATH"] = r"C:\Windows;C:\Windows\System32"
    elif IS_MACOS and Path(command[0]).parent.name.endswith(".app"):
        command = list(command)
        command[0] = Path(command[0]).parent
        open_command = which("open")
        if open_command:
            # open -W -a app [--args arg1...]
            if len(command) > 1:
                command.insert(1, "--args")
            command = [open_command, "-W", "-a", *command]
    process = await asyncio.create_subprocess_exec(
        *command, stdout=PIPE, stderr=PIPE, env=env
    )
    try:
        await asyncio.wait_for(process.wait(), timeout=TIMEOUT_FOR_GUI)
        capture_messages = []
    except asyncio.TimeoutError:
        capture_messages = await run_gui_capture(output)
        process.kill()
    stdout, stderr = await process.communicate()

    # output to logfile
    command_line = get_command_line(command)
    header = [
        f"Run GUI app '{command_line}'",
        f"Process {process.pid} started the GUI app",
    ]
    write_log(output, ".log", stdout, header + capture_messages)
    if stderr:
        write_log(output, ".err", stderr)
    return process


async def run_gui_capture(output: str) -> list[str]:
    # make a screenshot after a timeout
    args = None
    messages = []
    logimage = Path(f"{output}.png")
    if IS_MACOS:
        name = "screencapture"
        screencapture = Path(which(name) or f"/usr/sbin/{name}")
        if screencapture.exists():
            args = [screencapture, "-T", "20", logimage]
    elif IS_LINUX:
        name = "gnome-screenshot"
        screencapture = Path(which(name) or f"/usr/bin/{name}")
        if CI or not screencapture.exists():
            name = "fallback ImageMagick"
            screencapture = Path(which("import") or "/usr/bin/import")
            if screencapture.exists():
                messages.append(
                    "INFO: using ImageMagick to capture the screen"
                )
                args = [screencapture, "-window", "root", logimage]
        else:
            args = [screencapture, f"--file={logimage}"]
    elif IS_WINDOWS or IS_MINGW:
        name = "screencapture"
        if os.getenv("WENV_PREFIX"):  # using wenv/wine
            screencapture = Path(__file__).parent / f"{name}.wine.bat"
        else:
            screencapture = Path(which(name) or f"~/bin/{name}.exe")
            screencapture = screencapture.expanduser()
        if screencapture.exists():
            args = [screencapture, logimage]
    print("screencapture", screencapture, file=sys.stderr)
    print("args", args, file=sys.stderr)
    if args is None:
        messages.append(f"WARNING: {name} not found")
    else:
        if screencapture.suffix in (".bat", ".cmd"):
            command_line = get_command_line(args)
            subproc = await asyncio.create_subprocess_shell(command_line)
        else:
            if IS_WINDOWS and sys.version_info[:2] <= (3, 8):
                args = list(map(os.fspath, args))
            subproc = await asyncio.create_subprocess_exec(*args)
        await subproc.wait()
        if subproc.returncode == 0:
            uri = logimage.absolute().as_uri()
            message = f"Taking a capture of the whole screen to {uri}"
        else:
            message = f"{name} failed with error {subproc.returncode}"
        messages.append(message)
    return messages


async def run_svc(
    command: tuple[str, ...],
    output: str,  # noqa: ARG001
) -> Process:
    env = os.environ.copy()
    if IS_WINDOWS or IS_MINGW:
        env["PATH"] = r"C:\Windows;C:\Windows\System32"
    return await asyncio.create_subprocess_exec(
        *command, stdout=PIPE, stderr=PIPE, env=env
    )


async def run_svc_kill(
    command: tuple[str, ...], output: str, process: Process
) -> Process:
    try:
        await asyncio.wait_for(process.wait(), timeout=TIMEOUT)
    except asyncio.TimeoutError:
        process.kill()
    stdout, stderr = await process.communicate()

    # output to logfile
    command_line = get_command_line(command)
    header = [
        f"Run server '{command_line}'",
        f"Process {process.pid} started the SVC app in background",
    ]
    write_log(output, ".log", stdout, header)
    if stderr:
        write_log(output, ".err", stderr)
    return process


def write_log(
    base: str,
    suffix: str,
    data: bytes | str | list[str],
    header: list[str] | None = None,
) -> None:
    info = "STDERR" if suffix == ".err" else "STDOUT"
    logfile = Path(f"{base}{suffix}")

    if isinstance(data, bytes):  # convert to str
        data = data.decode(encoding="utf_8", errors="ignore")
    if isinstance(data, str):
        data = data.strip().splitlines()

    output = []
    if header:
        output.extend(header)
    output.append(info + "=" * (COLUMNS - len(info)))
    output.extend(data)
    output.append("=" * COLUMNS)
    output.append("")
    with logfile.open(mode="w", encoding="utf_8", newline="") as file:
        file.write("\n".join(output))


def validatecode(returncode: int, output: str, apptype: str) -> int:
    errorlog = Path(f"{output}.err")
    if errorlog.exists():
        data = errorlog.read_text(encoding="utf_8")
        if len(data) != 0:
            # generic errors or
            # error for pyqt5
            # error for pyside2
            # error for pythonnet
            if (
                "error:" in data.lower()
                or "Reinstalling the application may f" in data
                or "Unable to import shiboken" in data
                or "Unhandled Exception:" in data
            ):
                returncode = 255
                # ignore error for wxPython 4.1.1
                # https://github.com/wxWidgets/Phoenix/commit/040c59fd991cd08174b5acee7de9418c23c9de33
                if IS_MINGW and "Error: Unable to set default locale:" in data:
                    return 0
            elif apptype == "gui" and returncode != 0:
                return 0
    return returncode


async def main_loop(sample, count, data, debug=False) -> int:
    svc_data = None, None, None
    number = 0
    exitcode_fail = 0
    platform_and_pyver = Path.cwd().name.replace("exe.", "").replace(".", "_")
    while count == 0 or (count != 0 and number == count):
        try:
            apptype, basename, appargs = get_app(data, sample, number)
        except TypeError:
            break

        output = f"{sample}-{number}-{basename}-{platform_and_pyver}"

        # run commands asynchronously
        process = None
        if apptype == "cmd":
            process = await run_cmd(appargs, output)
        elif apptype in ("cli", "cui"):
            process = await run_cui(appargs, output)
        elif apptype == "gui":
            process = await run_gui(appargs, output)
        elif apptype == "svc":
            if basename != "kill":
                svc_data = appargs, output, await run_svc(appargs, output)
            else:
                appargs, output, process = svc_data
                process = await run_svc_kill(appargs, output, process)

        if process is not None:
            returncode = validatecode(process.returncode, output, apptype)
            if returncode != 0:
                exitcode_fail = returncode
            command_line = get_command_line(appargs)
            if len(appargs) > 1:
                command_line = (
                    "b64:" + b64encode(command_line.encode()).decode()
                )
            print(process.pid, returncode, output, apptype, end=command_line)
        if debug:
            for ext in ("log", "err"):
                output_path = Path(f"{output}.{ext}")
                if output_path.exists():
                    print(output_path.read_text(encoding="utf_8"))

        number += 1
    print(f"status {exitcode_fail}")
    return exitcode_fail


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("sample")
    parser.add_argument("--directory")
    parser.add_argument("--count", type=int, default=0)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    sample = args.sample
    count = args.count
    directory = (
        args.directory
        or TOP_DIR / f"samples/{sample}/build/exe.{PLATFORM}-{PY_VERSION}"
    )

    # verify if platform to run is in use
    data = CI_DIR.joinpath("build-test.json").read_bytes()
    sample_data = json.loads(data).get(sample, {})
    platform = sample_data.get("platform", [])
    pid = 0
    ret = 255
    if not is_supported_platform(platform):
        print(pid, ret)
        sys.exit(-1)

    # start asyncio work
    if IS_WINDOWS or IS_MINGW:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    with pushd(directory):
        return asyncio.run(main_loop(sample, count, sample_data, args.debug))


if __name__ == "__main__":
    sys.exit(main())
