"""Extract MSVC runtime package.

Code based on:
    https://github.com/conda-forge/vc-feedstock/blob/main/recipe/vc_repack.py
    https://github.com/conda-forge/vc-feedstock/blob/main/recipe/meta.yaml

But using cabarchive package (instead of 7z) to extract the cabs.

"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import time
import xml.dom.minidom
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.error import ContentTooShortError
from urllib.request import urlretrieve

import cabarchive
from filelock import FileLock
from striprtf.striprtf import rtf_to_text

from cx_Freeze._compat import PLATFORM

if TYPE_CHECKING:
    from collections.abc import Generator

__all__ = ["copy_msvcr_files"]

# All Microsoft CAB archives start with this signature
MS_CAB_HEADER = b"MSCF\0\0\0\0"

VC_REDIST_BASE_URL = "https://aka.ms/vs/{version}/release/{name}"

VC_VERSION_TABLE = {
    "15": "14.16.27052",
    "16": "14.29.30156",
    "17": "14.40.33816",
}

EXE_FILENAMES = {
    "win-arm64": "vc_redist.arm64.exe",
    "win-amd64": "vc_redist.x64.exe",
    "win32": "vc_redist.x86.exe",
}


def split_self_extract_exe(
    exe_file: Path, target_directory: Path
) -> list[str]:
    # The self-extracting exe file contains two embedded CAB archives.
    # Split these out using a match against the known Microsoft CAB
    # header.  It's not ideal, but it works.
    contents = exe_file.read_bytes()
    splits = contents.split(MS_CAB_HEADER)
    fnames = []
    for index, s in enumerate(splits[1:]):
        fname = f"cab{index:02}.cab"
        target_directory.joinpath(fname).write_bytes(MS_CAB_HEADER + s)
        fnames.append(fname)
    return fnames


def unpack_cab(cabfile: Path, tmpdir: Path) -> None:
    tmpdir.mkdir(exist_ok=True)
    cab = cabarchive.CabArchive(cabfile.read_bytes())
    for file in cab.values():
        target = tmpdir / file.filename
        target.write_bytes(file.buf)
        # Preserve timestamp
        date_time = time.mktime(
            datetime.combine(file.date, file.time).timetuple()
        )
        os.utime(target, (date_time, date_time))


def decode_manifest(directory: Path) -> dict[str, str]:
    # The first CAB file contains a manifest in the file "0" in XML format.
    dom = xml.dom.minidom.parse(os.fspath(directory / "0"))  # noqa: S318

    # The version is contained in Registration.Version
    registration = dom.documentElement.getElementsByTagName("Registration")
    version = registration[0].attributes["Version"].value
    line = f"MSVC Runtimes version: {version}"
    print("*" * len(line))
    print(line)
    print("*" * len(line))
    print(flush=True)

    # The other files have generic names such as a0, a1, etc.  The manifest
    # gives us their true names.  The FilePath contains the a0 type filename,
    # the SourcePath the true filename.
    payloads = dom.documentElement.getElementsByTagName("Payload")

    # Find the licence file.
    licences = [
        x.attributes
        for x in payloads
        if "FilePath" in x.attributes
        and x.attributes["FilePath"].value.lower() == "license.rtf"
    ]
    if len(licences) == 0:
        msg = "Found no licences in the manifest"
        raise RuntimeError(msg)
    if len(licences) > 1:
        msg = "Found more than one licence in the manfiest"
        raise RuntimeError(msg)

    # Find the files that are in the second CAB file. These have
    # helpful filenames of u0, u1, etc.
    containers = [x for x in payloads if "Container" in x.attributes]

    # The DLL files we want are in the second CAB file, with a name of
    # "packages\vcRuntimeMinimum_amd64\cab1.cab",
    # "packages\VC_Runtime_arm64\cab1.cab",
    # "packages\vcRuntimeMinimum_x86\cab1.cab" or similar
    def find_cab(r, v) -> bool:
        return r in v and v.endswith(".cab")

    runtimes = [
        i.attributes
        for i in containers
        if find_cab("vcRuntimeMinimum", i.attributes["FilePath"].value)
    ]
    if len(runtimes) == 0:
        runtimes = [
            i.attributes
            for i in containers
            if find_cab("VC_Runtime", i.attributes["FilePath"].value)
        ]
    if len(runtimes) == 0:
        msg = "Found no matches in the manifest"
        raise RuntimeError(msg)
    if len(runtimes) > 1:
        msg = "Found more than one match in the manfiest"
        raise RuntimeError(msg)

    return {
        "cabfile": runtimes[0]["SourcePath"].value,
        "licence": licences[0]["SourcePath"].value,
        "version": version,
    }


def fix_filename_and_copy(
    source_dir: Path, target_dir: Path
) -> Generator[Path]:
    # As of VS 17.6, the artifact contains intermediate DLL extensions,
    # which get renamed correctly upon installation; do it manually
    target_dir.mkdir(exist_ok=True)
    for file in source_dir.glob("*.dll*"):
        if file.name.startswith("api_"):
            new_fname = file.name.replace("_", "-")
        elif file.suffix.startswith(".dll_"):
            new_fname = file.stem + ".dll"
        else:
            new_fname = file.name
        print(f"Found DLL: {file.name} -> {new_fname}")
        shutil.copy2(file, target_dir / new_fname)
        yield target_dir / new_fname


def unpack_exe(exe_filename: Path, unpack_dir: Path) -> Generator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        cabs = split_self_extract_exe(exe_filename, tmp_path)
        # The first cab is the installer data
        # The second is the payload
        cabfile1 = tmp_path / cabs[0]
        cabdir1 = tmp_path / cabfile1.stem
        unpack_cab(cabfile1, cabdir1)
        payload = decode_manifest(cabdir1)
        # Get LICENSE and converts to txt
        unpack_dir.mkdir(parents=True, exist_ok=True)
        license_rtf = unpack_dir / "LICENSE.RTF"
        shutil.copy2(cabdir1 / payload["licence"], license_rtf)
        yield license_rtf
        text = rtf_to_text(
            license_rtf.read_text(encoding="cp1252", errors="strict")
        )
        license_txt = unpack_dir / "LICENSE.txt"
        license_txt.write_text(text, encoding="cp1252", errors="strict")
        yield license_txt
        # Get the payload
        cabfile2 = tmp_path / cabs[1]
        cabdir2 = tmp_path / cabfile2.stem
        unpack_cab(cabfile2, cabdir2)
        vc_redist = tmp_path / exe_filename.stem
        vc_redist.mkdir(exist_ok=True)
        unpack_cab(Path(cabdir2, payload["cabfile"]), vc_redist)
        yield from fix_filename_and_copy(vc_redist, unpack_dir)


def get_msvcr_files(
    version: str | None = None,
    target_platform: str | None = None,
    no_cache: bool = False,
) -> Generator[Path]:
    """Get MSVC runtime files."""
    if target_platform is None:
        target_platform = (
            PLATFORM if PLATFORM.startswith("win") else "win-amd64"
        )
    if target_platform in EXE_FILENAMES:
        name = EXE_FILENAMES[target_platform]
    else:
        msg = f"Architecture {target_platform} not supported"
        raise RuntimeError(msg)
    if version is None:
        version = max(VC_VERSION_TABLE.keys())
    if version not in VC_VERSION_TABLE:
        msg = f"Version {version} is not expected"
        raise RuntimeError(msg)

    # use a cache dir
    if os.environ.get("APPDATA"):
        cache_base = Path(os.path.expandvars("${APPDATA}"))
    else:
        cache_base = Path("~/.cache").expanduser()
    cache_dir = cache_base / f"cx_Freeze/vc_redist/{version}"
    cache_dir.mkdir(parents=True, exist_ok=True)
    filename = cache_dir / name
    unpack_dir = cache_dir / name.replace(".", "_")
    unpack_dir.mkdir(parents=True, exist_ok=True)
    with FileLock(filename.with_suffix(".lock")):
        if no_cache or (filename.exists() and filename.stat().st_size == 0):
            filename.unlink(missing_ok=True)
        url = VC_REDIST_BASE_URL.format(version=version, name=name)
        while not filename.exists():
            try:
                urlretrieve(url, filename)  # noqa: S310
            except ContentTooShortError as exc:
                print("warning:", exc.reason, "of", name, file=sys.stderr)
                print("retry!", file=sys.stderr)
                filename.unlink(missing_ok=True)
        if filename.exists():
            files = list(unpack_dir.glob("*.dll"))
            if no_cache or not files:
                yield from unpack_exe(filename, unpack_dir)
            else:
                yield from unpack_dir.iterdir()
        else:
            msg = f"{filename} not found"
            raise RuntimeError(msg)


def copy_msvcr_files(
    target_dir: Path | str,
    target_platform: str | None = None,
    version: str | None = None,
    dry_run: bool = False,
    no_cache: bool = False,
) -> None:
    """Copy MSVC runtime files."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    for file in get_msvcr_files(version, target_platform, no_cache):
        if not dry_run:
            shutil.copy2(file, target_dir / file.name)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract MSVC runtime package"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        help="Do not copy files, list files only",
        action="store_true",
    )
    parser.add_argument(
        "--target-dir", help="dist", metavar="DIR", default="dist"
    )
    parser.add_argument(
        "--target-platform",
        help="Target architecture (eg. win-arm64, win-amd64, win32)",
        default=None,
    )
    parser.add_argument(
        "--version",
        help="Runtime version number",
        default=None,
    )
    parser.add_argument(
        "--no-cache",
        help="Don't use the cached runtime",
        action="store_true",
    )
    args = parser.parse_args()

    copy_msvcr_files(
        args.target_dir,
        args.target_platform,
        args.version,
        args.dry_run,
        args.no_cache,
    )


if __name__ == "__main__":
    main()
