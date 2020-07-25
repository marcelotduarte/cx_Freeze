import os
import subprocess
import stat
from typing import List, Dict, Optional, Set, Iterable


# In a MachO file, need to deal specially with links that use @executable_path,
# @loader_path, @rpath
#
# @executable_path - where ultimate calling executable is
# @loader_path - directory of current object
# @rpath - list of paths to check (earlier rpaths have higher priority, i believe)
#
# Resolving these variables (particularly @rpath) requires tracing through the sequence
# linked MachO files leading the the current file, to determine which directories are
# included in the current rpath.

class DarwinException(Exception):
    pass

def _isMachOFile(path: str) -> bool:
    """Determines whether the file is a Mach-O file."""
    if not os.path.isfile(path):
        return False
    p = subprocess.Popen(("file", path), stdout=subprocess.PIPE)
    if "Mach-O" in p.stdout.readline().decode():
        return True
    return False

class MachOReference:
    """Represents a linking reference from MachO file to another file."""
    def __init__(self, sourceFile: "DarwinFile", rawPath: str, resolvedPath: str):
        self.sourceFile: "DarwinFile" = sourceFile
        self.rawPath: str = rawPath
        self.resolvedPath: str = resolvedPath

        # isSystemFile is True if the target is a system file that will not be
        # included in package
        self.isSystemFile = False
        # True if the file is being copied into the package
        self.isCopied = False
        # reference to target DarwinFile (but only if file is copied into app)
        self.targetFile: Optional[DarwinFile] = None
        return

    def setTargetFile(self, darwinFile: "DarwinFile"):
        self.targetFile = darwinFile
        self.isCopied = True
        return

class DarwinFile:
    """A DarwinFile object tracks a file referenced in the application, and record where it was
    ultimately moved to in the application bundle. Should also save a copy of the DarwinFile
    object, if any!, created for each referenced library."""

    def __init__(self, originalObjectPath: str,
                 referencingFile: Optional["DarwinFile"]=None):
        self.originalObjectPath = os.path.abspath( originalObjectPath )
        self.copyDestinationPath: Optional[str] = None
        self.commands: List[MachOCommand] = []
        self.loadCommands: List[MachOLoadCommand] = []
        self.rpathCommands: List[MachORPathCommand] = []
        self.referencingFile: Optional[DarwinFile] = None
        self.libraryPathResolution: Dict[str, str] = {}
        self._rpath: Optional[List[str]] = None
        self.machReferenceDict: Dict[str, MachOReference] = {}
        self.isMachO = False

        if not _isMachOFile(path=self.originalObjectPath):
            return

        self.isMachO = True
        self.commands = MachOCommand._getMachOCommands(path=self.originalObjectPath)
        self.loadCommands = [c for c in self.commands if isinstance(c, MachOLoadCommand)]
        self.rpathCommands = [c for c in self.commands if isinstance(c, MachORPathCommand)]
        self.referencingFile = referencingFile

        self.getRPath()
        self.resolveLibraryPaths()

        for rawPath, resolvedPath in self.libraryPathResolution.items():
            if resolvedPath in self.machReferenceDict:
                raise DarwinException("Dynamic libraries resolved to the same file?")
            self.machReferenceDict[resolvedPath] = MachOReference(sourceFile=self,
                                                                  rawPath=rawPath,
                                                                  resolvedPath=resolvedPath)
            pass
        return

    def __str__(self):
        l = []
        # l.append("RPath Commands: {}".format(self.rpathCommands))
        # l.append("Load commands: {}".format(self.loadCommands))
        l.append("Mach-O File: {}".format(self.originalObjectPath))
        l.append("Resolved rpath:")
        for rp in self.getRPath():
            l.append("   {}".format(rp))
            pass
        l.append("Loaded libraries:")
        for rp in self.libraryPathResolution:
            l.append("   {} -> {}".format(rp, self.libraryPathResolution[rp]))
            pass
        return "\n".join(l)

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
        return os.path.dirname( self.originalObjectPath )

    def resolveLoader(self, path:str) -> Optional[str]:
        if self.isLoaderPath(path=path):
            return path.replace("@loader_path", self.sourceDir(), 1)
        raise DarwinException("resolveLoader() called on bad path: {}".format(path))


    def resolveExecutable(self, path:str) -> str:
        if self.isExecutablePath(path=path):
            return path.replace("@executable_path", self.sourceDir(), 1)
        raise DarwinException("resolveExecutable() called on bad path: {}".format(path))

    def resolveRPath(self, path: str) -> str:
        for rp in self.getRPath():
            testPath = os.path.abspath( path.replace("@rpath", rp, 1) )
            if _isMachOFile(testPath):
                return testPath
            pass
        raise DarwinException("resolveRPath() failed to resolve path: {}".format(path))

    def getRPath(self) -> List[str]:
        """Returns the rpath in effect for this file."""
        if self._rpath is not None:
            return self._rpath
        rawPaths = [c.rPath for c in self.rpathCommands]
        rpath = []
        for rp in rawPaths:
            if os.path.isabs(rp): rpath.append(rp)
            elif self.isLoaderPath(rp): rpath.append(self.resolveLoader(rp))
            elif self.isExecutablePath(rp): rpath.append(self.resolveExecutable(rp))
            pass

        rpath = [os.path.abspath(rp) for rp in rpath]
        rpath = [rp for rp in rpath if os.path.exists(rp) ]

        if self.referencingFile is not None:
            rpath = self.referencingFile.getRPath() + rpath
            pass
        self._rpath = rpath
        return self._rpath

    def resolvePath(self, path) -> str:
        """Resolves any @executable_path, @loader_path, and @rpath references
        in a path."""
        if self.isLoaderPath(path):  # replace @loader_path
            return self.resolveLoader(path)
        if self.isExecutablePath(path):  # replace @executable_path
            return self.resolveExecutable(path)
        if self.isRPath(path):  # replace @rpath
            return self.resolveRPath(path)
        if os.path.isabs(path):  # just use the path, if it is absolute
            return path
        testPath = os.path.abspath( os.path.join(self.sourceDir(), path) )
        if _isMachOFile(path=testPath):
            return testPath
        raise DarwinException("Could not resolve path: {}".format(path))

    def resolveLibraryPaths(self):
        for lc in self.loadCommands:
            rawPath = lc.loadPath
            resolvedPath = self.resolvePath(path=rawPath)
            self.libraryPathResolution[rawPath]= resolvedPath
            pass
        return

    def getDependentFiles(self) -> List[str]:
        dependents: List[str] = []
        for rp,ref in self.machReferenceDict.items():
            dependents.append(ref.resolvedPath)
            pass
        return dependents

    def getMachOReference(self, resolvedPath: str) -> MachOReference:
        return self.machReferenceDict[resolvedPath]

    def setCopyDestination(self, destinationPath: str):
        """Tell the Mach-O file its relative position (compared to executable)
        in the bundled package."""
        self.copyDestinationPath = destinationPath
        return

    pass

class MachOCommand:
    """Represents a load command in a MachO file."""
    def __init__(self, lines: List[str]):
        self.lines = lines
        return

    def __repr__(self):
        return "<MachOCommand>"

    @staticmethod
    def _getMachOCommands(path) -> List["MachOCommand"]:
        """Returns a list of load commands in the specified file, using otool."""
        shellCommand = 'otool -l "{}"'.format(path)
        commands: List[MachOCommand] = []
        currentCommandLines = None

        # split the output into separate load commands
        for line in os.popen(shellCommand):
            line = line.strip()
            if line[:12] == "Load command":
                if currentCommandLines is not None:
                    commands.append(MachOCommand.parseLines(lines=currentCommandLines))
                    pass
                currentCommandLines = []
            if currentCommandLines is not None:
                currentCommandLines.append(line)
                pass
            pass
        if currentCommandLines is not None:
            commands.append(currentCommandLines)
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

    pass

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
        return "<LoadCommand path=\"{}\">".format(self.loadPath)

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
        return "<RPath path=\"{}\">".format(self.rPath)
    pass

def _printFile(darwinFile: DarwinFile, seenFiles: Set[DarwinFile],
               level: int, noRecurse=False):
    """Utility function to prints details about a DarwinFile and (optionally) recursively
    any other DarwinFiles that it references."""
    print("{}{} {}".format(level *"|  ", darwinFile.originalObjectPath,
                           "(already seen)" if noRecurse else ""))
    if noRecurse:
        return
    for path, ref in darwinFile.machReferenceDict.items():
        if not ref.isCopied: continue
        mf = ref.targetFile
        _printFile(mf, seenFiles=seenFiles, level=level+1, noRecurse=(mf in seenFiles))
        seenFiles.add(mf)
        pass
    return

def printMachOFiles(fileList: List[DarwinFile]):
    seenFiles = set()
    for mf in fileList:
        if mf not in seenFiles:
            seenFiles.add(mf)
            _printFile(mf, seenFiles=seenFiles, level=0)
            pass
        pass
    return

def changeLoadReference(fileName: str, oldReference: str, newReference: str,
                        VERBOSE: bool=True):
    """Utility function that uses intall_name_tool to change oldReference to
    newReference in the machO file specified by fileName."""
    if VERBOSE:
        print("Redirecting load reference for <{}> {} -> {}".format(fileName,
                                                                    oldReference,
                                                                    newReference))
    original = os.stat(fileName).st_mode
    newMode = original | stat.S_IWUSR
    os.chmod(fileName, newMode)
    subprocess.call(('install_name_tool', '-change', oldReference, newReference, fileName))
    os.chmod(fileName, original)
    return

class DarwinFileTracker:
    """Object to track the DarwinFiles that have been added during a freeze."""

    def __init__(self):
        self._targetFileList: List[DarwinFile] = []
        self._targetFileDict: Dict[str, DarwinFile] = {}
        return

    def __iter__(self) -> Iterable[DarwinFile]:
        return iter(self._targetFileList)

    def pathIsAlreadyCopiedTo(self, targetPath: str) -> bool:
        """Check if the given targetPath has already has a file copied to it."""
        if targetPath in self._targetFileDict: return True
        return False

    def getDarwinFile(self, sourcePath: str, targetPath: str) -> DarwinFile:
        """Gets the DarwinFile for file copied from sourcePath to targetPath. If either (i) nothing,
        or (ii) a different file has been copied to targetPath, raises a DarwinException."""

        # check that the file has been copied to
        if targetPath not in self._targetFileDict:
            raise DarwinException(
                "File \"{}\" already copied to, but no DarwinFile object found for it.".format(targetPath))

        # check that the target file came from the specified source
        targetDarwinFile: DarwinFile = self._targetFileDict[targetPath]
        realSource = os.path.realpath(sourcePath)
        targetRealSource = os.path.realpath(targetDarwinFile.originalObjectPath)
        if realSource != targetRealSource:
            exceptionString = \
"""Attempting to copy two files to "{}"
   source 1: "{}" (real: "{}")
   source 2: "{}" (real: "{}")
(This may be caused by including modules in the zip file that rely on binary libraries with the same name.)"""
            exceptionString = exceptionString.format( targetPath,
                                                      targetDarwinFile.originalObjectPath, targetRealSource,
                                                      sourcePath, realSource )

            raise DarwinException(exceptionString)
        return targetDarwinFile


    def addFile(self, targetPath:str, darwinFile: DarwinFile):
        """Record that a DarwinFile is being copied to a given path.  If the same file has already been copied
        to that path, do nothing. If a different file has been copied to that bath, raise a DarwinException."""
        if self.pathIsAlreadyCopiedTo(targetPath=targetPath):
            raise DarwinException("addFile() called with targetPath already copied to (targetPath=\"{}\")".format(targetPath))

        self._targetFileList.append(darwinFile)
        self._targetFileDict[targetPath] = darwinFile
        return