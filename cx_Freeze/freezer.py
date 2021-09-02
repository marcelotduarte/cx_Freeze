"""
Base class for freezing scripts into executables.
"""

from abc import ABC, abstractmethod
from distutils.dist import DistributionMetadata
from importlib.util import MAGIC_NUMBER
import marshal
import os
from pathlib import Path
import shutil
import stat
import struct
import sys
import sysconfig
import time
from typing import Any, Dict, List, Set, Tuple, Optional, Union
import zipfile

from .common import get_resource_file_path, process_path_specs
from .common import IncludesList, InternalIncludesList
from .exception import ConfigError
from .executable import Executable
from .finder import ModuleFinder
from .module import ConstantsModule, Module

DARWIN = sys.platform == "darwin"
MINGW = sysconfig.get_platform().startswith("mingw")
WIN32 = sys.platform == "win32"

if WIN32:
    from . import winmsvcr
    from . import util as winutil
    from .winversioninfo import VersionInfo

    try:
        from win32verstamp import stamp as version_stamp
    except ImportError:
        version_stamp = None
elif DARWIN:
    from .darwintools import DarwinFile, MachOReference, DarwinFileTracker
else:
    from .patchelf import Patchelf

__all__ = ["ConfigError", "ConstantsModule", "Executable", "Freezer"]


class Freezer(ABC):
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
            print(f"copying {source!s} -> {target!s}")
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
        )

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
                print(f"creating directory {path!s}")
            path.mkdir(parents=True, exist_ok=True)

    def _freeze_executable(self, exe: Executable) -> None:
        finder: ModuleFinder = self.finder
        finder.IncludeFile(exe.main_script, exe.main_module_name)
        finder.IncludeFile(exe.init_script, exe.init_module_name)
        finder.IncludeFile(
            get_resource_file_path("initscripts", "__startup__", ".py")
        )

        # Ensure the copy of default python libraries
        dependent_files = self._get_dependent_files(exe.base)
        if not dependent_files:
            dependent_files = self._get_dependent_files(Path(sys.executable))
        python_libs = tuple(self._default_bin_includes())
        python_dirs = {Path(sys.base_exec_prefix), Path(sys.exec_prefix)}
        python_dirs.add(Path(sysconfig.get_config_var("srcdir")))  # Linux
        for file in dependent_files:
            python_dirs.add(file.parent)
        for name in python_libs:
            for python_dir in python_dirs:
                source = python_dir / name
                if source.is_file():
                    dependent_files.add(source)
                    break
        if not dependent_files:
            if self.silent < 3:
                print("WARNING: shared libraries not found:", python_libs)

        # Search the C runtimes, using the directory of the python libraries
        # and the directories of the base executable
        self._platform_add_extra_dependencies(dependent_files)

        for source in dependent_files:
            # Store dynamic libraries in appropriate location for platform
            self._copy_top_dependency(source)

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
        """Called for copying certain top dependencies in _freeze_executable."""

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

    @abstractmethod
    def _get_dependent_files(self, path: Path) -> Set[Path]:
        """Return the file's dependencies using platform-specific tools (the
        imagehlp library on Windows, otool on Mac OS X and ldd on Linux);
        limit this list by the exclusion lists as needed.
        (Implemented separately for each platform.)"""

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
        finder.SetOptimizeFlag(self.optimize_flag)
        for name in self.includes:
            finder.IncludeModule(name)
        for name in self.packages:
            finder.IncludePackage(name)
        return finder

    def _post_freeze_hook(self) -> None:
        """Platform-specific post-Freeze work."""

    def _print_report(self, filename: Path, modules: List[Module]) -> None:
        print(f"writing zip file {filename!s}\n")
        print("  {:<25} {}".format("Name", "File"))
        print("  {:<25} {}".format("----", "----"))
        for module in modules:
            if module.path:
                print("P", end="")
            else:
                print("m", end="")
            print(f" {module.name:<25} {(module.file or '')!s}")

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
        finder.IncludeFile(*self.constants_module.create(finder.modules))

        modules = [m for m in finder.modules if m.name not in finder.excludes]
        modules.sort(key=lambda m: m.name)

        if self.silent < 1:
            self._print_report(filename, modules)
        if self.silent < 2:
            finder.ReportMissingModules()

        target_lib_dir = filename.parent
        self._create_directory(target_lib_dir)

        # Prepare zip file
        if self.compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED
        outFile = zipfile.PyZipFile(filename, "w", compress_type)

        files_to_copy: List[Tuple[Module, Path]] = []
        ignorePatterns = shutil.ignore_patterns(
            "*.py", "*.pyc", "*.pyo", "__pycache__"
        )
        for module in modules:

            # determine if the module should be written to the file system;
            # a number of packages make the assumption that files that they
            # require will be found in a location relative to where
            # they are located on disk; these packages will fail with strange
            # errors when they are written to a zip file instead
            include_in_file_system = module.in_file_system

            # if the module refers to a package, check to see if this package
            # should be included in the zip file or should be written to the
            # file system; if the package should be written to the file system,
            # any non-Python files are copied at this point if the target
            # directory does not already exist
            if (
                include_in_file_system
                and module.path is not None
                and module.file is not None
            ):
                parts = module.name.split(".")
                target_package_dir = target_lib_dir.joinpath(*parts)
                source_package_dir = module.file.parent
                if not target_package_dir.exists():
                    if self.silent < 1:
                        print(f"copying data from package {module.name}...")
                    shutil.copytree(
                        source_package_dir,
                        target_package_dir,
                        ignore=ignorePatterns,
                    )

                    # remove the subfolders which belong to excluded modules
                    excluded_folders = [
                        m[len(module.name) + 1 :].replace(".", os.sep)
                        for m in finder.excludes
                        if m.split(".")[0] == parts[0]
                    ]
                    for folder in excluded_folders:
                        folder_to_remove = target_package_dir / folder
                        if folder_to_remove.is_dir():
                            if self.silent < 1:
                                print(f"removing {folder_to_remove}...")
                            shutil.rmtree(folder_to_remove)

            # if an extension module is found in a package that is to be
            # included in a zip file, copy the actual file to the build
            # directory because shared libraries cannot be loaded from a
            # zip file
            if (
                module.code is None
                and module.file is not None
                and not include_in_file_system
            ):
                parts = module.name.split(".")[:-1]
                parts.append(module.file.name)
                target = target_lib_dir / ".".join(parts)
                files_to_copy.append((module, target))

            # starting with Python 3.3 the pyc file format contains the source
            # size; it is not actually used for anything except determining if
            # the file is up to date so we can safely set this value to zero
            if module.code is not None:
                if module.file is not None and module.file.exists():
                    st = module.file.stat()
                    mtime = int(st.st_mtime)
                    size = st.st_size & 0xFFFFFFFF
                else:
                    mtime = int(time.time())
                    size = 0
                if sys.version_info[:2] < (3, 7):
                    header = MAGIC_NUMBER + struct.pack("<ii", mtime, size)
                else:
                    header = MAGIC_NUMBER + struct.pack("<iii", 0, mtime, size)
                data = header + marshal.dumps(module.code)

            # if the module should be written to the file system, do so
            if include_in_file_system and module.file is not None:
                parts = module.name.split(".")
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
                target_name = "/".join(module.name.split("."))
                if module.path:
                    target_name += "/__init__"
                zinfo = zipfile.ZipInfo(target_name + ".pyc", zipTime)
                zinfo.compress_type = compress_type
                outFile.writestr(zinfo, data)

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
                outFile.write(name, name.as_posix()[pos:])

        # write any files to the zip file that were requested specially
        for source_path, target_path in finder.zip_includes:
            if source_path.is_dir():
                pos = len(source_path.as_posix()) + 1
                for source_filename in source_path.rglob("*"):
                    if source_filename.is_dir():
                        continue
                    target = target_path / source_filename.as_posix()[pos:]
                    outFile.write(source_filename, target)
            else:
                outFile.write(source_path, target_path.as_posix())

        outFile.close()

        # Copy Python extension modules from the list built above.
        origPath = os.environ["PATH"]
        for module, target in files_to_copy:
            try:
                if module.parent is not None:
                    path = os.pathsep.join(
                        [origPath] + [str(p) for p in module.parent.path]
                    )
                    os.environ["PATH"] = path
                self._copy_file(module.file, target, copy_dependent_files=True)
            finally:
                os.environ["PATH"] = origPath

    def Freeze(self):
        self.dependent_files: Dict[Path, Set[Path]] = {}
        self.files_copied: Set[Path] = set()
        self.linker_warnings: Dict[Path, Any] = {}

        finder: ModuleFinder = self._get_module_finder()
        self.finder: ModuleFinder = finder

        # Add the executables to target
        for executable in self.executables:
            self._freeze_executable(executable)

        # Write the modules
        targetdir = self.targetdir
        library_zip = targetdir / "lib" / "library.zip"
        self._write_modules(library_zip, finder)

        exclude_dependent_files = self.finder.exclude_dependent_files
        for source_path, target_path in finder.include_files:
            copy_dependent_files = source_path not in exclude_dependent_files
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


class WinFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # deal with C-runtime files
        self.runtime_files: Set[str] = set()
        self.runtime_files_to_dup: Set[str] = set()
        self._set_runtime_files()

    def _add_resources(self, exe: Executable) -> None:
        target_path: Path = self.targetdir / exe.target_name

        # Add version resource
        if self.metadata is not None:
            warning_msg = "WARNING: unable to create version resource"
            if version_stamp is None:
                if self.silent < 3:
                    print(warning_msg)
                    print("install pywin32 extensions first")
            elif not self.metadata.version:
                if self.silent < 3:
                    print(warning_msg)
                    print("version must be specified")
            else:
                versionInfo = VersionInfo(
                    self.metadata.version,
                    comments=self.metadata.long_description,
                    description=self.metadata.description,
                    company=self.metadata.author,
                    product=self.metadata.name,
                    copyright=exe.copyright,
                    trademarks=exe.trademarks,
                )
                version_stamp(str(target_path), versionInfo)

        # Add icon
        if exe.icon is not None:
            try:
                winutil.AddIcon(target_path, exe.icon)
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
            winutil.UpdateCheckSum(target_path)
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
        # top dependencies do not go into lib on windows.
        target = self.targetdir / source.name
        self._copy_file(
            source, target, copy_dependent_files=True, include_mode=True
        )

    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths. Also, adjust the target of
        C runtime libraries and triggers an additional copy for files in
        self.runtime_files_to_dup."""

        # fix the target path for C runtime files
        norm_target_name = target.name.lower()
        if norm_target_name in self.runtime_files:
            target_name = target.name
            target = self.targetdir / "lib" / target_name

            # vcruntime140.dll must be in the root and in the lib directory
            if norm_target_name in self.runtime_files_to_dup:
                self.runtime_files_to_dup.remove(norm_target_name)
                self._copy_file(source, target, copy_dependent_files=False)
                target = self.targetdir / target_name
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
            and source not in self.finder.exclude_dependent_files
        ):

            targetdir = target.parent
            for dependent_file in self._get_dependent_files(source):
                target = targetdir / dependent_file.name
                self._copy_file(dependent_file, target, copy_dependent_files)

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
        systemDir = winutil.GetSystemDir()
        windowsDir = winutil.GetWindowsDir()
        return [windowsDir, systemDir, os.path.join(windowsDir, "WinSxS")]

    def _default_bin_path_includes(self) -> List[str]:
        paths = {Path(path) for path in sys.path if path}
        # force some paths for conda systems
        paths.add(Path(sys.prefix, "DLLs"))
        paths.add(Path(sys.prefix, "Library", "bin"))
        # do the same for msys2, mingw32/64
        if sysconfig.get_config_var("DESTSHARED"):
            paths.add(Path(sysconfig.get_config_var("DESTSHARED")))
        # return only valid paths
        return [str(path) for path in paths if path.is_dir()]

    def _get_dependent_files(self, path: Path) -> Set[Path]:
        try:
            return self.dependent_files[path]
        except KeyError:
            pass

        dependent_files: Set[Path] = set()
        if path.suffix.lower().endswith((".exe", ".dll", ".pyd")):
            origPath = os.environ["PATH"]
            os.environ["PATH"] = (
                origPath + os.pathsep + os.pathsep.join(sys.path)
            )
            try:
                files: List[str] = winutil.GetDependentFiles(path)
            except winutil.BindError as exc:
                # Sometimes this gets called when path is not actually
                # a library (See issue 88).
                if self.silent < 3:
                    print("WARNING: ignoring error during ", end="")
                    print(f"GetDependentFiles({path}):", exc)
            else:
                dependent_files = {Path(dep) for dep in files}
            os.environ["PATH"] = origPath
        self.dependent_files[path] = dependent_files
        return dependent_files

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


class DarwinFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.darwinTracker: Optional[DarwinFileTracker] = None
        self.darwinTracker = DarwinFileTracker()

    def _post_freeze_hook(self) -> None:
        self.darwinTracker.finalizeReferences()

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

        self.darwinTracker.recordCopiedFile(target, darwin_file)
        if (
            copy_dependent_files
            and source not in self.finder.exclude_dependent_files
        ):
            # Always copy dependent files on root directory
            # to allow to set relative reference
            targetdir = self.targetdir
            for dependent in self._get_dependent_files(source, darwin_file):
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
                # the file was copied to (so the reference can later be updated).
                reference.setTargetFile(
                    self.darwinTracker.getDarwinFile(source, target)
                )
            return
        if source == target:
            return
        self._create_directory(target.parent)
        if self.silent < 1:
            print(f"copying {source!s} -> {target!s}")
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
        # found by the _get_dependent_files calls made previously (if any).
        # If one is found, pass into _copy_file.
        # We need to do this so the file knows what file referenced it,
        # and can therefore calculate the appropriate rpath.
        # (We only cache one reference.)
        cachedReference = self.darwinTracker.getCachedReferenceTo(source)
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

    def _get_dependent_files(
        self, path: Path, darwinFile: Optional["DarwinFile"] = None
    ) -> Set[Path]:
        try:
            return self.dependent_files[path]
        except KeyError:
            pass

        # if darwinFile is None (which means that _get_dependent_files is
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
                self.darwinTracker.cacheReferenceTo(
                    reference.resolved_path, reference
                )
        self.dependent_files[path] = dependent_files
        return dependent_files


class LinuxFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patchelf = Patchelf()

    def _pre_copy_hook(self, source: Path, target: Path) -> Tuple[Path, Path]:
        """Prepare the source and target paths."""
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
            and source not in self.finder.exclude_dependent_files
        ):
            targetdir = target.parent
            source_dir = source.parent
            library_dir = self.targetdir / "lib"
            fix_rpath = set()
            for dependent_file in self._get_dependent_files(source):
                if not self._should_copy_file(dependent_file):
                    continue
                try:
                    relative = dependent_file.relative_to(source_dir)
                except ValueError:
                    # put it in the targetdir if not already copied
                    dependent_filename = dependent_file.name
                    dependent_target = targetdir / dependent_filename
                    relative = Path(dependent_filename)
                    if dependent_target not in self.files_copied:
                        for file in self.files_copied:
                            if file.name == dependent_filename:
                                relative = file.relative_to(library_dir)
                                dependent_target = library_dir / relative
                                break
                else:
                    if targetdir == library_dir:
                        parts = relative.parts
                        while parts[0] == os.pardir:
                            parts = parts[1:]
                        relative = Path(*parts)
                    dependent_target = targetdir / relative
                dep_libs = str(relative.parent)
                fix_rpath.add(dep_libs)
                self._copy_file(
                    dependent_file, dependent_target, copy_dependent_files
                )
            if fix_rpath:
                has_rpath = self.patchelf.get_rpath(target)
                rpath = ":".join(f"$ORIGIN/{r}" for r in fix_rpath)
                if has_rpath != rpath:
                    self.patchelf.set_rpath(target, rpath)

    def _copy_top_dependency(self, source: Path) -> None:
        """Called for copying certain top dependencies in _freeze_executable."""
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
        return [sysconfig.get_config_var("DESTSHARED")]

    def _get_dependent_files(self, path: Path) -> Set[Path]:
        try:
            return self.dependent_files[path]
        except KeyError:
            pass

        dependent_files: Set[Path] = self.patchelf.get_needed(
            path, self.linker_warnings, show_warnings=self.silent < 3
        )
        self.dependent_files[path] = dependent_files
        return dependent_files
