"""
Base class for freezing scripts into executables.
"""

from abc import ABC, abstractmethod
from distutils.dist import DistributionMetadata
from importlib.util import MAGIC_NUMBER
import marshal
import os
import shutil
import stat
import struct
import sys
import sysconfig
import time
from typing import Any, Dict, List, Set, Tuple, Optional, Union
import zipfile

from .common import get_resource_file_path, process_path_specs
from .darwintools import DarwinFile, MachOReference, DarwinFileTracker
from .exception import ConfigError
from .executable import Executable
from .finder import ModuleFinder
from .module import ConstantsModule

if sys.platform == "linux":
    from .patchelf import Patchelf
if sys.platform == "win32":
    from . import winmsvcr
    from . import util as winutil
    from .winversioninfo import VersionInfo

    try:
        from win32verstamp import stamp as version_stamp
    except:
        version_stamp = None

__all__ = ["ConfigError", "ConstantsModule", "Executable", "Freezer"]


class Freezer(ABC):
    def __new__(cls, *args, **kwargs):
        # create instance of appropriate sub-class, depending on the platform.
        instance: Freezer
        if sys.platform == "win32":
            instance = super().__new__(WinFreezer)
        elif sys.platform == "darwin":
            instance = super().__new__(DarwinFreezer)
        else:  # assume any other platform would be handled by LinuxFreezer
            instance = super().__new__(LinuxFreezer)
        return instance

    def __init__(
        self,
        executables: List["Executable"],
        constantsModule: Optional["ConstantsModule"] = None,
        includes: Optional[List[str]] = None,
        excludes: Optional[List[str]] = None,
        packages: Optional[List[str]] = None,
        replacePaths: Optional[List] = None,
        compress: bool = True,
        optimizeFlag: int = 0,
        path: Optional[List[str]] = None,
        targetDir: Optional[str] = None,
        binIncludes: Optional[List] = None,
        binExcludes: Optional[List] = None,
        binPathIncludes: Optional[List] = None,
        binPathExcludes: Optional[List] = None,
        includeFiles: Optional[List] = None,
        zipIncludes: Optional[List] = None,
        silent: Union[bool, int] = 0,
        metadata: Optional[DistributionMetadata] = None,
        includeMSVCR: bool = False,
        zipIncludePackages: Optional[List[str]] = None,
        zipExcludePackages: Optional[List[str]] = None,
    ):
        self.executables = list(executables)
        self.constants_module = constantsModule or ConstantsModule()
        self.includes = list(includes or [])
        self.excludes = list(excludes or [])
        self.packages = set(list(packages or []))
        self.replacePaths = list(replacePaths or [])
        self.compress = True if compress is None else compress
        self.optimize_flag = optimizeFlag
        self.path = sys.path if path is None else path
        self.include_msvcr = includeMSVCR
        self.targetdir = targetDir
        self.binIncludes = binIncludes
        self.binExcludes = binExcludes
        self.binPathIncludes = binPathIncludes
        self.binPathExcludes = binPathExcludes
        self.includeFiles = process_path_specs(includeFiles)
        self.zipIncludes = process_path_specs(zipIncludes)
        if isinstance(silent, bool):
            if silent:
                self.silent = 1
            else:
                self.silent = 0
        else:
            self.silent = silent
        self.metadata = metadata
        self.zipIncludePackages = zipIncludePackages
        self.zipExcludePackages = zipExcludePackages
        self._VerifyConfiguration()

    def _AddVersionResource(self, exe):
        return

    def _CopyFile(
        self,
        source,
        target,
        copyDependentFiles,
        includeMode=False,
    ):
        if not self._ShouldCopyFile(source):
            return

        normalizedSource = os.path.normcase(os.path.normpath(source))
        normalizedTarget = os.path.normcase(os.path.normpath(target))

        # fix the target path for C runtime files (should do nothing on Darwin)
        target, normalizedTarget = self._CopyFileNameHook(
            source=source, target=target, normalizedTarget=normalizedTarget
        )

        if normalizedTarget in self.files_copied:
            return
        if normalizedSource == normalizedTarget:
            return
        targetdir = os.path.dirname(target)
        self._CreateDirectory(targetdir)
        if self.silent < 1:
            print(f"copying {source} -> {target}")
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        if includeMode:
            shutil.copymode(source, target)
        self.files_copied.add(normalizedTarget)

        # handle post-copy tasks, including copying dependencies
        self._PostCopyHook(
            source=source,
            target=target,
            normalizedSource=normalizedSource,
            normalizedTarget=normalizedTarget,
            copyDependentFiles=copyDependentFiles,
            includeMode=includeMode,
        )

    def _CopyFileNameHook(
        self, source: str, target: str, normalizedTarget: str
    ) -> Tuple[str, str]:
        # by default, do nothing and pass through the paths
        return target, normalizedTarget

    @abstractmethod
    def _PostCopyHook(
        self,
        source,
        target,
        normalizedSource,
        normalizedTarget,
        copyDependentFiles,
        includeMode=False,
    ):
        return

    def _CreateDirectory(self, path: str):
        if (self.silent < 1) and not os.path.isdir(path):
            print("creating directory %s" % path)
        os.makedirs(path, exist_ok=True)

    def _FreezeExecutable(self, exe):
        finder: ModuleFinder = self.finder
        finder.IncludeFile(exe.main_script, exe.main_module_name)
        finder.IncludeFile(exe.init_script, exe.init_module_name)
        finder.IncludeFile(
            get_resource_file_path("initscripts", "__startup__", ".py")
        )

        # Ensure the copy of default python libraries
        dependent_files = set(self._GetDependentFiles(exe.base))
        if not dependent_files:
            dependent_files.update(self._GetDependentFiles(sys.executable))
        python_libs = tuple(self._GetDefaultBinIncludes())
        python_dirs = {sys.base_exec_prefix, sys.exec_prefix}  # Win
        python_dirs.add(sysconfig.get_config_var("srcdir"))  # Linux
        for file in dependent_files:
            python_dirs.add(os.path.dirname(file))
        for name in python_libs:
            for python_dir in python_dirs:
                source = os.path.join(python_dir, name)
                if os.path.isfile(source):
                    dependent_files.add(source)
                    break
        if not dependent_files:
            if self.silent < 3:
                print(
                    "*** WARNING *** shared libraries not found:", python_libs
                )

        # Search the C runtimes, using the directory of the python libraries
        # and the directories of the base executable
        self._PlatformAddExtraExecutableDependencies(
            dependent_files=dependent_files
        )

        for source in dependent_files:
            # Store dynamic libraries in appropriate location for platform
            self._CopyTopDependency(source=source)

        target_path = os.path.join(self.targetdir, exe.target_name)
        self._CopyFile(
            exe.base,
            target_path,
            copyDependentFiles=False,
            includeMode=True,
        )
        if not os.access(target_path, os.W_OK):
            mode = os.stat(target_path).st_mode
            os.chmod(target_path, mode | stat.S_IWUSR)

        # Copy icon
        self._CopyIcon(exe=exe, target_path=target_path)

        if self.metadata is not None:
            self._AddVersionResource(exe)

    def _PlatformAddExtraExecutableDependencies(
        self, dependent_files: Set[str]
    ):
        """Override with platform specific files to add runtime libraries to
        the list of dependent_files calculated in _FreezeExecutable."""
        return

    @abstractmethod
    def _CopyTopDependency(self, source: str):
        """Called for copying certain top dependencies in _FreezeExecutable."""
        return

    def _CopyIcon(self, exe, target_path):
        """Copy icon into application.  (Overridden on Windows)."""
        if exe.icon is None:
            return
        target_icon = os.path.join(self.targetdir, os.path.basename(exe.icon))
        self._CopyFile(exe.icon, target_icon, copyDependentFiles=False)
        return

    def _GetDefaultBinExcludes(self):
        """Return the file names of libraries that need not be included because
        they would normally be expected to be found on the target system or
        because they are part of a package which requires independent
        installation anyway.
        (overridden on Windows)"""
        return ["libclntsh.so", "libwtc9.so", "ldd"]

    def _GetDefaultBinIncludes(self):
        """Return the file names of libraries which must be included for the
        frozen executable to work.
        (overriden on Windows)"""
        python_shared_libs = []
        name = sysconfig.get_config_var("INSTSONAME")
        if name:
            python_shared_libs.append(self._RemoveVersionNumbers(name))
        return python_shared_libs

    @abstractmethod
    def _GetDefaultBinPathExcludes(self):
        """Return the paths of directories which contain files that should not
        be included, generally because they contain standard system
        libraries.
        (Overridden on Windows and Darwin)"""
        return []

    @abstractmethod
    def _GetDependentFiles(self, path: str) -> List[str]:
        """Return the file's dependencies using platform-specific tools (the
        imagehlp library on Windows, otool on Mac OS X and ldd on Linux);
        limit this list by the exclusion lists as needed.
        (Implemented separately for each platform.)"""
        return []

    def _GetModuleFinder(self) -> ModuleFinder:
        finder = ModuleFinder(
            self.includeFiles,
            self.excludes,
            self.path,
            self.replacePaths,
            self.zipIncludeAllPackages,
            self.zipExcludePackages,
            self.zipIncludePackages,
            self.constants_module,
            self.zipIncludes,
        )
        finder.SetOptimizeFlag(self.optimize_flag)
        for name in self.includes:
            finder.IncludeModule(name)
        for name in self.packages:
            finder.IncludePackage(name)
        return finder

    def _PrintReport(self, filename, modules):
        print("writing zip file %s\n" % filename)
        print("  {:<25} {}".format("Name", "File"))
        print("  {:<25} {}".format("----", "----"))
        for module in modules:
            if module.path:
                print("P", end="")
            else:
                print("m", end="")
            print(" {:<25} {}\n".format(module.name, module.file or ""))

    @staticmethod
    def _RemoveVersionNumbers(filename):
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

    def _ShouldCopyFile(self, path):
        """
        Return true if the file should be copied to the target machine. This is
        done by checking the binPathIncludes, binPathExcludes, binIncludes and
        binExcludes configuration variables using first the full file name,
        then just the base file name, then the file name without any version
        numbers.

        Files are included unless specifically excluded but inclusions take
        precedence over exclusions."""

        path = os.path.normcase(path)
        dirname, filename = os.path.split(path)

        # check the full path
        if path in self.binIncludes:
            return True
        if path in self.binExcludes:
            return False

        # check the file name by itself (with any included version numbers)
        if filename in self.binIncludes:
            return True
        if filename in self.binExcludes:
            return False

        # check the file name by itself (version numbers removed)
        name = self._RemoveVersionNumbers(filename)
        if name in self.binIncludes:
            return True
        if name in self.binExcludes:
            return False

        # check the path for inclusion/exclusion
        for binpath in self.binPathIncludes:
            if dirname.startswith(binpath):
                return True
        for binpath in self.binPathExcludes:
            if dirname.startswith(binpath):
                return False

        return True

    def _VerifyConfiguration(self):
        # starts in a clean directory
        if self.targetdir is None:
            platform = sysconfig.get_platform()
            python_version = sysconfig.get_python_version()
            dir_name = f"exe.{platform}-{python_version}"
            self.targetdir = os.path.abspath(os.path.join("build", dir_name))
        if os.path.isdir(self.targetdir):

            def onerror(*args):
                raise ConfigError("the build directory cannot be cleaned")

            shutil.rmtree(self.targetdir, onerror=onerror)

        # verify and normalize names and paths
        filenames = list(self.binIncludes or [])
        filenames += self._GetDefaultBinIncludes()
        self.binIncludes = [os.path.normcase(name) for name in filenames]

        filenames = list(self.binExcludes or [])
        filenames += self._GetDefaultBinExcludes()
        self.binExcludes = [os.path.normcase(name) for name in filenames]

        paths = list(self.binPathIncludes or [])
        paths += [path for path in self.path if os.path.isdir(path)]
        self.binPathIncludes = [os.path.normcase(name) for name in paths]

        paths = list(self.binPathExcludes or [])
        paths += self._GetDefaultBinPathExcludes()
        self.binPathExcludes = [os.path.normcase(name) for name in paths]

        for source, target in self.includeFiles + self.zipIncludes:
            if not os.path.exists(source):
                raise ConfigError(f"cannot find file/directory named {source}")
            if os.path.isabs(target):
                raise ConfigError("target file/directory cannot be absolute")

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

    def _WriteModules(self, filename, finder):
        finder.IncludeFile(*self.constants_module.create(finder.modules))

        modules = [m for m in finder.modules if m.name not in finder.excludes]
        modules.sort(key=lambda m: m.name)

        if self.silent < 1:
            self._PrintReport(filename, modules)
        if self.silent < 2:
            finder.ReportMissingModules()

        targetdir = os.path.dirname(filename)
        self._CreateDirectory(targetdir)

        # Prepare zip file
        if self.compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED
        outFile = zipfile.PyZipFile(filename, "w", compress_type)

        filesToCopy = []
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
                targetPackageDir = os.path.join(targetdir, *parts)
                sourcePackageDir = os.path.dirname(module.file)
                if not os.path.exists(targetPackageDir):
                    if self.silent < 1:
                        print("Copying data from package", module.name + "...")
                    shutil.copytree(
                        sourcePackageDir,
                        targetPackageDir,
                        ignore=ignorePatterns,
                    )

                    # remove the subfolders which belong to excluded modules
                    excludedFolders = [
                        m[len(module.name) + 1 :].replace(".", os.sep)
                        for m in finder.excludes
                        if m.split(".")[0] == parts[0]
                    ]
                    for folder in excludedFolders:
                        folderToRemove = os.path.join(targetPackageDir, folder)
                        if os.path.isdir(folderToRemove):
                            if self.silent < 1:
                                print("Removing", folderToRemove + "...")
                            shutil.rmtree(folderToRemove)

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
                parts.append(os.path.basename(module.file))
                target = os.path.join(targetdir, ".".join(parts))
                filesToCopy.append((module, target))

            # starting with Python 3.3 the pyc file format contains the source
            # size; it is not actually used for anything except determining if
            # the file is up to date so we can safely set this value to zero
            if module.code is not None:
                if module.file is not None and os.path.exists(module.file):
                    st = os.stat(module.file)
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
                    parts.append(os.path.basename(module.file))
                    target_name = os.path.join(targetdir, *parts)
                    self._CopyFile(
                        module.file,
                        target_name,
                        copyDependentFiles=True,
                    )
                else:
                    if module.path is not None:
                        parts.append("__init__")
                    target_name = os.path.join(targetdir, *parts) + ".pyc"
                    with open(target_name, "wb") as fp:
                        fp.write(data)

            # otherwise, write to the zip file
            elif module.code is not None:
                zipTime = time.localtime(mtime)[:6]
                filename = "/".join(module.name.split("."))
                if module.path:
                    filename += "/__init__"
                zinfo = zipfile.ZipInfo(filename + ".pyc", zipTime)
                zinfo.compress_type = compress_type
                outFile.writestr(zinfo, data)

        # put the distribution files metadata in the zip file
        dist_cachedir = finder.dist_cachedir.name
        for dirpath, _, filenames in os.walk(dist_cachedir):
            basedir = dirpath[len(dist_cachedir) + 1 :].replace("\\", "/")
            for name in filenames:
                outFile.write(os.path.join(dirpath, name), f"{basedir}/{name}")

        # write any files to the zip file that were requested specially
        for source_filename, target_filename in finder.zip_includes:
            if os.path.isdir(source_filename):
                for dirPath, _, filenames in os.walk(source_filename):
                    basePath = dirPath[len(source_filename) :]
                    targetPath = target_filename + basePath.replace("\\", "/")
                    for name in filenames:
                        outFile.write(
                            os.path.join(dirPath, name),
                            targetPath + "/" + name,
                        )
            else:
                outFile.write(source_filename, target_filename)

        outFile.close()

        # Copy Python extension modules from the list built above.
        origPath = os.environ["PATH"]
        for module, target in filesToCopy:
            try:
                if module.parent is not None:
                    path = os.pathsep.join([origPath] + module.parent.path)
                    os.environ["PATH"] = path
                self._CopyFile(
                    module.file,
                    target,
                    copyDependentFiles=True,
                )
            finally:
                os.environ["PATH"] = origPath

    def Freeze(self):
        self.dependentFiles: Dict[Any, List] = {}
        self.files_copied = set()
        self.linkerWarnings = {}

        self.finder: ModuleFinder = self._GetModuleFinder()

        # Add the executables to target
        for executable in self.executables:
            self._FreezeExecutable(executable)

        # Write the modules
        targetdir = self.targetdir
        ziptargetdir = os.path.join(targetdir, "lib")
        filename = os.path.join(ziptargetdir, "library.zip")
        self._WriteModules(filename, self.finder)

        for source_filename, target_filename in self.finder.include_files:
            if os.path.isdir(source_filename):
                # Copy directories by recursing into them.
                # Can't use shutil.copytree because we may need dependencies
                for path, dirnames, filenames in os.walk(source_filename):
                    short_path = path[len(source_filename) + 1 :]
                    if ".svn" in dirnames:
                        dirnames.remove(".svn")
                    if "CVS" in dirnames:
                        dirnames.remove("CVS")
                    fulltargetdir = os.path.join(
                        targetdir, target_filename, short_path
                    )
                    self._CreateDirectory(fulltargetdir)
                    for filename in filenames:
                        source_path = os.path.join(path, filename)
                        target_path = os.path.join(fulltargetdir, filename)
                        self._CopyFile(
                            source_path,
                            target_path,
                            copyDependentFiles=True,
                        )
            else:
                # Copy regular files.
                fullname = os.path.join(targetdir, target_filename)
                self._CopyFile(
                    source_filename,
                    fullname,
                    copyDependentFiles=True,
                )

        # do any platform-specific post-Freeze work
        self._PostFreezeHook()

    def _PostFreezeHook(self):
        return


class WinFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # deal with C-runtime files
        self.runtime_files = set()
        self.runtime_files_to_dup = set()
        self._SetRuntimeFiles()

    def _AddVersionResource(self, exe):
        warning_msg = "*** WARNING *** unable to create version resource"
        if version_stamp is None:
            if self.silent < 3:
                print(warning_msg)
                print("install pywin32 extensions first")
            return
        if not self.metadata.version:
            if self.silent < 3:
                print(warning_msg)
                print("version must be specified")
            return

        filename = os.path.join(self.targetdir, exe.target_name)
        versionInfo = VersionInfo(
            self.metadata.version,
            comments=self.metadata.long_description,
            description=self.metadata.description,
            company=self.metadata.author,
            product=self.metadata.name,
            copyright=exe.copyright,
            trademarks=exe.trademarks,
        )
        version_stamp(filename, versionInfo)

    def _CopyIcon(self, exe, target_path):
        if exe.icon is None:
            return
        try:
            winutil.AddIcon(target_path, exe.icon)
        except RuntimeError as exc:
            if self.silent < 3:
                print("*** WARNING ***", exc)
        except OSError as exc:
            if "\\WindowsApps\\" in sys.base_prefix:
                if self.silent < 3:
                    print(
                        "*** WARNING *** Because of restrictions on "
                        "Microsoft Store apps, Python scripts may not "
                        "have full write access to built executable.\n"
                        "You will need to install the full installer.\n"
                        "The following error was returned:"
                    )
                    print(exc)
            else:
                raise
        return

    def _CopyFileNameHook(
        self, source: str, target: str, normalizedTarget: str
    ) -> Tuple[str, str]:
        """Adjusts target and normalizedTarget strings in certain cases related
        to C runtime libraries on Windows. And also triggers an additional copy
        for files in self.runtime_files_to_dup."""
        norm_target_name = os.path.basename(normalizedTarget)
        if norm_target_name in self.runtime_files:
            target_name = os.path.basename(target)
            target = os.path.join(self.targetdir, "lib", target_name)
            # vcruntime140.dll must be in the root and in the lib directory
            if norm_target_name in self.runtime_files_to_dup:
                self.runtime_files_to_dup.remove(norm_target_name)
                self._CopyFile(source, target, copyDependentFiles=False)
                target = os.path.join(self.targetdir, target_name)
            normalizedTarget = os.path.normcase(os.path.normpath(target))
        return target, normalizedTarget

    def _CopyTopDependency(self, source: str):
        """Called for copying certain top dependencies in _FreezeExecutable.
        We need this as a separate method so that it can be overridden on
        Darwin and Windows."""
        target = os.path.join(
            self.targetdir, os.path.basename(source)
        )  # top dependencies do not go into lib on windows.
        self._CopyFile(
            source, target, copyDependentFiles=True, includeMode=True
        )

    def _PostCopyHook(
        self,
        source,
        target,
        normalizedSource,
        normalizedTarget,
        copyDependentFiles,
        includeMode=False,
    ):
        if (
            copyDependentFiles
            and source not in self.finder.exclude_dependent_files
        ):

            targetdir = os.path.dirname(target)
            for dependent_file in self._GetDependentFiles(source):
                target = os.path.join(
                    targetdir, os.path.basename(dependent_file)
                )
                self._CopyFile(dependent_file, target, copyDependentFiles)

    def _GetDefaultBinExcludes(self):
        return ["comctl32.dll", "oci.dll"]

    def _GetDefaultBinIncludes(self):
        python_shared_libs = []
        if sysconfig.get_platform() == "mingw":
            name = sysconfig.get_config_var("INSTSONAME")
            if name:
                python_shared_libs.append(name.replace(".dll.a", ".dll"))
        else:
            python_shared_libs += [
                "python%s.dll" % sys.version_info[0],
                "python%s%s.dll" % sys.version_info[:2],
            ]
        return python_shared_libs

    def _GetDefaultBinPathExcludes(self):
        systemDir = winutil.GetSystemDir()
        windowsDir = winutil.GetWindowsDir()
        return [windowsDir, systemDir, os.path.join(windowsDir, "WinSxS")]

    def _GetDependentFiles(self, path) -> List[str]:
        path = os.path.normcase(path)
        dependentFiles = self.dependentFiles.get(path, None)
        if dependentFiles is not None:
            return dependentFiles

        dependentFiles: List[str] = []
        if path.endswith((".exe", ".dll", ".pyd")):
            origPath = os.environ["PATH"]
            os.environ["PATH"] = (
                origPath + os.pathsep + os.pathsep.join(sys.path)
            )
            try:
                dependentFiles = winutil.GetDependentFiles(path)
            except winutil.BindError as exc:
                # Sometimes this gets called when path is not actually
                # a library (See issue 88).
                if self.silent < 3:
                    print("error during GetDependentFiles() of ", end="")
                    print(f"{path!r}: {exc!s}")
            os.environ["PATH"] = origPath
        self.dependentFiles[path] = dependentFiles
        return dependentFiles

    def _PlatformAddExtraExecutableDependencies(
        self, dependent_files: Set[str]
    ):
        search_dirs = set()
        for filename in dependent_files:
            search_dirs.add(os.path.dirname(filename))
        for filename in self.runtime_files:
            for search_dir in search_dirs:
                filepath = os.path.join(search_dir, filename)
                if os.path.exists(filepath):
                    dependent_files.add(filepath)

    def _SetRuntimeFiles(self):
        if self.include_msvcr:
            self.runtime_files.update(winmsvcr.FILES)
            self.runtime_files_to_dup.update(winmsvcr.FILES_TO_DUPLICATE)
        else:
            # just put on the exclusion list
            self.binExcludes.extend(winmsvcr.FILES)


class DarwinFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.darwinTracker: Optional[DarwinFileTracker] = None
        self.darwinTracker = DarwinFileTracker()

    def _PostFreezeHook(self):
        self.darwinTracker.finalizeReferences()

    def _PostCopyHook(
        self,
        source,
        target,
        normalizedSource,
        normalizedTarget,
        copyDependentFiles,
        includeMode=False,
        machOReference: Optional[MachOReference] = None,
    ):

        # The file was not previously copied, so need to create a
        # DarwinFile file object to represent the file being copied.
        newDarwinFile = None

        referencingFile = None
        if machOReference is not None:
            referencingFile = machOReference.sourceFile

        newDarwinFile = DarwinFile(
            originalFilePath=source, referencingFile=referencingFile
        )
        newDarwinFile.setBuildPath(normalizedTarget)
        if machOReference is not None:
            machOReference.setTargetFile(darwinFile=newDarwinFile)

        self.darwinTracker.recordCopiedFile(
            targetPath=normalizedTarget, darwinFile=newDarwinFile
        )
        if (
            copyDependentFiles
            and source not in self.finder.exclude_dependent_files
        ):
            # Always copy dependent files on root directory
            # to allow to set relative reference
            for dependent_file in self._GetDependentFiles(
                source, darwinFile=newDarwinFile
            ):
                targetdir = self.targetdir
                target = os.path.join(
                    targetdir, os.path.basename(dependent_file)
                )
                self._CopyFileRecursion(
                    dependent_file,
                    target,
                    copyDependentFiles=True,
                    machOReference=newDarwinFile.getMachOReferenceForPath(
                        path=dependent_file
                    ),
                )

    def _CopyFileRecursion(
        self,
        source,
        target,
        copyDependentFiles,
        includeMode=False,
        machOReference: Optional[MachOReference] = None,
    ):
        """This is essentially the same as Freezer._CopyFile, except that it
        also takes a machOReference parameter. Used when recursing to
        dependencies of a file on Darwin."""
        if not self._ShouldCopyFile(source):
            return

        normalizedSource = os.path.normcase(os.path.normpath(source))
        normalizedTarget = os.path.normcase(os.path.normpath(target))

        # fix the target path for C runtime files
        target, normalizedTarget = self._CopyFileNameHook(
            source=source, target=target, normalizedTarget=normalizedTarget
        )

        if normalizedTarget in self.files_copied:
            if machOReference is not None:
                # If file was already copied, and we are following a reference
                # from a DarwinFile, then we need to tell the reference where
                # the file was copied to (so the reference can later be updated).
                copiedDarwinFile = self.darwinTracker.getDarwinFile(
                    sourcePath=normalizedSource, targetPath=normalizedTarget
                )
                machOReference.setTargetFile(darwinFile=copiedDarwinFile)
            return
        if normalizedSource == normalizedTarget:
            return
        targetdir = os.path.dirname(target)
        self._CreateDirectory(targetdir)
        if self.silent < 1:
            print(f"copying {source} -> {target}")
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        if includeMode:
            shutil.copymode(source, target)
        self.files_copied.add(normalizedTarget)

        # handle post-copy tasks, including copying dependencies
        self._PostCopyHook(
            source=source,
            target=target,
            normalizedSource=normalizedSource,
            normalizedTarget=normalizedTarget,
            copyDependentFiles=copyDependentFiles,
            includeMode=includeMode,
            machOReference=machOReference,
        )

    def _CopyTopDependency(self, source: str):
        """Called for copying certain top dependencies. We need this as a
        separate function so that it can be overridden on Darwin
        (to interact with the DarwinTools system)."""

        target = os.path.join(
            os.path.join(self.targetdir, "lib"), os.path.basename(source)
        )

        # this recovers the cached MachOReference pointers to the files
        # found by the _GetDependentFiles calls made previously (if any).
        # If one is found, pass into _CopyFile.
        # We need to do this so the file knows what file referenced it,
        # and can therefore calculate the appropriate rpath.
        # (We only cache one reference.)
        cachedReference = self.darwinTracker.getCachedReferenceTo(
            sourcePath=source
        )
        self._CopyFileRecursion(
            source,
            target,
            copyDependentFiles=True,
            includeMode=True,
            machOReference=cachedReference,
        )

    def _GetDefaultBinPathExcludes(self):
        return ["/lib", "/usr/lib", "/System/Library/Frameworks"]

    def _GetDependentFiles(
        self, path, darwinFile: Optional[DarwinFile] = None
    ) -> List[str]:
        path = os.path.normcase(path)
        dependentFiles = self.dependentFiles.get(path, None)
        if dependentFiles is not None:
            return dependentFiles

        # if darwinFile is None (which means that _GetDependentFiles is
        # being called outside of _CopyFile -- e.g., one of the
        # preliminary calls in _FreezeExecutable), create a temporary
        # DarwinFile object for the path, just so we can read its
        # dependencies
        if darwinFile is None:
            darwinFile = DarwinFile(
                originalFilePath=path, referencingFile=None
            )
        dependentFiles = darwinFile.getDependentFilePaths()

        # cache the MachOReferences to the dependencies, so they can be
        # called up later in _CopyFile if copying a dependency without
        # an explicit reference provided
        # (to assist in resolving @rpaths)
        for reference in darwinFile.getMachOReferenceList():
            if reference.isResolved():
                self.darwinTracker.cacheReferenceTo(
                    sourcePath=reference.resolvedReferencePath,
                    machOReference=reference,
                )
        self.dependentFiles[path] = dependentFiles
        return dependentFiles


class LinuxFreezer(Freezer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patchelf = Patchelf()

    def _PostCopyHook(
        self,
        source,
        target,
        normalizedSource,
        normalizedTarget,
        copyDependentFiles,
        includeMode=False,
    ):
        if (
            copyDependentFiles
            and source not in self.finder.exclude_dependent_files
        ):
            targetdir = os.path.dirname(target)
            source_dir = os.path.dirname(source)
            library_dir = os.path.join(self.targetdir, "lib")
            fix_rpath = set()
            for dependent_file in self._GetDependentFiles(source):
                dep_base = os.path.basename(dependent_file)
                dep_abs = os.path.abspath(dependent_file)
                dep_rel = os.path.relpath(dep_abs, source_dir)
                if targetdir == library_dir:
                    while dep_rel.startswith(os.pardir + os.sep):
                        dep_rel = dep_rel[len(os.pardir + os.sep) :]
                dep_libs = dep_rel[: -(len(dep_base) + 1)]
                if dep_libs:
                    fix_rpath.add(dep_libs)
                dependent_target = os.path.join(targetdir, dep_rel)
                self._CopyFile(
                    dependent_file,
                    dependent_target,
                    copyDependentFiles,
                )
            if fix_rpath:
                has_rpath = self.patchelf.get_rpath(target)
                rpath = ":".join([f"$ORIGIN/{r}" for r in fix_rpath])
                if has_rpath != rpath:
                    self.patchelf.set_rpath(target, rpath)

    def _CopyTopDependency(self, source: str):
        """Called for copying certain top dependencies in _FreezeExecutable."""
        target = os.path.join(
            os.path.join(self.targetdir, "lib"), os.path.basename(source)
        )
        self._CopyFile(
            source, target, copyDependentFiles=True, includeMode=True
        )

    def _GetDefaultBinPathExcludes(self):
        return [
            "/lib",
            "/lib32",
            "/lib64",
            "/usr/lib",
            "/usr/lib32",
            "/usr/lib64",
        ]

    def _GetDependentFiles(self, path) -> List[str]:
        path = os.path.normcase(path)
        dependentFiles = self.dependentFiles.get(path, None)
        if dependentFiles is not None:
            return dependentFiles

        dependentFiles = []
        if not os.access(path, os.X_OK):
            self.dependentFiles[path] = []
            return []
        command = f"ldd {path!r}"
        splitString = " => "
        dependentFileIndex = 1
        for line in os.popen(command):
            parts = line.expandtabs().strip().split(splitString)
            if len(parts) != 2:
                continue
            dependentFile = parts[dependentFileIndex].strip()
            if dependentFile == os.path.basename(path):
                continue
            if dependentFile in ("not found", "(file not found)"):
                filename = parts[0]
                if filename not in self.linkerWarnings:
                    self.linkerWarnings[filename] = None
                    if self.silent < 3:
                        print("WARNING: cannot find %s" % filename)
                continue
            if dependentFile.startswith("("):
                continue
            pos = dependentFile.find(" (")
            if pos >= 0:
                dependentFile = dependentFile[:pos].strip()
            if dependentFile:
                dependentFiles.append(dependentFile)
        self.dependentFiles[path] = dependentFiles
        return dependentFiles
