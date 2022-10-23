"""Implements `Parser` interface to create an abstraction to parse binary
files."""

import os
import re
import shutil
import stat
import sys
from abc import ABC, abstractmethod
from contextlib import suppress
from pathlib import Path
from subprocess import PIPE, CalledProcessError, check_call, check_output, run
from typing import Any, Dict, List, Set, Union

from .common import TemporaryPath

# pylint: disable=c-extension-no-member
if sys.platform == "win32":
    import lief

    lief.logging.set_level(lief.logging.LOGGING_LEVEL.ERROR)

try:
    from cx_Freeze import util
except ImportError:
    util = None

PE_EXT = (".exe", ".dll", ".pyd")
MAGIC_ELF = b"\x7fELF"
NON_ELF_EXT = ".a:.c:.h:.py:.pyc:.pyi:.pyx:.pxd:.txt:.html:.xml".split(":")
NON_ELF_EXT += ".png:.jpg:.gif:.jar:.json".split(":")

# In Windows, to get dependencies, the default is to use lief package,
# but LIEF can be disabled with:
# set CX_FREEZE_BIND=imagehlp
LIEF_DISABLED = os.environ.get("CX_FREEZE_BIND", "") == "imagehlp" and util


class Parser(ABC):
    """`Parser` interface."""

    def __init__(self, silent: int = 0) -> None:
        self.dependent_files: Dict[Path, Set[Path]] = {}
        self._silent: int = silent

    @abstractmethod
    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        """Return the file's dependencies using platform-specific tools
        (lief package or the imagehlp library on Windows, otool on Mac OS X or
        ldd on Linux); limit this list by the exclusion lists as needed.
        (Implemented separately for each platform.)"""


class PEParser(Parser):
    """`PEParser` is based on the `lief` package. If it is disabled,
    use the old friend `cx_Freeze.util` extension module."""

    @staticmethod
    def is_pe(path: Union[str, Path]) -> bool:
        """Determines whether the file is a PE file."""
        if isinstance(path, str):
            path = Path(path)
        return path.suffix.lower().endswith(PE_EXT) and path.is_file()

    def _get_dependent_files_lief(self, path: Path) -> Set[Path]:
        with path.open("rb", buffering=0) as raw:
            binary = lief.PE.parse(raw, path.name)
        if not binary:
            return set()

        libraries: List[str] = []
        if binary.has_imports:
            libraries += binary.libraries
        for delay_import in binary.delay_imports:
            libraries.append(delay_import.name)

        dependent_files: Set[Path] = set()
        orig_path: List[str] = os.environ["PATH"]
        search_path: List[str] = sys.path + orig_path.split(os.pathsep)
        for library_name in libraries:
            for directory in search_path:
                library_path = Path(directory, library_name)
                if library_path.is_file():
                    dependent_files.add(library_path)
                    break
        return dependent_files

    def _get_dependent_files_imagehlp(self, path: Path) -> Set[Path]:
        dependent_files: Set[Path] = set()
        orig_path = os.environ["PATH"]
        os.environ["PATH"] = os.pathsep.join(sys.path) + os.pathsep + orig_path
        try:
            files: List[str] = util.GetDependentFiles(path)
        except util.BindError as exc:
            # Sometimes this gets called when path is not actually
            # a library (See issue 88).
            if self._silent < 3:
                print("WARNING: ignoring error during ", end="")
                print(f"GetDependentFiles({path}):", exc)
        else:
            dependent_files = {Path(dep) for dep in files}
        os.environ["PATH"] = orig_path
        return dependent_files

    if LIEF_DISABLED:
        _get_dependent_files = _get_dependent_files_imagehlp
    else:
        _get_dependent_files = _get_dependent_files_lief

    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        if isinstance(path, str):
            path = Path(path)
        with suppress(KeyError):
            return self.dependent_files[path]
        if not self.is_pe(path):
            return set()

        dependent_files: Set[Path] = self._get_dependent_files(path)
        self.dependent_files[path] = dependent_files
        return dependent_files

    def read_manifest(self, path: Union[str, Path]) -> str:
        """
        :return: the XML schema of the manifest included in the executable
        :rtype: str

        """
        if isinstance(path, str):
            path = Path(path)
        with path.open("rb", buffering=0) as raw:
            binary = lief.PE.parse(raw, path.name)
        try:
            resources_manager = binary.resources_manager
            manifest = resources_manager.manifest
        except lief.exception as exc:
            raise RuntimeError(exc) from None
        return manifest

    def write_manifest(self, path: Union[str, Path], manifest: str) -> None:
        """
        :return: write the XML schema of the manifest into the executable
        :rtype: str

        """
        if isinstance(path, str):
            path = Path(path)
        with path.open("rb", buffering=0) as raw:
            binary = lief.PE.parse(raw, path.name)
        try:
            resources_manager = binary.resources_manager
            resources_manager.manifest = manifest
            builder = lief.PE.Builder(binary)
            builder.build_resources(True)
            builder.build()
            with TemporaryPath("temp.exe") as tmp_path:
                builder.write(os.fspath(tmp_path))
                tmp_path.replace(path)
        except lief.exception as exc:
            raise RuntimeError(exc) from None


class ELFParser(Parser):
    """`ELFParser` is based on the logic around invoking `patchelf` and
    `ldd`."""

    def __init__(self, silent: int = 0) -> None:
        super().__init__(silent)
        self.linker_warnings: Dict[Path, Any] = {}
        _verify_patchelf()

    @staticmethod
    def is_elf(path: Union[str, Path]) -> bool:
        """Check if the executable is an ELF."""
        if isinstance(path, str):
            path = Path(path)
        if (
            path.suffix in NON_ELF_EXT
            or path.is_symlink()
            or not path.is_file()
        ):
            return False
        with open(path, "rb") as binary:
            four_bytes = binary.read(4)
        return bool(four_bytes == MAGIC_ELF)

    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        if isinstance(path, str):
            path = Path(path)
        with suppress(KeyError):
            return self.dependent_files[path]

        dependent_files: Set[Path] = set()
        if not self.is_elf(path) or not os.access(path, os.X_OK):
            return dependent_files

        split_string = " => "
        dependent_file_index = 1
        args = ("ldd", path)
        process = run(
            args, check=False, stdout=PIPE, stderr=PIPE, encoding="utf-8"
        )
        for line in process.stdout.splitlines():
            parts = line.expandtabs().strip().split(split_string)
            if len(parts) != 2:
                continue
            dependent_file = parts[dependent_file_index].strip()
            if dependent_file == path.name:
                continue
            if dependent_file in ("not found", "(file not found)"):
                filename = parts[0]
                if filename not in self.linker_warnings:
                    self.linker_warnings[filename] = None
                    if self._silent < 3:
                        print(f"WARNING: cannot find '{filename}'")
                continue
            if dependent_file.startswith("("):
                continue
            pos = dependent_file.find(" (")
            if pos >= 0:
                dependent_file = dependent_file[:pos].strip()
            if dependent_file:
                dependent_files.add(Path(dependent_file))
        if process.returncode and self._silent < 3:
            print("WARNING:", *args, "returns:")
            print(process.stderr, end="")
        self.dependent_files[path] = dependent_files
        return dependent_files

    def get_rpath(self, filename: Union[str, Path]) -> str:
        """Gets the rpath of the executable."""
        args = ["patchelf", "--print-rpath", filename]
        with suppress(CalledProcessError):
            return check_output(args, encoding="utf-8").strip()
        return ""

    def replace_needed(
        self, filename: Union[str, Path], so_name: str, new_so_name: str
    ) -> None:
        """Replace DT_NEEDED entry in the dynamic table."""
        self._set_write_mode(filename)
        args = ["patchelf", "--replace-needed", so_name, new_so_name, filename]
        check_call(args)

    def set_rpath(self, filename: Union[str, Path], rpath: str) -> None:
        """Sets the rpath of the executable."""
        self._set_write_mode(filename)
        args = ["patchelf", "--remove-rpath", filename]
        check_call(args)
        args = ["patchelf", "--force-rpath", "--set-rpath", rpath, filename]
        check_call(args)

    def set_soname(self, filename: Union[str, Path], new_so_name: str) -> None:
        """Sets DT_SONAME entry in the dynamic table."""
        self._set_write_mode(filename)
        args = ["patchelf", "--set-soname", new_so_name, filename]
        check_call(args)

    @staticmethod
    def _set_write_mode(filename: Union[str, Path]) -> None:
        if isinstance(filename, str):
            filename = Path(filename)
        mode = filename.stat().st_mode
        if mode & stat.S_IWUSR == 0:
            filename.chmod(mode | stat.S_IWUSR)


def _verify_patchelf() -> None:
    """This function looks for the ``patchelf`` external binary in the PATH,
    checks for the required version, and throws an exception if a proper
    version can't be found. Otherwise, silence is golden."""
    if not shutil.which("patchelf"):
        raise ValueError("Cannot find required utility `patchelf` in PATH")
    try:
        version = check_output(["patchelf", "--version"], encoding="utf-8")
    except CalledProcessError:
        raise ValueError("Could not call `patchelf` binary") from None

    mobj = re.match(r"patchelf\s+(\d+(.\d+)?)", version)
    if mobj and tuple(int(x) for x in mobj.group(1).split(".")) >= (0, 12):
        return
    raise ValueError(
        f"patchelf {version} found. cx_Freeze requires patchelf >= 0.12."
    )
