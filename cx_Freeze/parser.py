"""
Implements `Parser` interface to create an abstraction to parse binary files.
"""

from abc import ABC, abstractmethod
import os
from pathlib import Path
import re
import shutil
import stat
from subprocess import check_call, check_output, run, CalledProcessError, PIPE
import sys
from typing import Any, Dict, List, Set, Union

from .common import TemporaryPath

try:
    import lief
except ImportError:
    lief = None
else:
    lief.logging.set_level(lief.logging.LOGGING_LEVEL.ERROR)

try:
    from cx_Freeze import util
except ImportError:
    util = None

PE_EXT = (".exe", ".dll", ".pyd")
MAGIC_ELF = b"\x7fELF"
NON_ELF_EXT = ".a:.c:.h:.py:.pyc:.pyi:.pyx:.pxd:.txt:.html:.xml".split(":")
NON_ELF_EXT += ".png:.jpg:.gif:.jar:.json".split(":")

# The default is to use lief if it is installed.
# To disable the experimental feature in Windows:
# set CX_FREEZE_BIND=imagehlp
LIEF_ENABLED = os.environ.get("CX_FREEZE_BIND", "lief") == "lief" and lief


class Parser(ABC):
    """`Parser` interface."""

    def __init__(self, silent: int = 0) -> None:
        self.dependent_files: Dict[Path, Set[Path]] = {}
        self._silent: int = silent

    @abstractmethod
    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        """Return the file's dependencies using platform-specific tools (the
        imagehlp library on Windows, otool on Mac OS X and ldd on Linux);
        limit this list by the exclusion lists as needed.
        (Implemented separately for each platform.)"""


class PEParser(Parser):
    """`PEParser` is based on the `lief` package. The use of LIEF is
    experimental. If it is not installed or disabled use the old friend
    `cx_Freeze.util` extension module."""

    def is_PE(self, path: Union[str, Path]) -> bool:
        """Determines whether the file is a PE file."""
        if isinstance(path, str):
            path = Path(path)
        return path.suffix.lower().endswith(PE_EXT) and path.is_file()

    def _get_dependent_files_lief(self, path: Path) -> Set[Path]:
        dependent_files: Set[Path] = set()
        orig_path = os.environ["PATH"]
        with path.open("rb", buffering=0) as raw:
            binary = lief.PE.parse(raw, path.name)
        if binary and binary.has_imports:
            search_path = sys.path + orig_path.split(os.pathsep)
            for library in binary.imports:
                for directory in search_path:
                    library_path = Path(directory, library.name)
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

    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        if isinstance(path, str):
            path = Path(path)
        try:
            return self.dependent_files[path]
        except KeyError:
            pass
        if not self.is_PE(path):
            return set()
        dependent_files: Set[Path]
        if LIEF_ENABLED:
            dependent_files = self._get_dependent_files_lief(path)
        else:
            dependent_files = self._get_dependent_files_imagehlp(path)
        self.dependent_files[path] = dependent_files
        return dependent_files

    def read_manifest(self, path: Union[str, Path]) -> str:
        if lief is None:
            raise RuntimeError("lief is not installed")
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
        if lief is None:
            raise RuntimeError("lief is not installed")
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
                builder.write(str(tmp_path))
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

    def is_ELF(self, path: Union[str, Path]) -> bool:
        if isinstance(path, str):
            path = Path(path)
        if (
            path.suffix in NON_ELF_EXT
            or path.is_symlink()
            or not path.is_file()
        ):
            return False
        with open(path, "rb") as fp:
            four_bytes = fp.read(4)
        return bool(four_bytes == MAGIC_ELF)

    def get_dependent_files(self, path: Union[str, Path]) -> Set[Path]:
        if isinstance(path, str):
            path = Path(path)
        try:
            return self.dependent_files[path]
        except KeyError:
            pass
        dependent_files: Set[Path] = set()
        if not self.is_ELF(path) or not os.access(path, os.X_OK):
            return dependent_files
        split_string = " => "
        dependent_file_index = 1
        args = ("ldd", path)
        process = run(args, encoding="utf-8", stdout=PIPE, stderr=PIPE)
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
        args = ["patchelf", "--print-rpath", filename]
        try:
            rpath = check_output(args, encoding="utf-8").strip()
        except CalledProcessError:
            rpath = ""
        return rpath

    def replace_needed(
        self, filename: Union[str, Path], so_name: str, new_so_name: str
    ) -> None:
        self._set_write_mode(filename)
        args = ["patchelf", "--replace-needed", so_name, new_so_name, filename]
        check_call(args)

    def set_rpath(self, filename: Union[str, Path], rpath: str) -> None:
        self._set_write_mode(filename)
        args = ["patchelf", "--remove-rpath", filename]
        check_call(args)
        args = ["patchelf", "--force-rpath", "--set-rpath", rpath, filename]
        check_call(args)

    def set_soname(self, filename: Union[str, Path], new_so_name: str) -> None:
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
        f"patchelf {version} found. cx-freeze requires patchelf >= 0.12."
    )
