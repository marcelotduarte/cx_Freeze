"""The core class for freezing scripts into executables."""

import marshal
import os
import shutil
import stat
import struct
import sys
import sysconfig
import time
from abc import abstractmethod
from importlib.util import MAGIC_NUMBER
from pathlib import Path
from typing import List, Optional, Set, Tuple, Union
from zipfile import ZIP_DEFLATED, ZIP_STORED, PyZipFile, ZipInfo

from ._compat import cached_property
from .common import (
    IncludesList,
    InternalIncludesList,
    get_resource_file_path,
    process_path_specs,
)
from .dist import DistributionMetadata
from .exception import ConfigError
from .executable import Executable
from .finder import ModuleFinder
from .module import ConstantsModule, Module
from .parser import ELFParser, Parser, PEParser

DARWIN = sys.platform == "darwin"
MINGW = sysconfig.get_platform().startswith("mingw")
WIN32 = sys.platform == "win32"

if WIN32:
    from . import winmsvcr
    from .winversioninfo import VersionInfo

    try:
        from .util import AddIcon, GetSystemDir, GetWindowsDir, UpdateCheckSum
    except ImportError:
        pass
elif DARWIN:
    from .darwintools import DarwinFile, DarwinFileTracker, MachOReference

__all__ = ["ConfigError", "ConstantsModule", "Executable", "Freezer"]


class Freezer:
    def __new__(cls, *args, **kwargs):
        # create instance of appropriate sub-class, depending on the platform.
        instance: Freezer
        if WIN32:
            instance = super().__new__(WinFreezer)
        elif DARWIN:
            instance = super().__new__(DarwinFreezer)
        else:  # assume any other platform would be handled by LinuxFreezer
            instance = super().__new__(LinuxFreezer)
        return instance

    def __init__(
        self,
        executables: List[Executable],
        constantsModule: Optional[ConstantsModule] = None,
        includes: Optional[List[str]] = None,
        excludes: Optional[List[str]] = None,
        packages: Optional[List[str]] = None,
        replacePaths: Optional[List[str]] = None,
        compress: bool = True,
        optimizeFlag: int = 0,
        path: Optional[List[str]] = None,
        targetDir: Optional[Union[str, Path]] = None,
        binIncludes: Optional[List[str]] = None,
        binExcludes: Optional[List[str]] = None,
        binPathIncludes: Optional[List[str]] = None,
        binPathExcludes: Optional[List[str]] = None,
        includeFiles: Optional[IncludesList] = None,
        zipIncludes: Optional[IncludesList] = None,
        silent: Union[bool, int] = 0,
        metadata: Optional[DistributionMetadata] = None,
        includeMSVCR: bool = False,
        zipIncludePackages: Optional[List[str]] = None,
        zipExcludePackages: Optional[List[str]] = None,
    ):
        self.executables: List[Executable] = list(executables)
        if constantsModule is None:
            constantsModule = ConstantsModule()
        self.constants_module: ConstantsModule = constantsModule
        self.includes: List[str] = list(includes or [])
        self.excludes: List[str] = list(excludes or [])
        self.packages: Set[str] = set(packages or [])
        self.replacePaths: List[str] = list(replacePaths or [])
        self.compress = True if compress is None else compress
        self.optimize_flag: int = optimizeFlag
        self.path: Optional[List[str]] = path
        self.include_msvcr: bool = includeMSVCR
        self.targetdir = targetDir
        self.bin_includes: Optional[List[str]] = binIncludes
        self.bin_excludes: Optional[List[str]] = binExcludes
        self.bin_path_includes: Optional[List[str]] = binPathIncludes
        self.bin_path_excludes: Optional[List[str]] = binPathExcludes
        self.include_files: InternalIncludesList = process_path_specs(
            includeFiles
        )
        self.zip_includes: InternalIncludesList = process_path_specs(
            zipIncludes
        )
        if isinstance(silent, bool):
            if silent:
                self.silent = 1
            else:
                self.silent = 0
        else:
            self.silent = silent
        self.metadata: Optional[DistributionMetadata] = metadata
        self.zipIncludePackages: Optional[List[str]] = zipIncludePackages
        self.zipExcludePackages: Optional[List[str]] = zipExcludePackages
        self._verify_configuration()

    @property
    def targetdir(self) -> Path:
        return self._targetdir

    @targetdir.setter
    def targetdir(self, path: Optional[Union[str, Path]]):
        if path is None:
            platform = sysconfig.get_platform()
            python_version = sysconfig.get_python_version()
            path = f"build/exe.{platform}-{python_version}"
        path = Path(path).resolve()
        if path.is_dir():
            # starts in a clean directory

            def onerror(*args):
                raise ConfigError("the build directory cannot be cleaned")

            shutil.rmtree(path, onerror=onerror)

        self._targetdir: Path = path

    def _add_resources(self, exe: Executable) -> None:
        """Add resources for an executable, platform dependent."""
        # Copy icon into application. (Overridden on Windows)
        if exe.icon is None:
            return
        target_icon = self.targetdir / exe.icon.name
        self._copy_file(exe.icon, target_icon, copy_dependent_files=False)

    def _copy_file(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
    ):
        if not self._should_copy_file(source):
            return

        # handle pre-copy tasks, normally on the target path
        source, target = self._pre_copy_hook(source, target)

        if target in self.files_copied:
            return
        if source == target:
            return
        self._create_directory(target.parent)
        if self.silent < 1:
            print(f"copying {source} -> {target}")
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        if include_mode:
            shutil.copymode(source, target)
        self.files_copied.add(target)

        # handle post-copy tasks, including copying dependencies
        self._post_copy_hook(
            source, target, copy_dependent_files, include_mode
        )

    def _copy_package_data(self, module: Module, target_dir: Path):
        """Copy any non-Python files to the target directory."""
        ignore_patterns = ("__pycache__", "*.py", "*.pyc", "*.pyo")

        def copy_tree(source_dir: Path, target_dir: Path, excludes: Set[str]):
            self._create_directory(target_dir)
            for source in source_dir.iterdir():
                if any(filter(source.match, ignore_patterns)):
                    continue
                source_name = source.name
                if source_name in excludes:
                    continue
                target = target_dir / source_name
                if source.is_dir():
                    source_subdir = source_dir / source_name
                    excludes_subdir = {
                        ".".join(m.split(".")[1:])
                        for m in excludes
                        if m.split(".")[0] == source_name
                    }
                    copy_tree(source_subdir, target, excludes_subdir)
                else:
                    self._copy_file(source, target, copy_dependent_files=True)

        source_dir = module.file.parent
        module_name = module.name
        if self.silent < 1:
            print(f"copying data from package {module_name}...")
        # do not copy the subfolders which belong to excluded modules
        excludes = {
            ".".join(m.split(".")[1:])
            for m in self.finder.excludes.keys()
            if m.split(".")[0] == module_name
        }
        copy_tree(source_dir, target_dir, excludes)

    @abstractmethod
    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths."""

    @abstractmethod
    def _post_copy_hook(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
    ):
        """Post-copy task."""

    def _create_directory(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)
        if not path.is_dir():
            if self.silent < 1:
                print(f"creating directory {path}")
            path.mkdir(parents=True, exist_ok=True)

    def _freeze_executable(self, exe: Executable) -> None:
        finder: ModuleFinder = self.finder
        finder.include_file_as_module(exe.main_script, exe.main_module_name)
        finder.include_file_as_module(exe.init_script, exe.init_module_name)
        finder.include_file_as_module(
            get_resource_file_path("initscripts", "__startup__", ".py")
        )

        # Ensure the copy of default python libraries
        dependent_files = self.get_dependent_files(exe.base)
        if not dependent_files:
            dependent_files = self.get_dependent_files(Path(sys.executable))
        python_libs = self._default_bin_includes()
        for path in self._default_bin_path_includes():
            for file in python_libs:
                dependent_file = Path(path, file)
                if dependent_file.is_file():
                    dependent_files.add(dependent_file)
                    break
        if not dependent_files:
            if self.silent < 3:
                print("WARNING: shared libraries not found:", python_libs)

        # Search the C runtimes, using the directory of the python libraries
        # and the directories of the base executable
        self._platform_add_extra_dependencies(dependent_files)

        for source in dependent_files:
            # Store dynamic libraries in appropriate location for platform.
            self._copy_top_dependency(source)
            # Once copied, it should be deleted from the list to ensure
            # it will not be copied again.
            name = Path(source.name)
            if name in self.bin_includes:
                self.bin_includes.remove(name)
                self.bin_excludes.append(name)

        target_path = self.targetdir / exe.target_name
        self._copy_file(
            exe.base,
            target_path,
            copy_dependent_files=False,
            include_mode=True,
        )
        if not os.access(target_path, os.W_OK):
            mode = target_path.stat().st_mode
            target_path.chmod(mode | stat.S_IWUSR)

        # Add resources like version metadata and icon
        self._add_resources(exe)

    def _platform_add_extra_dependencies(
        self, dependent_files: Set[Path]
    ) -> None:
        """Override with platform specific files to add runtime libraries to
        the list of dependent_files calculated in _freeze_executable."""

    @abstractmethod
    def _copy_top_dependency(self, source: Path) -> None:
        """Called for copying the top dependencies in _freeze_executable."""

    def _default_bin_excludes(self) -> List[str]:
        """Return the file names of libraries that need not be included because
        they would normally be expected to be found on the target system or
        because they are part of a package which requires independent
        installation anyway.
        (overridden on Windows)"""
        return ["libclntsh.so", "libwtc9.so", "ldd"]

    def _default_bin_includes(self) -> List[str]:
        """Return the file names of libraries which must be included for the
        frozen executable to work.
        (overriden on Windows)"""
        python_shared_libs = []
        # Miniconda python 3.6-3.9 linux returns a static library to indicate
        # the usage of libpython-static (a shared library is not used).
        name = sysconfig.get_config_var("INSTSONAME")
        if name and not name.endswith(".a"):
            python_shared_libs.append(self._remove_version_numbers(name))
        return python_shared_libs

    @abstractmethod
    def _default_bin_path_excludes(self) -> List[str]:
        """Return the paths of directories which contain files that should not
        be included, generally because they contain standard system
        libraries."""

    @abstractmethod
    def _default_bin_path_includes(self) -> List[str]:
        """Return the paths of directories which contain files that should
        be included."""

    def _get_module_finder(self) -> ModuleFinder:
        finder = ModuleFinder(
            self.include_files,
            self.excludes,
            self.path,
            self.replacePaths,
            self.zipIncludeAllPackages,
            self.zipExcludePackages,
            self.zipIncludePackages,
            self.constants_module,
            self.zip_includes,
        )
        finder.optimize_flag = self.optimize_flag
        for name in self.includes:
            finder.include_module(name)
        for name in self.packages:
            finder.include_package(name)
        return finder

    def _post_freeze_hook(self) -> None:
        """Platform-specific post-Freeze work."""

    def _print_report(self, filename: Path, modules: List[Module]) -> None:
        print(f"writing zip file {filename}\n")
        print("  {:<25} {}".format("Name", "File"))
        print("  {:<25} {}".format("----", "----"))
        for module in modules:
            if module.path:
                print("P", end="")
            else:
                print("m", end="")
            print(f" {module.name:<25} {module.file or ''}")

    @staticmethod
    def _remove_version_numbers(filename: str) -> str:
        tweaked = False
        parts = filename.split(".")
        while parts:
            if not parts[-1].isdigit():
                break
            parts.pop(-1)
            tweaked = True
        if tweaked:
            filename = ".".join(parts)
        return filename

    def _should_copy_file(self, path: Path) -> bool:
        """Return true if the file should be copied to the target machine.
        This is done by checking the bin_path_includes, bin_path_excludes,
        bin_includes and bin_excludes configuration variables using first
        the full file name, then just the base file name, then the file name
        without any version numbers.

        Files are included unless specifically excluded but inclusions take
        precedence over exclusions."""

        # check the full path
        if path in self.bin_includes:
            return True
        if path in self.bin_excludes:
            return False

        # check the file name by itself (with any included version numbers)
        filename = Path(path.name)
        if filename in self.bin_includes:
            return True
        if filename in self.bin_excludes:
            return False

        # check the file name by itself (version numbers removed)
        filename = Path(self._remove_version_numbers(path.name))
        if filename in self.bin_includes:
            return True
        if filename in self.bin_excludes:
            return False

        # check the path for inclusion/exclusion
        dirname = path.parent
        for binpath in self.bin_path_includes:
            try:
                dirname.relative_to(binpath)
            except ValueError:
                pass
            else:
                return True
        for binpath in self.bin_path_excludes:
            try:
                dirname.relative_to(binpath)
            except ValueError:
                pass
            else:
                return False

        return True

    def _verify_configuration(self) -> None:
        """Verify and normalize names and paths. Raises ConfigError on
        failure."""
        filenames = list(self.bin_includes or [])
        filenames += self._default_bin_includes()
        self.bin_includes = [Path(name) for name in filenames]

        filenames = list(self.bin_excludes or [])
        filenames += self._default_bin_excludes()
        self.bin_excludes = [Path(name) for name in filenames]

        paths = list(self.bin_path_includes or [])
        paths += self._default_bin_path_includes()
        self.bin_path_includes = [
            name for name in paths if Path(name).is_dir()
        ]

        paths = list(self.bin_path_excludes or [])
        paths += self._default_bin_path_excludes()
        self.bin_path_excludes = [
            name for name in paths if Path(name).is_dir()
        ]

        if self.zipIncludePackages is None and self.zipExcludePackages is None:
            self.zipIncludePackages = []
            self.zipExcludePackages = ["*"]
        else:
            self.zipIncludePackages = list(self.zipIncludePackages or [])
            self.zipExcludePackages = list(self.zipExcludePackages or [])
        self.zipExcludeAllPackages = "*" in self.zipExcludePackages
        self.zipIncludeAllPackages = "*" in self.zipIncludePackages
        if self.zipExcludeAllPackages and self.zipIncludeAllPackages:
            raise ConfigError(
                "all packages cannot be included and excluded "
                "from the zip file at the same time"
            )
        for name in self.zipIncludePackages:
            if name in self.zipExcludePackages:
                raise ConfigError(
                    f"package {name!r} cannot be both included and "
                    "excluded from zip file"
                )

    def _write_modules(self, filename: Path, finder: ModuleFinder):
        finder.include_file_as_module(
            *self.constants_module.create(finder.modules)
        )

        modules = [m for m in finder.modules if m.name not in finder.excludes]
        modules.sort(key=lambda m: m.name)

        if self.silent < 1:
            self._print_report(filename, modules)
        if self.silent < 2:
            finder.report_missing_modules()

        target_lib_dir = filename.parent
        self._create_directory(target_lib_dir)

        # Prepare zip file
        compress_type = ZIP_DEFLATED if self.compress else ZIP_STORED
        with PyZipFile(filename, "w", compress_type) as outfile:

            files_to_copy: List[Tuple[Module, Path]] = []

            for module in modules:

                # determine if the module should be written to the file system;
                # a number of packages make the assumption that files that they
                # require will be found in a location relative to where they
                # are located on disk; these packages will fail with strange
                # errors when they are written to a zip file instead
                include_in_file_system = module.in_file_system
                mod_name = module.name
                mod_name_parts = mod_name.split(".")

                # if the module refers to a package, check to see if this
                # package should be written to the file system
                if (
                    include_in_file_system >= 1
                    and module.path is not None
                    and module.file is not None
                ):
                    parts = mod_name_parts
                    target_package_dir = target_lib_dir.joinpath(*parts)
                    if include_in_file_system == 2:
                        # a few packages are optimized on the hooks,
                        # so for now create the directory for this package
                        self._create_directory(target_package_dir)

                    elif not target_package_dir.exists():
                        # whether the package and its data will be written to
                        # the file system, any non-Python files are copied at
                        # this point if the target directory does not already
                        # exist
                        self._copy_package_data(module, target_package_dir)

                # if an extension module is found in a package that is to be
                # included in a zip file, copy the actual file to the build
                # directory because shared libraries cannot be loaded from a
                # zip file
                if (
                    module.code is None
                    and module.file is not None
                    and include_in_file_system == 0
                ):
                    parts = mod_name_parts[:-1]
                    parts.append(module.file.name)
                    target = target_lib_dir / ".".join(parts)
                    files_to_copy.append((module, target))

                # starting with Python 3.3 the pyc file format contains the
                # source size; it is not actually used for anything except
                # determining if the file is up to date so we can safely set
                # this value to zero
                if module.code is not None:
                    if module.file is not None and module.file.exists():
                        st = module.file.stat()
                        mtime = int(st.st_mtime)
                        size = st.st_size & 0xFFFFFFFF
                    else:
                        mtime = int(time.time())
                        size = 0
                    header = MAGIC_NUMBER + struct.pack("<iii", 0, mtime, size)
                    if sys.version_info[:2] < (3, 7):
                        header = MAGIC_NUMBER + struct.pack("<ii", mtime, size)
                    data = header + marshal.dumps(module.code)

                # if the module should be written to the file system, do so
                if include_in_file_system >= 1 and module.file is not None:
                    parts = mod_name_parts.copy()
                    if module.code is None:
                        parts.pop()
                        parts.append(module.file.name)
                        target_name = target_lib_dir.joinpath(*parts)
                        self._copy_file(
                            module.file,
                            target_name,
                            copy_dependent_files=True,
                        )
                    else:
                        if module.path is not None:
                            parts.append("__init__")
                        target_name = target_lib_dir.joinpath(*parts)
                        target_name = target_name.with_suffix(".pyc")
                        target_name.write_bytes(data)

                # otherwise, write to the zip file
                elif module.code is not None:
                    zipTime = time.localtime(mtime)[:6]
                    target_name = "/".join(mod_name_parts)
                    if module.path:
                        target_name += "/__init__"
                    zinfo = ZipInfo(target_name + ".pyc", zipTime)
                    zinfo.compress_type = compress_type
                    outfile.writestr(zinfo, data)

            # put the distribution files metadata in the zip file
            dist_cachedir = None
            for module in modules:
                if module.distribution:
                    dist_cachedir = module.distribution.locate_file(".")
                    break
            if dist_cachedir is not None:
                pos = len(dist_cachedir.as_posix()) + 1
                for name in dist_cachedir.rglob("*"):
                    if name.is_dir():
                        continue
                    outfile.write(name, name.as_posix()[pos:])

            # write any files to the zip file that were requested specially
            for source_path, target_path in finder.zip_includes:
                if source_path.is_dir():
                    pos = len(source_path.as_posix()) + 1
                    for source_filename in source_path.rglob("*"):
                        if source_filename.is_dir():
                            continue
                        target = target_path / source_filename.as_posix()[pos:]
                        outfile.write(source_filename, target)
                else:
                    outfile.write(source_path, target_path.as_posix())

        # Copy Python extension modules from the list built above.
        origPath = os.environ["PATH"]
        for module, target in files_to_copy:
            try:
                if module.parent is not None:
                    path = os.pathsep.join(
                        [origPath] + list(map(os.fspath, module.parent.path))
                    )
                    os.environ["PATH"] = path
                self._copy_file(module.file, target, copy_dependent_files=True)
            finally:
                os.environ["PATH"] = origPath

    def Freeze(self):
        self.files_copied: Set[Path] = set()

        finder: ModuleFinder = self._get_module_finder()
        self.finder: ModuleFinder = finder

        # Add the executables to target
        for executable in self.executables:
            self._freeze_executable(executable)

        # Write the modules
        targetdir = self.targetdir
        library_zip = targetdir / "lib" / "library.zip"
        self._write_modules(library_zip, finder)

        excluded_dependent_files = self.finder.excluded_dependent_files
        for source_path, target_path in finder.included_files:
            copy_dependent_files = source_path not in excluded_dependent_files
            if source_path.is_dir():
                # Copy directories by recursing into them.
                # Can't use shutil.copytree because we may need dependencies
                target_base = targetdir / target_path
                for name in source_path.rglob("*"):
                    if name.is_dir():
                        continue
                    if ".svn" in name.parents:
                        continue
                    if "CVS" in name.parents:
                        continue
                    fulltarget = target_base / name.relative_to(source_path)
                    self._create_directory(fulltarget.parent)
                    self._copy_file(name, fulltarget, copy_dependent_files)
            else:
                # Copy regular files.
                fulltarget = targetdir / target_path
                self._copy_file(source_path, fulltarget, copy_dependent_files)

        # do any platform-specific post-Freeze work
        self._post_freeze_hook()


class WinFreezer(Freezer, PEParser):
    def __init__(self, *args, **kwargs):
        Freezer.__init__(self, *args, **kwargs)
        PEParser.__init__(self, self.silent)

        # deal with C-runtime files
        self.runtime_files: Set[str] = set()
        self.runtime_files_to_dup: Set[str] = set()
        self._set_runtime_files()

    def _add_resources(self, exe: Executable) -> None:
        target_path: Path = self.targetdir / exe.target_name

        # Change the manifest
        manifest: Optional[str] = exe.manifest
        if manifest is not None or exe.uac_admin:
            if self.silent < 1:
                print(f"writing manifest -> {target_path}")
            try:
                if exe.uac_admin:
                    manifest = manifest or self.read_manifest(target_path)
                    manifest = manifest.replace(
                        "asInvoker", "requireAdministrator"
                    )
                self.write_manifest(target_path, manifest)
            except FileNotFoundError as exc:
                if self.silent < 3:
                    print("WARNING:", exc)
            except RuntimeError as exc:
                if self.silent < 3:
                    print(f"WARNING: error parsing {target_path}:", exc)

        # Add version resource
        if self.metadata is not None:
            warning_msg = "WARNING: unable to create version resource:"
            if not self.metadata.version:
                if self.silent < 3:
                    print(warning_msg, "version must be specified")
            else:
                version = VersionInfo(
                    self.metadata.version,
                    comments=self.metadata.long_description,
                    description=self.metadata.description,
                    company=self.metadata.author,
                    product=self.metadata.name,
                    copyright=exe.copyright,
                    trademarks=exe.trademarks,
                    verbose=bool(self.silent < 1),
                )
                try:
                    version.stamp(target_path)
                except (FileNotFoundError, RuntimeError) as exc:
                    if self.silent < 3:
                        print(warning_msg, exc)

        # Add icon
        if exe.icon is not None:
            try:
                AddIcon(target_path, exe.icon)
            except MemoryError:
                if self.silent < 3:
                    print("WARNING: MemoryError")
            except RuntimeError as exc:
                if self.silent < 3:
                    print("WARNING:", exc)
            except OSError as exc:
                if "\\WindowsApps\\" in sys.base_prefix:
                    if self.silent < 3:
                        print("WARNING:", exc)
                        print(
                            "WARNING: Because of restrictions on Microsoft "
                            "Store apps, Python scripts may not have full "
                            "write access to built executable. "
                            "You will need to install the full installer."
                        )
                else:
                    raise

        # Update the PE checksum (or fix it in case it is zero)
        try:
            UpdateCheckSum(target_path)
        except MemoryError:
            if self.silent < 3:
                print("WARNING: MemoryError")
        except (RuntimeError, OSError) as exc:
            if self.silent < 3:
                print("WARNING:", exc)

    def _copy_top_dependency(self, source: Path) -> None:
        """Called for copying certain top dependencies in _freeze_executable.
        We need this as a separate method so that it can be overridden on
        Darwin and Windows."""
        # top dependencies go into build root directory on windows
        # the C runtimes are handled in _copy_file/_pre_copy_hook
        # on msys2 libpython depends on libgcc_s_seh and libwinpthread dlls.
        if MINGW:
            dependent_files = self.get_dependent_files(source)
            for file in dependent_files:
                if self._should_copy_file(file):
                    self._copy_top_dependency(file)
            copy_dependent_files = False  # already copied
        else:
            copy_dependent_files = True
        target = self.targetdir / source.name
        self._copy_file(
            source, target, copy_dependent_files, include_mode=True
        )

    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths. Also, adjust the target of
        C runtime libraries and triggers an additional copy for files in
        self.runtime_files_to_dup."""

        # fix the target path for C runtime files
        norm_target_name = target.name.lower()
        if norm_target_name in self.runtime_files:
            target = self.targetdir / "lib" / norm_target_name

            # vcruntime140.dll must be in the root and in the lib directory
            if norm_target_name in self.runtime_files_to_dup:
                self.runtime_files_to_dup.remove(norm_target_name)
                self._copy_file(source, target, copy_dependent_files=False)
                self.files_copied.remove(target)
                target = self.targetdir / norm_target_name
        return source, target

    def _post_copy_hook(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
    ) -> None:
        if (
            copy_dependent_files
            and source not in self.finder.excluded_dependent_files
        ):

            library_dir = self.targetdir / "lib"
            source_dir = source.parent
            target_dir = target.parent
            platform_bin_path = self._platform_bin_path
            for dependent_source in self.get_dependent_files(source):
                if not self._should_copy_file(dependent_source):
                    continue
                # put the dependency in the target_dir (except C runtime)
                dependent_srcdir = dependent_source.parent
                dependent_name = dependent_source.name
                try:
                    # dependency located with source or in a subdirectory
                    relative = dependent_source.relative_to(source_dir)
                    dependent_target = target_dir / relative
                except ValueError:
                    # check if dependency is on default binaries path
                    if dependent_srcdir in platform_bin_path:
                        dependent_target = library_dir / dependent_name
                    else:
                        # check if dependency is located in a upper level
                        try:
                            relative = source_dir.relative_to(dependent_srcdir)
                            # fix the target_dir - go to the previous level
                            parts = target_dir.parts[: -len(relative.parts)]
                            dependent_target = Path(*parts) / dependent_name
                        except ValueError:
                            dependent_target = target_dir / dependent_name
                # check to make sure the dependency is in the correct place
                # because it can be outside of the python subtree
                try:
                    dependent_target.relative_to(library_dir)
                except ValueError:
                    dependent_target = library_dir / dependent_name
                else:
                    _, dependent_target = self._pre_copy_hook(
                        dependent_source, dependent_target
                    )
                    if dependent_target not in self.files_copied:
                        for file in self.files_copied:
                            if file.match(dependent_name):
                                dependent_target = file
                                break
                self._copy_file(
                    dependent_source, dependent_target, copy_dependent_files
                )

    def _default_bin_excludes(self) -> List[str]:
        return ["comctl32.dll", "oci.dll"]

    def _default_bin_includes(self) -> List[str]:
        python_shared_libs: List[str] = []
        if MINGW:
            name = sysconfig.get_config_var("INSTSONAME")
            if name:
                python_shared_libs.append(name.replace(".dll.a", ".dll"))
        else:
            python_shared_libs += [
                "python%s.dll" % sys.version_info[0],
                "python%s%s.dll" % sys.version_info[:2],
            ]
        return python_shared_libs

    def _default_bin_path_excludes(self) -> List[str]:
        systemDir = GetSystemDir()
        windowsDir = GetWindowsDir()
        return [windowsDir, systemDir, os.path.join(windowsDir, "WinSxS")]

    def _default_bin_path_includes(self) -> List[str]:
        paths = {Path(path) for path in sys.path if path}
        paths.update(self._platform_bin_path)
        # return only valid paths
        return [os.fspath(path) for path in paths if path.is_dir()]

    @cached_property
    def _platform_bin_path(self) -> List[Path]:
        # try to find the paths (windows, conda-forge, msys2/mingw)
        paths = set()
        dest_shared = sysconfig.get_config_var("DESTSHARED")  # msys2
        dest_relative = None
        if dest_shared:
            dest_shared = Path(dest_shared)
            paths.add(dest_shared)
            try:
                dest_relative = dest_shared.relative_to(sys.prefix)
            except ValueError:
                pass
        for prefix in [
            sys.base_exec_prefix,
            sys.base_prefix,
            sys.exec_prefix,
            sys.prefix,
        ]:
            prefix = Path(prefix)
            paths.add(prefix / "bin")
            paths.add(prefix / "DLLs")
            paths.add(prefix / "Library/bin")
            if dest_relative:
                paths.add(prefix / dest_relative)
        # return only valid paths
        return [path for path in paths if path.is_dir()]

    def _platform_add_extra_dependencies(
        self, dependent_files: Set[Path]
    ) -> None:
        search_dirs: Set[Path] = set()
        for filename in dependent_files:
            search_dirs.add(filename.parent)
        for filename in self.runtime_files:
            for search_dir in search_dirs:
                filepath = search_dir / filename
                if filepath.exists():
                    dependent_files.add(filepath)

    def _post_freeze_hook(self) -> None:
        target_lib = self.targetdir / "lib"
        # Recursing into directories to search for load order files.
        # Some libraries use delvewheel to patch them.
        for loader_file in target_lib.rglob(".load-order-*"):
            load_order = loader_file.read_text().split()
            load_dir = loader_file.parent
            new_order = [
                f for f in load_order if load_dir.joinpath(f).is_file()
            ]
            if new_order != load_order:
                loader_file.write_text("\n".join(new_order))

    def _set_runtime_files(self) -> None:
        if self.include_msvcr:
            self.runtime_files.update(winmsvcr.FILES)
            self.runtime_files_to_dup.update(winmsvcr.FILES_TO_DUPLICATE)
        else:
            # just put on the exclusion list
            self.bin_excludes.extend([Path(name) for name in winmsvcr.FILES])


class DarwinFreezer(Freezer, Parser):
    def __init__(self, *args, **kwargs):
        Freezer.__init__(self, *args, **kwargs)
        Parser.__init__(self, self.silent)
        self.darwin_tracker: Optional[DarwinFileTracker] = None
        self.darwin_tracker = DarwinFileTracker()

    def _post_freeze_hook(self) -> None:
        self.darwin_tracker.finalizeReferences()

    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths."""
        return source, target

    def _post_copy_hook(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
        reference: Optional["MachOReference"] = None,
    ) -> None:

        # The file was not previously copied, so need to create a
        # DarwinFile file object to represent the file being copied.
        if reference is not None:
            referencing_file = reference.source_file
        else:
            referencing_file = None
        darwin_file = DarwinFile(source, referencing_file)
        darwin_file.setBuildPath(target)
        if reference is not None:
            reference.setTargetFile(darwin_file)

        self.darwin_tracker.recordCopiedFile(target, darwin_file)
        if (
            copy_dependent_files
            and source not in self.finder.excluded_dependent_files
        ):
            # Always copy dependent files on root directory
            # to allow to set relative reference
            targetdir = self.targetdir
            for dependent in self.get_dependent_files(source, darwin_file):
                target = targetdir / dependent.name
                reference = darwin_file.getMachOReferenceForPath(dependent)
                self._copy_file_recursion(
                    dependent,
                    target,
                    copy_dependent_files=True,
                    reference=reference,
                )

    def _copy_file_recursion(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
        reference: Optional["MachOReference"] = None,
    ) -> None:
        """This is essentially the same as Freezer._copy_file, except that it
        also takes a reference parameter. Used when recursing to dependencies
        of a file on Darwin."""
        if not self._should_copy_file(source):
            return

        # handle pre-copy tasks, normally on the target path
        source, target = self._pre_copy_hook(source, target)

        if target in self.files_copied:
            if reference is not None:
                # If file was already copied, and we are following a reference
                # from a DarwinFile, then we need to tell the reference where
                # the file was copied to (the reference can later be updated).
                reference.setTargetFile(
                    self.darwin_tracker.getDarwinFile(source, target)
                )
            return
        if source == target:
            return
        self._create_directory(target.parent)
        if self.silent < 1:
            print(f"copying {source} -> {target}")
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        if include_mode:
            shutil.copymode(source, target)
        self.files_copied.add(target)

        # handle post-copy tasks, including copying dependencies
        self._post_copy_hook(
            source,
            target,
            copy_dependent_files=copy_dependent_files,
            include_mode=include_mode,
            reference=reference,
        )

    def _copy_top_dependency(self, source: Path) -> None:
        """Called for copying certain top dependencies. We need this as a
        separate function so that it can be overridden on Darwin
        (to interact with the DarwinTools system)."""

        target = self.targetdir / "lib" / source.name

        # this recovers the cached MachOReference pointers to the files
        # found by the get_dependent_files calls made previously (if any).
        # If one is found, pass into _copy_file.
        # We need to do this so the file knows what file referenced it,
        # and can therefore calculate the appropriate rpath.
        # (We only cache one reference.)
        cachedReference = self.darwin_tracker.getCachedReferenceTo(source)
        self._copy_file_recursion(
            source,
            target,
            copy_dependent_files=True,
            include_mode=True,
            reference=cachedReference,
        )

    def _default_bin_path_excludes(self):
        return ["/lib", "/usr/lib", "/System/Library/Frameworks"]

    def _default_bin_path_includes(self) -> List[str]:
        return [sysconfig.get_config_var("DESTSHARED")]

    def get_dependent_files(
        self, path: Path, darwinFile: Optional["DarwinFile"] = None
    ) -> Set[Path]:
        try:
            return self.dependent_files[path]
        except KeyError:
            pass

        # if darwinFile is None (which means that get_dependent_files is
        # being called outside of _copy_file -- e.g., one of the
        # preliminary calls in _freeze_executable), create a temporary
        # DarwinFile object for the path, just so we can read its
        # dependencies
        if darwinFile is None:
            darwinFile = DarwinFile(path)
        dependent_files = darwinFile.getDependentFilePaths()

        # cache the MachOReferences to the dependencies, so they can be
        # called up later in _copy_file if copying a dependency without
        # an explicit reference provided (to assist in resolving @rpaths)
        for reference in darwinFile.getMachOReferenceList():
            if reference.isResolved():
                self.darwin_tracker.cacheReferenceTo(
                    reference.resolved_path, reference
                )
        self.dependent_files[path] = dependent_files
        return dependent_files


class LinuxFreezer(Freezer, ELFParser):
    def __init__(self, *args, **kwargs):
        Freezer.__init__(self, *args, **kwargs)
        ELFParser.__init__(self, self.silent)
        self._symlinks: Set[Tuple[Path, str]] = set()

    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths. In addition, it ensures that
        the source of a symbolic link is copied by deferring the creation of
        the link."""
        if source.is_symlink():
            real_source = source.resolve()
            symlink = real_source.name
            real_target = target.with_name(symlink)
            self._symlinks.add((target, symlink))
            return real_source, real_target
        return source, target

    def _post_copy_hook(
        self,
        source: Path,
        target: Path,
        copy_dependent_files: bool,
        include_mode: bool = False,
    ):
        if (
            copy_dependent_files
            and source not in self.finder.excluded_dependent_files
        ):
            library_dir = self.targetdir / "lib"
            source_dir = source.parent
            target_dir = target.parent
            fix_rpath = set()
            for dependent_file in self.get_dependent_files(source):
                if not self._should_copy_file(dependent_file):
                    continue
                try:
                    relative = dependent_file.relative_to(source_dir)
                except ValueError:
                    # put it in the target_dir if not already copied
                    dependent_filename = dependent_file.name
                    dependent_target = target_dir / dependent_filename
                    relative = Path(dependent_filename)
                    if dependent_target not in self.files_copied:
                        for file in self.files_copied:
                            if file.name == dependent_filename:
                                relative = file.relative_to(library_dir)
                                dependent_target = library_dir / relative
                                break
                else:
                    dependent_target = target_dir / relative
                    dependent_target = dependent_target.resolve()
                    try:
                        dependent_target.relative_to(library_dir)
                    except ValueError:
                        parts = list(relative.parts)
                        while parts[0] == os.pardir:
                            parts.pop(0)
                        relative = Path(*parts)
                        dependent_target = library_dir / relative
                dep_libs = os.fspath(relative.parent)
                fix_rpath.add(dep_libs)
                self._copy_file(
                    dependent_file, dependent_target, copy_dependent_files
                )
            if fix_rpath:
                has_rpath = self.get_rpath(target)
                rpath = ":".join(f"$ORIGIN/{r}" for r in fix_rpath)
                if has_rpath != rpath:
                    self.set_rpath(target, rpath)

    def _post_freeze_hook(self):
        target: Path
        symlink: str
        for target, symlink in self._symlinks:
            if self.silent < 1:
                print(f"linking {target} -> {symlink}")
            if not target.exists():
                target.symlink_to(symlink)

    def _copy_top_dependency(self, source: Path) -> None:
        """Called for copying the top dependencies in _freeze_executable."""
        target = self.targetdir / "lib" / source.name
        self._copy_file(
            source, target, copy_dependent_files=True, include_mode=True
        )

    def _default_bin_path_excludes(self) -> List[str]:
        return [
            "/lib",
            "/lib32",
            "/lib64",
            "/usr/lib",
            "/usr/lib32",
            "/usr/lib64",
        ]

    def _default_bin_path_includes(self) -> List[str]:
        # add the stdlib/lib-dynload directory
        destlib = sysconfig.get_config_var("DESTLIB")
        if bool(destlib):
            return [destlib]
        return []
