"""
Base class for freezing scripts into executables.
"""

import datetime
from distutils.dist import DistributionMetadata
import distutils.sysconfig
from importlib.util import MAGIC_NUMBER
from keyword import iskeyword
import marshal
import os
import shutil
import socket
import stat
import string
import struct
import sys
import sysconfig
import tempfile
import time
from typing import Any, Dict, List, Optional
import uuid
import zipfile

from .common import (
    ConfigError,
    get_resource_file_path,
    process_path_specs,
    validate_args,
)
from .darwintools import DarwinFile, MachOReference, DarwinFileTracker
from .finder import ModuleFinder

if sys.platform == "win32":
    import cx_Freeze.util

__all__ = ["ConfigError", "ConstantsModule", "Executable", "Freezer"]

STRINGREPLACE = list(
    string.whitespace + string.punctuation.replace(".", "").replace("_", "")
)


class Freezer:
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
        silent: bool = False,
        metadata: Optional[DistributionMetadata] = None,
        includeMSVCR: bool = False,
        zipIncludePackages: Optional[List[str]] = None,
        zipExcludePackages: Optional[List[str]] = ["*"],
    ):
        self.executables = list(executables)
        self.constantsModule = constantsModule or ConstantsModule()
        self.includes = list(includes or [])
        self.excludes = list(excludes or [])
        self.packages = set(list(packages or []))
        self.replacePaths = list(replacePaths or [])
        self.compress = compress
        self.optimizeFlag = optimizeFlag
        self.path = path
        self.includeMSVCR = includeMSVCR
        self.targetDir = targetDir
        binIncludes = self._GetDefaultBinIncludes() + list(binIncludes or [])
        self.binIncludes = [os.path.normcase(n) for n in binIncludes]
        binExcludes = self._GetDefaultBinExcludes() + list(binExcludes or [])
        self.binExcludes = [os.path.normcase(n) for n in binExcludes]
        binPathIncludes = binPathIncludes or []
        self.binPathIncludes = [os.path.normcase(n) for n in binPathIncludes]
        binPathExcludes = self._GetDefaultBinPathExcludes() + list(
            binPathExcludes or []
        )
        self.binPathExcludes = [os.path.normcase(n) for n in binPathExcludes]
        self.includeFiles = process_path_specs(includeFiles)
        self.zipIncludes = process_path_specs(zipIncludes)
        self.silent = silent
        self.metadata = metadata
        self.zipIncludePackages = list(zipIncludePackages or [])
        self.zipExcludePackages = list(zipExcludePackages or [])
        self._VerifyConfiguration()

    def _AddVersionResource(self, exe):
        warning_msg = "*** WARNING *** unable to create version resource"
        try:
            from win32verstamp import stamp
        except:
            print(warning_msg)
            print("install pywin32 extensions first")
            return
        if not self.metadata.version:
            print(warning_msg)
            print("version must be specified")
            return
        fileName = os.path.join(self.targetDir, exe.target_name)
        versionInfo = VersionInfo(
            self.metadata.version,
            comments=self.metadata.long_description,
            description=self.metadata.description,
            company=self.metadata.author,
            product=self.metadata.name,
            copyright=exe.copyright,
            trademarks=exe.trademarks,
        )
        stamp(fileName, versionInfo)

    def _CopyFile(
        self,
        source,
        target,
        copyDependentFiles,
        includeMode=False,
        relativeSource=False,
        machOReference: Optional[MachOReference] = None,
    ):
        normalizedSource = os.path.normcase(os.path.normpath(source))
        normalizedTarget = os.path.normcase(os.path.normpath(target))

        if normalizedTarget in self.files_copied:
            if sys.platform == "darwin" and (machOReference is not None):
                # If file was already copied, and we are following a reference
                # from a DarwinFile, then we need to tell the reference where
                # the file was copied to.
                targetDarwinFile = self.darwinTracker.getDarwinFile(
                    sourcePath=normalizedSource, targetPath=normalizedTarget
                )
                machOReference.setTargetFile(darwinFile=targetDarwinFile)
            return
        if normalizedSource == normalizedTarget:
            return
        self._RemoveFile(target)
        targetDir = os.path.dirname(target)
        self._CreateDirectory(targetDir)
        if not self.silent:
            print(f"copying {source} -> {target}")
        shutil.copyfile(source, target)
        shutil.copystat(source, target)
        if includeMode:
            shutil.copymode(source, target)
        self.files_copied.add(normalizedTarget)

        newDarwinFile = None
        if sys.platform == "darwin":
            # The file was not previously copied, so need to create a
            # DarwinFile file object to represent the file being copied.
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
            # TODO: relativeSource for other platforms
            if sys.platform != "linux":
                relativeSource = False
            # Always copy dependent files on root directory
            # to allow to set relative reference
            sourceDir = os.path.dirname(source)

            if sys.platform == "darwin":
                targetDir = self.targetDir
                for dependent_file in self._GetDependentFiles(
                    source, darwinFile=newDarwinFile
                ):
                    target = os.path.join(
                        targetDir, os.path.basename(dependent_file)
                    )
                    self._CopyFile(
                        dependent_file,
                        target,
                        copyDependentFiles=True,
                        machOReference=newDarwinFile.getMachOReference(
                            resolvedPath=dependent_file
                        ),
                    )
            else:
                for dependent_file in self._GetDependentFiles(
                    source, darwinFile=newDarwinFile
                ):
                    if (
                        relativeSource
                        and os.path.isabs(dependent_file)
                        and os.path.commonpath((dependent_file, sourceDir))
                        == sourceDir
                    ):
                        relative = os.path.relpath(dependent_file, sourceDir)
                        target = os.path.join(targetDir, relative)
                    else:
                        target = os.path.join(
                            targetDir, os.path.basename(dependent_file)
                        )
                    self._CopyFile(
                        dependent_file,
                        target,
                        copyDependentFiles,
                        relativeSource=relativeSource,
                    )

    def _CreateDirectory(self, path):
        if not os.path.isdir(path):
            if not self.silent:
                print("creating directory %s" % path)
            os.makedirs(path)

    def _FreezeExecutable(self, exe):
        finder = self.finder
        finder.IncludeFile(exe.main_script, exe.main_module_name)
        finder.IncludeFile(exe.init_script, exe.init_module_name)
        startupModule = get_resource_file_path(
            "initscripts", "__startup__", ".py"
        )
        finder.IncludeFile(startupModule)

        # Ensure the copy of default python libraries
        dependent_files = set()
        dependent_files.update(self._GetDependentFiles(exe.base))
        dependent_files.update(self._GetDependentFiles(sys.executable))
        for name in self._GetDefaultBinIncludes():
            normalized_name = os.path.normcase(name)
            found = False
            for dependent_name in list(dependent_files):
                if os.path.normcase(dependent_name).endswith(normalized_name):
                    found = True
                    break
                source_dir = os.path.dirname(dependent_name)
                source = os.path.join(source_dir, name)
                if os.path.isfile(source):
                    dependent_files.add(source)
                    found = True
                    break
            if not found:
                print("*** WARNING *** default bin include not found:", name)
        # Copy the python dynamic libraries and the frozen executable
        if sys.platform == "win32":
            # Copy the python dynamic libraries into build root folder
            target_dir = self.targetDir
        else:
            # Always copy the python dynamic libraries into lib folder
            target_dir = os.path.join(self.targetDir, "lib")
        for source in dependent_files:
            target = os.path.join(target_dir, os.path.basename(source))
            if sys.platform == "darwin":
                self._CopyFile(
                    source,
                    target,
                    copyDependentFiles=True,
                    includeMode=True,
                    machOReference=self.darwinTracker.getCachedReferenceTo(
                        path=source
                    ),
                )
            else:
                self._CopyFile(
                    source, target, copyDependentFiles=True, includeMode=True
                )
        target_path = os.path.join(self.targetDir, exe.target_name)
        self._CopyFile(
            exe.base,
            target_path,
            copyDependentFiles=False,
            includeMode=True,
        )
        if not os.access(target_path, os.W_OK):
            mode = os.stat(target_path).st_mode
            os.chmod(target_path, mode | stat.S_IWUSR)

        if self.includeMSVCR:
            self._IncludeMSVCR(exe)

        # Copy icon
        if exe.icon is not None:
            if sys.platform == "win32":
                try:
                    cx_Freeze.util.AddIcon(target_path, exe.icon)
                except RuntimeError as exc:
                    print("*** WARNING ***", exc)
                except OSError as exc:
                    if "\\WindowsApps\\" in sys.base_prefix:
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
            else:
                target_icon = os.path.join(
                    self.targetDir, os.path.basename(exe.icon)
                )
                self._CopyFile(exe.icon, target_icon, copyDependentFiles=False)

        if self.metadata is not None and sys.platform == "win32":
            self._AddVersionResource(exe)

    def _GetDefaultBinExcludes(self):
        """Return the file names of libraries that need not be included because
        they would normally be expected to be found on the target system or
        because they are part of a package which requires independent
        installation anyway."""
        if sys.platform == "win32":
            return ["comctl32.dll", "oci.dll", "cx_Logging.pyd"]
        else:
            return ["libclntsh.so", "libwtc9.so", "ldd"]

    def _GetDefaultBinIncludes(self):
        """Return the file names of libraries which must be included for the
        frozen executable to work."""
        python_shared_libs = []
        if sys.platform == "win32":
            if sysconfig.get_platform() == "mingw":
                name = distutils.sysconfig.get_config_var("INSTSONAME")
                if name:
                    python_shared_libs.append(name.replace(".dll.a", ".dll"))
            else:
                python_shared_libs += [
                    "python%s.dll" % sys.version_info[0],
                    "python%s%s.dll" % sys.version_info[:2],
                    "vcruntime140.dll",
                ]
        else:
            name = distutils.sysconfig.get_config_var("INSTSONAME")
            if name:
                python_shared_libs.append(self._RemoveVersionNumbers(name))
        return python_shared_libs

    def _GetDefaultBinPathExcludes(self):
        """Return the paths of directories which contain files that should not
        be included, generally because they contain standard system
        libraries."""
        if sys.platform == "win32":
            systemDir = cx_Freeze.util.GetSystemDir()
            windowsDir = cx_Freeze.util.GetWindowsDir()
            return [windowsDir, systemDir, os.path.join(windowsDir, "WinSxS")]
        elif sys.platform == "darwin":
            return ["/lib", "/usr/lib", "/System/Library/Frameworks"]
        else:
            return [
                "/lib",
                "/lib32",
                "/lib64",
                "/usr/lib",
                "/usr/lib32",
                "/usr/lib64",
            ]

    def _GetDependentFiles(self, path, darwinFile: DarwinFile = None) -> List:
        """Return the file's dependencies using platform-specific tools (the
        imagehlp library on Windows, otool on Mac OS X and ldd on Linux);
        limit this list by the exclusion lists as needed"""
        path = os.path.normcase(path)
        dependentFiles = self.dependentFiles.get(path, [])
        if not dependentFiles:
            if sys.platform == "win32":
                if path.endswith((".exe", ".dll", ".pyd")):
                    origPath = os.environ["PATH"]
                    os.environ["PATH"] = (
                        origPath + os.pathsep + os.pathsep.join(sys.path)
                    )
                    try:
                        dependentFiles = cx_Freeze.util.GetDependentFiles(path)
                    except cx_Freeze.util.BindError as exc:
                        # Sometimes this gets called when path is not actually a
                        # library See issue 88
                        print("error during GetDependentFiles() of ", end="")
                        print(f"{path!r}: {exc!s}")
                    os.environ["PATH"] = origPath
            elif sys.platform == "darwin":
                # if darwinFile is None, create a temporary DarwinFile object
                # for the path, just so we can read its dependencies
                if darwinFile is None:
                    darwinFile = DarwinFile(
                        originalFilePath=path, referencingFile=None
                    )
                dependentFiles = darwinFile.getDependentFilePaths()

                # cache the MachOReferences to the dependencies, so they can be
                # called up later in _CopyFile if copying a dependency without
                # an explicit reference provided
                for depFilePath, ref in darwinFile.getMachOReferences():
                    self.darwinTracker.cacheReferenceTo(
                        path=depFilePath, machOReference=ref
                    )
            else:
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
                        fileName = parts[0]
                        if fileName not in self.linkerWarnings:
                            self.linkerWarnings[fileName] = None
                            print("WARNING: cannot find %s" % fileName)
                        continue
                    if dependentFile.startswith("("):
                        continue
                    pos = dependentFile.find(" (")
                    if pos >= 0:
                        dependentFile = dependentFile[:pos].strip()
                    if dependentFile:
                        dependentFiles.append(dependentFile)

            dependentFiles = [
                os.path.normcase(f)
                for f in dependentFiles
                if self._ShouldCopyFile(f)
            ]
            self.dependentFiles[path] = dependentFiles
        return dependentFiles

    def _GetModuleFinder(self, argsSource=None):
        if argsSource is None:
            argsSource = self
        finder = ModuleFinder(
            self.includeFiles,
            self.excludes,
            self.path,
            self.replacePaths,
            self.zipIncludeAllPackages,
            self.zipExcludePackages,
            self.zipIncludePackages,
            self.constantsModule,
            self.zipIncludes,
        )
        finder.SetOptimizeFlag(self.optimizeFlag)
        for name in self.includes:
            finder.IncludeModule(name)
        for name in self.packages:
            finder.IncludePackage(name)
        return finder

    def _IncludeMSVCR(self, exe):
        targetDir = self.targetDir
        for fullName in self.files_copied:
            path, name = os.path.split(os.path.normcase(fullName))
            if name.startswith("msvcr") and name.endswith(".dll"):
                for otherName in [name.replace("r", c) for c in "mp"]:
                    sourceName = os.path.join(self.msvcRuntimeDir, otherName)
                    if not os.path.exists(sourceName):
                        continue
                    target_name = os.path.join(targetDir, otherName)
                    self._CopyFile(
                        sourceName, target_name, copyDependentFiles=False
                    )
                break

    def _PrintReport(self, fileName, modules):
        print("writing zip file %s\n" % fileName)
        print("  {:<25} {}".format("Name", "File"))
        print("  {:<25} {}".format("----", "----"))
        for module in modules:
            if module.path:
                print("P", end="")
            else:
                print("m", end="")
            print(" {:<25} {}\n".format(module.name, module.file or ""))

    def _RemoveFile(self, path):
        if os.path.exists(path):
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)

    def _RemoveVersionNumbers(self, libName):
        tweaked = False
        parts = libName.split(".")
        while parts:
            if not parts[-1].isdigit():
                break
            parts.pop(-1)
            tweaked = True
        if tweaked:
            libName = ".".join(parts)
        return libName

    def _ShouldCopyFile(self, path):
        """Return true if the file should be copied to the target machine. This
        is done by checking the binPathIncludes, binPathExcludes,
        binIncludes and binExcludes configuration variables using first the
        full file name, then just the base file name, then the file name
        without any version numbers.

        Files are included unless specifically excluded but inclusions take
        precedence over exclusions."""

        # check for C runtime, if desired
        path = os.path.normcase(path)
        dirName, fileName = os.path.split(path)
        if fileName.startswith("msvcr") and fileName.endswith(".dll"):
            self.msvcRuntimeDir = dirName
            return self.includeMSVCR

        # check the full path
        if path in self.binIncludes:
            return True
        if path in self.binExcludes:
            return False

        # check the file name by itself (with any included version numbers)
        if fileName in self.binIncludes:
            return True
        if fileName in self.binExcludes:
            return False

        # check the file name by itself (version numbers removed)
        name = self._RemoveVersionNumbers(fileName)
        if name in self.binIncludes:
            return True
        if name in self.binExcludes:
            return False

        # check the path for inclusion/exclusion
        for path in self.binPathIncludes:
            if dirName.startswith(path):
                return True
        for path in self.binPathExcludes:
            if dirName.startswith(path):
                return False

        return True

    def _VerifyConfiguration(self):
        if self.compress is None:
            self.compress = True
        if self.targetDir is None:
            self.targetDir = os.path.abspath("dist")
        if self.path is None:
            self.path = sys.path

        for sourceFileName, targetFileName in (
            self.includeFiles + self.zipIncludes
        ):
            if not os.path.exists(sourceFileName):
                raise ConfigError(
                    "cannot find file/directory named {}".format(
                        sourceFileName
                    )
                )
            if os.path.isabs(targetFileName):
                raise ConfigError("target file/directory cannot be absolute")

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
                    "package {} cannot be both included and "
                    "excluded from zip file".format(name)
                )

    def _WriteModules(self, fileName, finder):
        self.constantsModule.Create(finder)
        modules = [
            m for m in finder.modules if m.name not in self.excludeModules
        ]
        modules.sort(key=lambda m: m.name)

        if not self.silent:
            self._PrintReport(fileName, modules)
        finder.ReportMissingModules()

        targetDir = os.path.dirname(fileName)
        self._CreateDirectory(targetDir)

        # Prepare zip file
        if self.compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED
        outFile = zipfile.PyZipFile(fileName, "w", compress_type)

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
                targetPackageDir = os.path.join(targetDir, *parts)
                sourcePackageDir = os.path.dirname(module.file)
                if not os.path.exists(targetPackageDir):
                    if not self.silent:
                        print("Copying data from package", module.name + "...")
                    shutil.copytree(
                        sourcePackageDir,
                        targetPackageDir,
                        ignore=ignorePatterns,
                    )

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
                target = os.path.join(targetDir, ".".join(parts))
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
                    target_name = os.path.join(targetDir, *parts)
                    self._CopyFile(
                        module.file,
                        target_name,
                        copyDependentFiles=True,
                        relativeSource=True,
                    )
                else:
                    if module.path is not None:
                        parts.append("__init__")
                    target_name = os.path.join(targetDir, *parts) + ".pyc"
                    with open(target_name, "wb") as fp:
                        fp.write(data)

            # otherwise, write to the zip file
            elif module.code is not None:
                zipTime = time.localtime(mtime)[:6]
                fileName = "/".join(module.name.split("."))
                if module.path:
                    fileName += "/__init__"
                zinfo = zipfile.ZipInfo(fileName + ".pyc", zipTime)
                zinfo.compress_type = compress_type
                outFile.writestr(zinfo, data)

            # put the distribution files metadata in the zip file
            if module.dist_files:
                for filepath, arcname in module.dist_files:
                    if arcname not in outFile.namelist():
                        outFile.write(filepath, arcname)

        # write any files to the zip file that were requested specially
        for sourceFileName, targetFileName in finder.zip_includes:
            if os.path.isdir(sourceFileName):
                for dirPath, _, fileNames in os.walk(sourceFileName):
                    basePath = dirPath[len(sourceFileName) :]
                    targetPath = targetFileName + basePath.replace("\\", "/")
                    for name in fileNames:
                        outFile.write(
                            os.path.join(dirPath, name),
                            targetPath + "/" + name,
                        )
            else:
                outFile.write(sourceFileName, targetFileName)

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
                    relativeSource=True,
                )
            finally:
                os.environ["PATH"] = origPath

    def Freeze(self):
        self.finder = None
        self.excludeModules = {}
        self.dependentFiles = {}  # type: Dict[Any, List]
        self.files_copied = set()
        self.linkerWarnings = {}
        self.msvcRuntimeDir = None

        self.darwinTracker = None  # type: Optional[DarwinFileTracker]
        if sys.platform == "darwin":
            self.darwinTracker = DarwinFileTracker()

        self.finder = self._GetModuleFinder()
        for executable in self.executables:
            self._FreezeExecutable(executable)
        targetDir = self.targetDir
        zipTargetDir = os.path.join(targetDir, "lib")
        fileName = os.path.join(zipTargetDir, "library.zip")
        self._RemoveFile(fileName)
        self._WriteModules(fileName, self.finder)

        for sourceFileName, targetFileName in self.finder.include_files:
            if os.path.isdir(sourceFileName):
                # Copy directories by recursing into them.
                # Can't use shutil.copytree because we may need dependencies
                for path, dirNames, fileNames in os.walk(sourceFileName):
                    shortPath = path[len(sourceFileName) + 1 :]
                    if ".svn" in dirNames:
                        dirNames.remove(".svn")
                    if "CVS" in dirNames:
                        dirNames.remove("CVS")
                    fullTargetDir = os.path.join(
                        targetDir, targetFileName, shortPath
                    )
                    self._CreateDirectory(fullTargetDir)
                    for fileName in fileNames:
                        fullSourceName = os.path.join(path, fileName)
                        fullTargetName = os.path.join(fullTargetDir, fileName)
                        self._CopyFile(
                            fullSourceName,
                            fullTargetName,
                            copyDependentFiles=True,
                            relativeSource=True,
                        )
            else:
                # Copy regular files.
                fullName = os.path.join(targetDir, targetFileName)
                self._CopyFile(
                    sourceFileName,
                    fullName,
                    copyDependentFiles=True,
                    relativeSource=True,
                )

        if sys.platform == "darwin":
            self.darwinTracker.finalizeReferences()
        return


class Executable:

    _base: str
    _init_script: str
    _internal_name: str
    _name: str
    _ext: str

    def __init__(
        self,
        script: str,
        init_script: Optional[str] = None,
        base: Optional[str] = None,
        target_name: Optional[str] = None,
        icon: Optional[str] = None,
        shortcut_name: Optional[str] = None,
        shortcut_dir: Optional[str] = None,
        copyright: Optional[str] = None,
        trademarks: Optional[str] = None,
        *,
        initScript: Optional[str] = None,
        targetName: Optional[str] = None,
        shortcutName: Optional[str] = None,
        shortcutDir: Optional[str] = None,
    ):
        self.main_script: str = script
        self.init_script = validate_args(
            "init_script", init_script, initScript
        )
        self.base = base
        self.target_name = validate_args(
            "target_name", target_name, targetName
        )
        self.icon = icon
        self.shortcut_name = validate_args(
            "shortcut_name", shortcut_name, shortcutName
        )
        self.shortcut_dir = validate_args(
            "shortcut_dir", shortcut_dir, shortcutDir
        )
        self.copyright = copyright
        self.trademarks = trademarks

    def __repr__(self):
        return f"<Executable script={self.main_script}>"

    @property
    def base(self) -> str:
        return self._base

    @base.setter
    def base(self, name: Optional[str]):
        name = name or "Console"
        ext = ".exe" if sys.platform == "win32" else ""
        self._base = get_resource_file_path("bases", name, ext)
        if self._base is None:
            raise ConfigError(f"no base named {name}")

    @property
    def init_module_name(self) -> str:
        return f"{self._internal_name}__init__"

    @property
    def init_script(self) -> str:
        return self._init_script

    @init_script.setter
    def init_script(self, name: Optional[str]):
        name = name or "Console"
        self._init_script = get_resource_file_path("initscripts", name, ".py")
        if self._init_script is None:
            raise ConfigError(f"no init_script named {name}")

    @property
    def main_module_name(self) -> str:
        return f"{self._internal_name}__main__"

    @property
    def target_name(self) -> str:
        return self._name + self._ext

    @target_name.setter
    def target_name(self, name: Optional[str]):
        if name is None:
            name = os.path.splitext(os.path.basename(self.main_script))[0]
            ext = os.path.splitext(self.base)[1]
        else:
            if name != os.path.basename(name):
                raise ConfigError(
                    "target_name should only be the name, for example: "
                    f"{os.path.basename(name)}"
                )
            if sys.platform == "win32":
                if name.endswith(".exe"):
                    name, ext = os.path.splitext(name)
                else:
                    ext = ".exe"
            else:
                ext = ""
        self._name = name
        self._ext = ext
        name = name.partition(".")[0]
        if not name.isidentifier():
            for ch in STRINGREPLACE:
                name = name.replace(ch, "_")
        name = os.path.normcase(name)
        if not name.isidentifier():
            raise ConfigError(f"Invalid name for target_name ({self._name!r})")
        self._internal_name = name


class ConstantsModule:
    def __init__(
        self,
        release_string: Optional[str] = None,
        copyright_string: Optional[str] = None,
        module_name: str = "BUILD_CONSTANTS",
        time_format: str = "%B %d, %Y %H:%M:%S",
        constants: Optional[List[str]] = None,
    ):
        self.module_name = module_name
        self.time_format = time_format
        self.values = {}
        self.values["BUILD_RELEASE_STRING"] = release_string
        self.values["BUILD_COPYRIGHT"] = copyright_string
        if constants:
            for constant in constants:
                parts = constant.split("=", maxsplit=1)
                if len(parts) == 1:
                    name = constant
                    value = None
                else:
                    name, string_value = parts
                    value = eval(string_value)
                if (not name.isidentifier()) or iskeyword(name):
                    raise ConfigError(
                        f"Invalid constant name in ConstantsModule ({name!r})"
                    )
                self.values[name] = value

    def Create(self, finder):
        """Create the module which consists of declaration statements for each
        of the values."""
        today = datetime.datetime.today()
        source_timestamp = 0
        for module in finder.modules:
            if module.file is None:
                continue
            if module.source_is_zip_file:
                continue
            if not os.path.exists(module.file):
                raise ConfigError(
                    f"No file named {module.file} (for module {module.name})"
                )
            timestamp = os.stat(module.file).st_mtime
            source_timestamp = max(source_timestamp, timestamp)
        stamp = datetime.datetime.fromtimestamp(source_timestamp)
        self.values["BUILD_TIMESTAMP"] = today.strftime(self.time_format)
        self.values["BUILD_HOST"] = socket.gethostname().split(".")[0]
        self.values["SOURCE_TIMESTAMP"] = stamp.strftime(self.time_format)
        source_parts = []
        names = list(self.values.keys())
        names.sort()
        for name in names:
            value = self.values[name]
            source_parts.append(f"{name} = {value!r}")
        filename = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.py")
        with open(filename, "w") as fp:
            fp.write("\n".join(source_parts))
        module = finder.IncludeFile(filename, self.module_name)
        os.remove(filename)
        return module


class VersionInfo:
    def __init__(
        self,
        version,
        internalName=None,
        originalFileName=None,
        comments=None,
        company=None,
        description=None,
        copyright=None,
        trademarks=None,
        product=None,
        dll=False,
        debug=False,
        verbose=True,
    ):
        parts = version.split(".")
        while len(parts) < 4:
            parts.append("0")
        self.version = ".".join(parts)
        self.internal_name = internalName
        self.original_filename = originalFileName
        self.comments = comments
        self.company = company
        self.description = description
        self.copyright = copyright
        self.trademarks = trademarks
        self.product = product
        self.dll = dll
        self.debug = debug
        self.verbose = verbose
