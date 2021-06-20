import os
import subprocess
import stat
from typing import List, Dict, Optional, Set, Iterable

from .exception import DarwinException
from .freezeutil import _norm_path

# In a MachO file, need to deal specially with links that use @executable_path,
# @loader_path, @rpath
#
# @executable_path - where ultimate calling executable is
# @loader_path - directory of current object
# @rpath - list of paths to check
# (earlier rpaths have higher priority, i believe)
#
# Resolving these variables (particularly @rpath) requires tracing through the
# sequence linked MachO files leading the the current file, to determine which
# directories are included in the current rpath.


def _isMachOFile(path: str) -> bool:
    """Determines whether the file is a Mach-O file."""
    if not os.path.isfile(path):
        return False
    p = subprocess.Popen(("file", path), stdout=subprocess.PIPE)
    if b"Mach-O" in p.stdout.readline():
        return True
    return False


class DarwinFileData:
    """
    A DarwinFile object represents a file that will be copied into the
    application, and record where it was ultimately moved to in the application
    bundle. Mostly used to provide special handling for copied files that are
    Mach-O files.
    """

    def __init__(
        self,
        originalFilePath: str,
        linkedFrom: Optional["DarwinFileData"] = None,
        strictRPath: bool = False,
    ):
        """
        :param originalFilePath: The original path of the DarwinFile (before
        copying into app)
        :param linkedFrom: DarwinFile object representing the referencing
        source file
        :param strictRPath: Do not make guesses about rpath resolution.  If the
        load does not resolve, throw an Exception.
        """
        self.originalFilePath = _norm_path(originalFilePath)
        self.linkedFrom: Optional[DarwinFileData] = linkedFrom
        self.strictRPath = strictRPath

        # commands in a Mach-O file
        self.commands: List[MachOCommand] = []
        self.loadCommands: List[MachOLoadCommand] = []
        self.rpathCommands: List[MachORPathCommand] = []

        # note: if file gets referenced twice (or more), it will only be the
        # first reference that gets recorded.
        # mapping of raw load paths to absolute resolved paths
        # (or None, if no resolution was determined)
        self.libraryPathResolution: Dict[str, Optional[str]] = {}
        # the is of entries in the rpath in effect for this file.
        self._rpath: Optional[List[str]] = None

        self.isMachO = False

        if not _isMachOFile(path=self.originalFilePath):
            self._rpath = []
            return

        # if this is a MachO file, extract linking information from it
        self.isMachO = True
        self.commands = MachOCommand._getMachOCommands(
            forFileAtPath=self.originalFilePath
        )
        self.loadCommands = [
            c for c in self.commands if isinstance(c, MachOLoadCommand)
        ]
        self.rpathCommands = [
            c for c in self.commands if isinstance(c, MachORPathCommand)
        ]
        self.linkedFrom = linkedFrom

        self.getRPath()
        self.resolveLibraryPaths()

        return

    def __str__(self):
        l = []
        # l.append("RPath Commands: {}".format(self.rpathCommands))
        # l.append("Load commands: {}".format(self.loadCommands))
        l.append(f"Mach-O File: {self.originalFilePath}")
        l.append("Resolved rpath:")
        for rp in self.getRPath():
            l.append(f"   {rp}")
        l.append("Loaded libraries:")
        for rp in self.libraryPathResolution:
            l.append("   {} -> {}".format(rp, self.libraryPathResolution[rp]))
        return "\n".join(l)

    def getResolvedPaths(self) -> List[str]:
        """Returns list of resolved rpaths."""
        resolved_paths: List[str] = []
        for raw, resolved in self.libraryPathResolution.items():
            if resolved is not None: resolved_paths.append(resolved)
            pass
        return resolved_paths

    def getRemainingRPaths(self) -> List[str]:
        """Returns remaining unresolved rpaths."""
        rpaths: List[str] = []
        for raw, resolved in self.libraryPathResolution.items():
            if resolved is None:
                if not raw.startswith("@rpath"):
                    raise DarwinException(f"Unresolved path that is not an @rpath: {raw}")
                rpaths.append(raw)
            pass
        return rpaths

    def fileReferenceDepth(self) -> int:
        """Returns how deep this Mach-O file is in the dynamic load order."""
        if self.linkedFrom is not None:
            return self.linkedFrom.fileReferenceDepth() + 1
        return 0

    def printFileInformation(self):
        """Prints information about the Mach-O file."""
        print(f'[{self.fileReferenceDepth()}] File: "{self.originalFilePath}"')
        print("  Commands:")
        if len(self.commands) > 0:
            for c in self.commands:
                print(f"    {c}")
        else:
            print("    [None]")

        print("  RPath commands:")
        if len(self.rpathCommands) > 0:
            for rpc in self.rpathCommands:
                print(f"    {rpc}")
        else:
            print("    [None]")
        print("  Calculated RPath:")
        rpath = self.getRPath()
        if len(rpath) > 0:
            for path in rpath:
                print(f"    {path}")
        else:
            print("    [None]")
        if self.linkedFrom is not None:
            print("Referenced from:")
            self.linkedFrom.printFileInformation()

    def getBaseName(self) -> str:
        return os.path.basename(self.originalFilePath)

    @staticmethod
    def isExecutablePath(path: str) -> bool:
        return path.startswith("@executable_path")

    @staticmethod
    def isLoaderPath(path: str) -> bool:
        return path.startswith("@loader_path")

    @staticmethod
    def isRPath(path: str) -> bool:
        return path.startswith("@rpath")

    def sourceDir(self) -> str:
        return os.path.dirname(self.originalFilePath)

    def resolveLoader(self, path: str) -> Optional[str]:
        """Resolve a path that includes @loader_path.
        @loader_path represents the directory in which the DarwinFile is
        located."""
        if self.isLoaderPath(path=path):
            return path.replace("@loader_path", self.sourceDir(), 1)
        raise DarwinException(f"resolveLoader() called on bad path: {path}")

    def resolveExecutable(self, path: str) -> str:
        """
        @executable_path should resolve to the directory where the original
        executable was located. By default, we set that to the directory of the
        library, so it would resolve in the same was as if linked from an
        executable in the same directory.
        """
        # consider making this resolve to the directory of the target script
        # instead?
        if self.isExecutablePath(path=path):
            return path.replace("@executable_path", self.sourceDir(), 1)
        raise DarwinException(
            f"resolveExecutable() called on bad path: {path}"
        )

    def resolveRPath(self, path: str) -> Optional[str]:
        for rp in self.getRPath():
            testPath = os.path.abspath(path.replace("@rpath", rp, 1))
            if _isMachOFile(testPath):
                return testPath
        if not self.strictRPath:
            # If not strictly enforcing rpath, return None here, and leave any error to
            # .finalizeReferences() instead.
            return None
        print(f"\nERROR: Problem resolving RPath [{path}] in file:")
        self.printFileInformation()
        raise DarwinException(f"resolveRPath() failed to resolve path: {path}")

    def getRPath(self) -> List[str]:
        """
        Returns the rpath in effect for this file.  Determined by rpath
        commands in this file and (recursively) the chain of files that
        referenced this file.
        """
        if self._rpath is not None:
            return self._rpath
        rawPaths = [c.rPath for c in self.rpathCommands]
        #TODO: Are the rpathCommands allowed to include an @rpath based path?
        rpath = []
        for rp in rawPaths:
            if os.path.isabs(rp):
                rpath.append(rp)
            elif self.isLoaderPath(rp):
                rpath.append(self.resolveLoader(rp))
            elif self.isExecutablePath(rp):
                rpath.append(self.resolveExecutable(rp))


        rpath = [os.path.abspath(rp) for rp in rpath]
        rpath = [rp for rp in rpath if os.path.exists(rp)]

        if self.linkedFrom is not None:
            rpath = self.linkedFrom.getRPath() + rpath
        self._rpath = rpath
        return self._rpath

    def resolvePath(self, path) -> Optional[str]:
        """
        Resolves any @executable_path, @loader_path, and @rpath references
        in a path.
        """
        if self.isLoaderPath(path):  # replace @loader_path
            return self.resolveLoader(path)
        if self.isExecutablePath(path):  # replace @executable_path
            return self.resolveExecutable(path)
        if self.isRPath(path):  # replace @rpath
            return self.resolveRPath(path)
        if os.path.isabs(path):  # just use the path, if it is absolute
            return path
        # if None of the above, check if is a relative path from the directory of this file?
        testPath = os.path.abspath(os.path.join(self.sourceDir(), path))
        if _isMachOFile(path=testPath):
            return testPath
        raise DarwinException(f"Could not resolve path: {path}")

    def resolveLibraryPaths(self):
        for lc in self.loadCommands:
            rawPath = lc.loadPath
            resolvedPath = self.resolvePath(path=rawPath)
            self.libraryPathResolution[rawPath] = resolvedPath


class MachOCommand:
    """Represents a load command in a MachO file."""

    def __init__(self, lines: List[str]):
        self.lines = lines

    def displayString(self) -> str:
        l: List[str] = []
        if len(self.lines) > 0:
            l.append(self.lines[0].strip())
        if len(self.lines) > 1:
            l.append(self.lines[1].strip())
        return " / ".join(l)

    def __repr__(self):
        return f"<MachOCommand ({self.displayString()})>"

    @staticmethod
    def _getMachOCommands(forFileAtPath: str) -> List["MachOCommand"]:
        """
        Returns a list of load commands in the specified file, using otool.
        """
        shellCommand = f'otool -l "{forFileAtPath}"'
        commands: List[MachOCommand] = []
        currentCommandLines = None

        # split the output into separate load commands
        for line in os.popen(shellCommand):
            line = line.strip()
            if line[:12] == "Load command":
                if currentCommandLines is not None:
                    commands.append(
                        MachOCommand.parseLines(lines=currentCommandLines)
                    )
                currentCommandLines = []
            if currentCommandLines is not None:
                currentCommandLines.append(line)
        if currentCommandLines is not None:
            commands.append(MachOCommand.parseLines(lines=currentCommandLines))
        return commands

    @staticmethod
    def parseLines(lines: List[str]) -> "MachOCommand":
        if len(lines) < 2:
            return MachOCommand(lines=lines)
        commandLinePieces = lines[1].split(" ")
        if commandLinePieces[0] != "cmd":
            return MachOCommand(lines=lines)
        if commandLinePieces[1] == "LC_LOAD_DYLIB":
            return MachOLoadCommand(lines=lines)
        if commandLinePieces[1] == "LC_RPATH":
            return MachORPathCommand(lines=lines)
        return MachOCommand(lines=lines)


class MachOLoadCommand(MachOCommand):
    def __init__(self, lines: List[str]):
        super().__init__(lines=lines)
        self.loadPath = None
        if len(self.lines) < 4:
            return
        pathline = self.lines[3]
        pathline = pathline.strip()
        if not pathline.startswith("name "):
            return
        pathline = pathline[4:].strip()
        pathline = pathline.split("(offset")[0].strip()
        self.loadPath = pathline
        return

    def getPath(self):
        return self.loadPath

    def __repr__(self):
        return f"<LoadCommand path={self.loadPath!r}>"


class MachORPathCommand(MachOCommand):
    def __init__(self, lines: List[str]):
        super().__init__(lines=lines)
        self.rPath = None
        if len(self.lines) < 4:
            return
        pathline = self.lines[3]
        pathline = pathline.strip()
        if not pathline.startswith("path "):
            return
        pathline = pathline[4:].strip()
        pathline = pathline.split("(offset")[0].strip()
        self.rPath = pathline
        return

    def __repr__(self):
        return f"<RPath path={self.rPath!r}>"


def changeLoadReference(
    fileName: str, oldReference: str, newReference: str, VERBOSE: bool = True
):
    """
    Utility function that uses intall_name_tool to change oldReference to
    newReference in the machO file specified by fileName.
    """
    if VERBOSE:
        print("Redirecting load reference for ", end="")
        print(f"<{fileName}> {oldReference} -> {newReference}")
    original = os.stat(fileName).st_mode
    newMode = original | stat.S_IWUSR
    os.chmod(fileName, newMode)
    subprocess.call(
        ("install_name_tool", "-change", oldReference, newReference, fileName)
    )
    os.chmod(fileName, original)
    return

class DarwinFileTracker:
    """Object to track the DarwinFiles that have been added during a freeze."""

    def __init__(self):
        # list of DarwinFile objects for files being copied into project
        self._copiedFileList: List[DarwinFileData] = []

        # mapping of (build directory) target paths to DarwinFile objects
        self._darwinFileForBuildPath: Dict[str, DarwinFileData] = {}

        # mapping of (source location) paths to DarwinFile objects
        self._darwinFileForSourcePath: Dict[str, DarwinFileData] = {}
        return

    def __iter__(self) -> Iterable[DarwinFileData]:
        return iter(self._copiedFileList)

    def pathIsAlreadyCopiedTo(self, targetPath: str) -> bool:
        """Check if the given targetPath has already has a file copied to it."""
        if targetPath in self._darwinFileForBuildPath:
            return True
        return False

    def getDarwinFile(self, sourcePath: str, targetPath: str) -> DarwinFileData:
        """
        Gets the DarwinFile for file copied from sourcePath to targetPath.
        If either (i) nothing, or (ii) a different file has been copied to
        targetPath, raises a DarwinException.
        """
        # check that the file has been copied to
        if targetPath not in self._darwinFileForBuildPath:
            raise DarwinException(
                f"File {targetPath!r} already copied to, "
                "but no DarwinFile object found for it."
            )

        # check that the target file came from the specified source
        targetDarwinFile: DarwinFileData = self._darwinFileForBuildPath[targetPath]
        realSource = os.path.realpath(sourcePath)
        targetRealSource = os.path.realpath(targetDarwinFile.originalFilePath)
        if realSource != targetRealSource:
            # raise DarwinException(
            print(
                "*** WARNING ***\n"
                f"Attempting to copy two files to {targetPath!r}\n"
                f"source 1: {targetDarwinFile.originalFilePath!r} "
                f"(real: {targetRealSource!r})\n"
                f"source 2: {sourcePath!r} (real: {realSource!r})\n"
                "(This may be caused by including modules in the zip file "
                "that rely on binary libraries with the same name.)"
                "\nUsing only source 1."
            )
        return targetDarwinFile

    def recordCopiedFile(self, targetPath: str, darwinFile: DarwinFileData):
        """
        Record that a DarwinFile is being copied to a given path. If a
         file has been copied to that path, raise a DarwinException.
        """
        if self.pathIsAlreadyCopiedTo(targetPath=targetPath):
            raise DarwinException(
                "addFile() called with targetPath already copied to "
                f"(targetPath={targetPath!r})"
            )

        self._copiedFileList.append(darwinFile)
        self._darwinFileForBuildPath[targetPath] = darwinFile
        self._darwinFileForSourcePath[darwinFile.originalFilePath] = darwinFile

    def findDarwinFileForFilename(self, fileName: str) -> Optional[DarwinFileData]:
        """Attempts to locate a copied DarwinFile with the specified filename and returns that.
        Otherwise returns None."""
        for df in self._copiedFileList:
            if df.getBaseName() == fileName:
                return df
        return None

    def finalizeReferences(self):
        """
        This function does a final pass through the references for all the
        copied DarwinFiles and attempts to clean up any remaining references
        that are not already marked as copied.  It covers two cases where the
        reference might not be marked as copied:
        1) Files where _CopyFile was called without copyDependentFiles=True
           (in which the information would not have been added to the
            references at that time).
        2) Files with broken @rpath references.  We try to fix that up here by
           seeing if the relevant file was located *anywhere* as part of the
           freeze process.
        """
        for copiedFile in self._copiedFileList:  # DarwinFile
            for reference in copiedFile.getMachOReferenceList():
                if not reference.isCopied:
                    if reference.isResolved():
                        # if reference is resolve, simply check if the resolved
                        # path was otherwise copied and lookup the DarwinFile
                        # object.
                        realTargetPath = os.path.realpath(
                            reference.resolvedReferencePath
                        )
                        if realTargetPath in self._darwinFileForSourcePath:
                            reference.setTargetFile(
                                self._darwinFileForSourcePath[realTargetPath]
                            )
                    else:
                        # if reference is not resolved, look through the copied
                        # files and try to find a candidate, and use it if found.
                        potentialTarget = self.findDarwinFileForFilename(
                            fileName=os.path.basename(
                                reference.rawReferencePath
                            )
                        )
                        if potentialTarget is None:
                            # If we cannot find any likely candidate, fail.
                            print(
                                "\nERROR: Could not resolve RPath "
                                f"[{reference.rawReferencePath}] in file "
                                f"[{copiedFile.originalFilePath}], and could "
                                "not find any likely intended reference."
                            )
                            copiedFile.printFileInformation()
                            raise DarwinException(
                                f"finalizeReferences() failed to resolve path "
                                f"[{reference.rawReferencePath}] in file "
                                f"[{copiedFile.originalFilePath}]."
                            )
                        print(
                            f"WARNING: In file [{copiedFile.originalFilePath}]"
                            f" guessing that {reference.rawReferencePath} "
                            f"resolved to {potentialTarget.originalFilePath}."
                        )
                        reference.resolvedReferencePath = (
                            potentialTarget.originalFilePath
                        )
                        reference.setTargetFile(potentialTarget)
