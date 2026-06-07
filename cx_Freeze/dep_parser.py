"""Implements `Parser` interface.

Creates an abstraction to parse binary files.
"""

from __future__ import annotations

import os
import re
import shutil
import stat
import subprocess
from abc import ABC, abstractmethod
from contextlib import suppress
from ctypes.util import find_library
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, cast

from cx_Freeze._compat import PLATFORM
from cx_Freeze.exception import PlatformError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from cx_Freeze._typing import StrPath

# In Windows, to get dependencies, the default is to use lief package,
# but LIEF can be disabled with:
# set CX_FREEZE_BIND=imagehlp

# In Linux, to get dependencies, the default is to use ldd in x64 platforms
LDD_DISABLED = (
    os.environ.get(
        "CX_FREEZE_BIND", "" if PLATFORM.endswith("x86_64") else "patchelf"
    )
    == "patchelf"
)
PE_EXT = (".exe", ".dll", ".pyd")
MAGIC_ELF = b"\x7fELF"
NON_ELF_EXT = [".a", ".c", ".gif", ".h", ".html", ".jar", ".jpeg", ".jpg"]
NON_ELF_EXT += [".json", ".png", ".pxd", ".py", ".pyc", ".pyi", ".pyx"]
NON_ELF_EXT += [".txt", ".xml"]


class Parser(ABC):
    """`Parser` interface."""

    def __init__(
        self,
        path: list[str],
        bin_path_includes: list[str],
        silent: int,
        warnings: dict[str, bool],
    ) -> None:
        self._path: list[str] = path
        self._bin_path_includes: list[str] = bin_path_includes
        self._silent: int = silent
        self._warnings: dict[str, bool] = warnings

        self.dependent_files: dict[Path, set[Path]] = {}

    @property
    def search_path(self) -> list[Path]:
        """The default search path."""
        # This cannot be cached because os.environ["PATH"] can be changed in
        # freeze module before the call to get_dependent_files.
        env_path = os.get_exec_path()
        new_path = []
        for path in self._path + self._bin_path_includes + env_path:
            with suppress(PermissionError):
                resolved_path = Path(path).resolve()
                if resolved_path not in new_path and resolved_path.is_dir():
                    new_path.append(resolved_path)
        return new_path

    def find_library(
        self, name: str, search_path: list[StrPath] | None = None
    ) -> Path | None:
        """Returns the pathname of a library, or None."""
        if search_path is None:
            search_path = cast("list[StrPath]", self.search_path)
        for directory in map(Path, search_path):
            library = directory / name
            if self._is_binary(library):
                return library.resolve()
        return None

    def get_dependent_files(self, filename: StrPath) -> set[Path]:
        """Return the file's dependencies using platform-specific tools."""
        filename = Path(filename).resolve()

        with suppress(KeyError):
            return self.dependent_files[filename]

        if not self._is_binary(filename):
            return set()

        dependent_files: set[Path] = self._get_dependent_files(filename)
        self.dependent_files[filename] = dependent_files
        return dependent_files

    @abstractmethod
    def _get_dependent_files(self, filename: Path) -> set[Path]:
        """Return the file's dependencies using platform-specific tools.

        The tools used are `patchelf" and `ldd` on Linux, `otool` on macOS and
        `lief` on Windows. The imagehlp library can be used, through
        `freeze_core.util` extension module, on Windows when lief is disabled
        or is not available.
        Limit this list by the exclusion lists as needed.
        (Implemented separately for each platform).
        """

    @staticmethod  # pragma: no cover
    def _is_binary(filename: Path) -> bool:
        """Determines whether the file is a binary file.

        Binary file can be an executable or a shared library.
        (Implemented separately for each platform).
        """
        return filename.is_file()


class PEParser(Parser):
    """`PEParser` is based on the `lief` package.

    If it is disabled, or not available, use the old friend `freeze_core.util`
    extension module.
    """

    def __init__(
        self,
        path: list[str],
        bin_path_includes: list[str],
        silent: int,
        warnings: dict[str, bool],
    ) -> None:
        if os.environ.get("CX_FREEZE_BIND", "") == "imagehlp":
            lief = None
        else:
            try:
                import lief  # noqa: PLC0415 # ty: ignore[unresolved-import]
            except ImportError:
                lief = None  # ty: ignore[invalid-assignment]
            else:
                lief.logging.set_level(lief.logging.LEVEL.ERROR)
        super().__init__(path, bin_path_includes, silent, warnings)
        if lief:
            imports_only = lief.PE.ParserConfig()
            imports_only.parse_exports = False
            imports_only.parse_imports = True
            imports_only.parse_reloc = False
            imports_only.parse_rsrc = False
            imports_only.parse_signature = False
            self.imports_only = imports_only
            resource_only = lief.PE.ParserConfig()
            resource_only.parse_exports = False
            resource_only.parse_imports = False
            resource_only.parse_reloc = False
            resource_only.parse_rsrc = True
            resource_only.parse_signature = False
            self.resource_only = resource_only
            self.lief_errors = lief.lief_errors
            self._pe = lief.PE
        else:
            from freeze_core.util import (  # noqa: PLC0415
                BindError,
                GetDependentFiles,
            )

            self.GetDependentFiles = GetDependentFiles
            self.BindError = BindError
            self._pe = None

    @staticmethod
    def _is_binary(filename: StrPath) -> bool:
        """Determines whether the file is a PE file."""
        filename = Path(filename)
        return filename.suffix.lower().endswith(PE_EXT) and filename.is_file()

    is_pe = _is_binary

    def _get_dependent_files(self, filename: Path) -> set[Path]:
        if self._pe is None:
            return self._get_dependent_files_imagehlp(filename)
        with filename.open("rb", buffering=0) as raw:
            binary = self._pe.parse(raw, self.imports_only)
        if not binary:
            return set()

        libraries: list[str] = []
        if binary.has_imports:
            for library in binary.libraries:
                if not isinstance(library, str):
                    libraries.append(library.decode())
                else:
                    libraries.append(library)
        if binary.has_delay_imports:
            for library in binary.delay_imports:
                if not isinstance(library.name, str):
                    libraries.append(library.name.decode())
                else:
                    libraries.append(library.name)

        dependent_files: set[Path] = set()
        search_path: list[StrPath] = [filename.parent, *self.search_path]
        for name in libraries:
            library = self.find_library(name, search_path)
            if library:
                dependent_files.add(library)
                if name in self._warnings:
                    self._warnings[name] = False
            elif name not in self._warnings:
                self._warnings[name] = True
        return dependent_files

    def _get_dependent_files_imagehlp(self, filename: Path) -> set[Path]:
        env_path = os.environ["PATH"]
        os.environ["PATH"] = os.pathsep.join(
            [os.path.normpath(path) for path in self.search_path]
        )
        try:
            return {Path(dep) for dep in self.GetDependentFiles(filename)}
        except self.BindError as exc:
            # Sometimes this gets called when filename is not actually
            # a library (See issue 88).
            if self._silent < 3:
                print("WARNING: ignoring error during ", end="")
                print(f"GetDependentFiles({filename}):", exc)
        finally:
            os.environ["PATH"] = env_path
        return set()

    def read_manifest(self, filename: StrPath) -> str | None:
        """Read the XML schema of the manifest included in the executable."""
        if self._pe is None:
            if self._silent < 3:
                print(f"WARNING: ignoring read manifest for {filename}")
            return None
        filename = Path(filename)
        with filename.open("rb", buffering=0) as raw:
            binary = self._pe.parse(raw, self.resource_only)
        if binary and binary.has_resources:
            resources_manager = binary.resources_manager
            if (
                not isinstance(resources_manager, self.lief_errors)
                and resources_manager.has_manifest
            ):
                manifest = resources_manager.manifest
                if not isinstance(manifest, str):
                    manifest = manifest.decode()
                return manifest
        if self._silent < 3:
            print(f"WARNING: ignoring read manifest for {filename}")
        return None

    def write_manifest(self, filename: StrPath, manifest: str) -> None:
        """Write the XML schema of the manifest into the executable."""
        if self._pe is None:
            if self._silent < 3:
                print(f"WARNING: ignoring write manifest for {filename}")
            return
        filename = Path(filename)
        with filename.open("rb", buffering=0) as raw:
            binary = self._pe.parse(raw, self.resource_only)
        if binary:
            resources_manager = binary.resources_manager
            if not isinstance(resources_manager, self.lief_errors):
                resources_manager.manifest = manifest
                with TemporaryDirectory(prefix="cxfreeze-") as tmp_dir:
                    tmp_path = os.path.join(tmp_dir, filename.name)
                    binary.write(tmp_path)
                    shutil.move(tmp_path, filename)


class ELFParser(Parser):
    """`ELFParser` is based on the `patchelf` and `ldd` tools."""

    def __init__(
        self,
        path: list[str],
        bin_path_includes: list[str],
        silent: int,
        warnings: dict[str, bool],
    ) -> None:
        super().__init__(path, bin_path_includes, silent, warnings)
        self._patchelf = shutil.which("patchelf")
        self._verify_patchelf()

    def find_library(
        self, name: str, search_path: list[StrPath] | None = None
    ) -> Path | None:
        library = super().find_library(name, search_path)
        if library is None:
            filename = find_library(name)
            if filename:
                library = super().find_library(filename, search_path)
        return library

    @staticmethod
    def _is_binary(filename: StrPath) -> bool:
        """Check if the executable is an ELF."""
        filename = Path(filename)
        if filename.suffix in NON_ELF_EXT or not filename.is_file():
            return False
        with open(filename, "rb") as binary:
            four_bytes = binary.read(4)
        return bool(four_bytes == MAGIC_ELF)

    is_elf = _is_binary

    def _get_dependent_files_ldd(self, filename: Path) -> set[Path]:
        dependent_files: set[Path] = set()
        split_string = " => "
        dependent_file_index = 1
        args = ("ldd", filename)
        env = os.environ.copy()
        env.pop("LD_PRELOAD", None)
        process = subprocess.run(
            args, check=False, capture_output=True, encoding="utf_8", env=env
        )
        for line in process.stdout.splitlines():
            parts = line.expandtabs().strip().split(split_string)
            if len(parts) != 2:
                continue
            partname = parts[dependent_file_index].strip()
            if partname == filename.name:
                continue
            if partname in ("not found", "(file not found)"):
                partname = Path(parts[0])
                search_path = [*self.search_path, filename.parent]
                for bin_path in search_path:
                    name = partname.name
                    partname = Path(bin_path, name)
                    if partname.is_file():
                        dependent_files.add(partname)
                        if name in self._warnings:
                            self._warnings[name] = False
                        break
                if not partname.is_file():
                    name = partname.name
                    if name not in self._warnings:
                        self._warnings[name] = True
                continue
            if partname.startswith("("):
                continue
            pos = partname.find(" (")
            if pos >= 0:
                partname = partname[:pos].strip()
            if partname:
                dependent_files.add(Path(partname))
        if process.returncode and self._silent < 3:
            print("WARNING:", *args, "returns:")
            print(process.stderr, end="")
        return dependent_files

    def _get_dependent_files_patchelf(self, filename: Path) -> set[Path]:
        libraries: list[str] = self.get_needed(filename)
        rpath: list[Path] = self.get_resolved_rpath(filename) or []

        dependent_files: set[Path] = set()
        search_path = cast(
            "list[StrPath]", rpath + self.search_path + [filename.parent]
        )
        for name in libraries:
            library = self.find_library(name, search_path)
            if library:
                dependent_files.add(library)
            elif name not in self._warnings:
                self._warnings[name] = True
        return dependent_files

    if LDD_DISABLED:
        _get_dependent_files = _get_dependent_files_patchelf
    else:
        _get_dependent_files = _get_dependent_files_ldd

    def get_needed(self, filename: StrPath) -> list[str]:
        """Gets the DT_NEEDED entry of the dynamic table."""
        libraries: list[str] = []
        with suppress(subprocess.CalledProcessError):
            libraries.extend(
                self.run_patchelf(["--print-needed", filename]).split()
            )
        return libraries

    def get_resolved_rpath(self, filename: StrPath) -> list[Path] | None:
        """Gets the resolved rpath of the executable."""
        rpath = self.get_rpath(filename)
        if rpath:
            origin = Path(filename).parent.as_posix()
            rpath_list = rpath.replace("$ORIGIN", origin).split(":")
            return [Path(p).resolve() for p in rpath_list]
        return None

    def get_rpath(self, filename: StrPath) -> str:
        """Gets the rpath of the executable."""
        with suppress(subprocess.CalledProcessError):
            return self.run_patchelf(["--print-rpath", filename]).strip()
        return ""

    def replace_needed(
        self, filename: StrPath, so_name: str, new_so_name: str
    ) -> None:
        """Replace DT_NEEDED entry in the dynamic table."""
        self._set_write_mode(filename)
        self.run_patchelf(["--replace-needed", so_name, new_so_name, filename])

    def set_rpath(self, filename: StrPath, rpath: str) -> None:
        """Sets the rpath of the executable."""
        self._set_write_mode(filename)
        rpath_list = rpath.split(":")
        for i, rp in enumerate(rpath_list):
            if rp == "$ORIGIN/.":
                rpath_list[i] = "$ORIGIN"
        rpath = ":".join(rpath_list)
        if rpath == self.get_rpath(filename):
            return
        try:
            self.run_patchelf(["--set-rpath", rpath, filename])
        except subprocess.CalledProcessError:
            self.run_patchelf(["--remove-rpath", filename])
            self.run_patchelf(["--add-rpath", rpath, filename])

    def set_soname(self, filename: StrPath, new_so_name: str) -> None:
        """Sets DT_SONAME entry in the dynamic table."""
        self._set_write_mode(filename)
        self.run_patchelf(["--set-soname", new_so_name, filename])

    def run_patchelf(self, args: Sequence[StrPath]) -> str:
        cmd = list(map(str, [self._patchelf, *args]))
        process = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )
        if self._silent < 1:
            print("patchelf", *args, "returns:", repr(process.stdout))
            if process.stderr:
                print("patchelf errors:", repr(process.stderr))
        return process.stdout

    @staticmethod
    def _set_write_mode(filename: StrPath) -> None:
        filename = Path(filename)
        mode = filename.stat().st_mode
        if mode & stat.S_IWUSR == 0:
            filename.chmod(mode | stat.S_IWUSR)

    def _verify_patchelf(self) -> None:
        """Looks for the ``patchelf`` external binary in the PATH.

        Checks for the required version, and throws an exception if a proper
        version can't be found. Otherwise, silence is golden.
        """
        if not self._patchelf:
            msg = "Cannot find required utility `patchelf` in PATH"
            raise PlatformError(msg)
        try:
            version = self.run_patchelf(["--version"])
        except subprocess.CalledProcessError:
            msg = "Could not call `patchelf` binary"
            raise PlatformError(msg) from None

        mobj = re.match(r"patchelf\s+(\d+(.\d+)?)", version)
        if mobj:
            version = mobj.group(1)
            if tuple(map(int, version.split("."))) >= (0, 14):
                return
        msg = f"patchelf {version} found. cx_Freeze requires patchelf >= 0.14."
        raise ValueError(msg)
