import os, shutil, stat, sys, textwrap
from abc import ABC, abstractmethod
from collections import deque
from typing import Tuple, List, Dict, Iterator, Optional, Deque, Callable

from .freezeutil import _norm_path
from .exception import FileTrackerException
from .darwintools2 import DarwinFileData

# TODO: Deal with
#  (1) cases where a special path is set just before marking file to copy (e.g., in _WriteModules) (extra path used for finding dependencies)
#  (2) dummy file for created files (so they are not copied initially, but are moved on a re-locate operation)
#  (3) relative_source (as part of dependency copying)

WEAK_WARNING = True


class ReasonProtocol(ABC):

    @abstractmethod
    def this_reason_string(self) -> str:
        return ""

    def __str__(self) -> str:
        return self.full_reason_string()

    def full_reason_string(self) -> str:
        l = []
        curReason = self
        n = 1
        while curReason is not None:
            l.append(f"{n:>2}) {curReason.this_reason_string()}")
            curReason = curReason.get_prior_reason()
            n += 1
            pass
        return "\n".join(l)

    def get_prior_reason(self) -> Optional["ReasonProtocol"]:
        return None

    def get_reason_depth(self) -> int:
        curReason: "ReasonProtocol" = self
        n = 0
        while curReason is not None:
            curReason = curReason.get_prior_reason()
            n += 1
        return n

class BaseReason(ReasonProtocol):
    def __init__(self, text: str):
        self.text = text

    def this_reason_string(self) -> str:
        return self.text


class LinkReason(ReasonProtocol):
    def __init__(self, fobj: "FileObject", prior_reason: ReasonProtocol):
        self.file_object: "FileObject" = fobj
        self.prior_reason = prior_reason

    def this_reason_string(self) -> str:
        return f"Linked from file: {self.file_object}"

    def get_prior_reason(self) -> Optional["ReasonProtocol"]:
        return self.prior_reason

class FileObject(ABC):
    """Abstract object representing a file included in frozen application.  Can also be used as a
    ReasonProtocol object, for files dynamically linked from this file."""
    def __init__(self,
                 reason: ReasonProtocol,
                 target_rel_paths: List[str] = None,
                 ):
        if target_rel_paths is None:
            self.target_rel_paths: List[str] = []
        else:
            self.target_rel_paths = target_rel_paths

        if reason is None:
            raise FileTrackerException("Reason must be provided for inclusion of each File Object.")
        if not isinstance(reason, ReasonProtocol):
            raise FileTrackerException(f"Bad reason object given: {repr(reason)}")

        self.reason_to_include: ReasonProtocol = reason
        self.reason_for_links = LinkReason(fobj=self, prior_reason=self.reason_to_include)
        return

    @abstractmethod
    def get_reason_name(self) -> str:
        """Returns a string identifying this file in reasons."""
        return ""

    def get_inclusion_reason(self) -> ReasonProtocol:
        """Returns the ReasonProtocol object explaining why file included."""
        return self.reason_to_include

    def get_inclusion_reason_string(self) -> str:
        """Returns a string explaining why this file was included."""
        return self.reason_to_include.full_reason_string()

    def get_reason_for_links(self) -> ReasonProtocol:
        return self.reason_for_links

    def add_target_rel_path(self, path: str):
        if path in self.target_rel_paths:
            if WEAK_WARNING: print(f"WARNING: Attempting to add a duplicate target: {path}")
            else: raise FileTrackerException(f"Attempting to add a duplicate target: {path}")
        self.target_rel_paths.append(path)
        return

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return "<FileObject>"

    @abstractmethod
    def copy_to(self, dest_root:str):
        return

    @staticmethod
    def remove_file(target_path: str):
        if os.path.exists(target_path):
            os.chmod(target_path, stat.S_IWRITE)
            os.remove(target_path)
            pass
        return

class RealFileObject(FileObject):
    """Represents a real file that should be copied into frozen application."""
    def __init__(self,
                 original_file_path: str,
                 reason: ReasonProtocol,
                 target_rel_paths: Optional[List[str]] = None,
                 linking_file: Optional["RealFileObject"] = None,
                 copy_links: bool = False,
                 include_mode: bool = False,
                 force_write_access: bool = False,
                 relative_source: bool = False,
                 ):
        """
        :param original_file_path: Path to source file.
        :param reason: The reason that this file is included in the
        :param target_rel_paths: List of relative paths where file should be copied (relative to the dest_root specified at the time of copying).
        :param linking_file: the real file that this file is linked to from (used to resolve rpaths on Darwin, and for reporting of why files added)
        :param copy_links: If True, also find and copy dynamic libraries linked by the file.
        :param include_mode: If True, copies over file mode information.
        :param force_write_access: If True, forces write access on copied file. (overrides include_mode)
        :param relative_source: If True, then (on Linux only), any dependencies of the file that are in a subdirectory of the directory containing this file, will be placed in the same position relative to this file.
        """
        super().__init__(target_rel_paths=target_rel_paths, reason=reason)
        self.original_file_path = original_file_path
        self.linking_file: Optional[RealFileObject] = linking_file
        self.copy_links = copy_links
        self.links_processed: bool = False  # set to True once links processed for file
        self.force_write_access = force_write_access
        self.include_mode = include_mode
        self.relative_source = relative_source

        # for speed, the darwin_file_data is created lazily, if/when it is needed to evaluate links.
        self.darwin_file_data: Optional[DarwinFileData] = None

        return

    def __str__(self):
        return f"<File {self.original_file_path} -> {self.target_rel_paths}>"

    def __repr__(self) -> str:
        return str(self)

    def get_reason_name(self) -> str:
        """Returns a string identifying this file in reasons."""
        return f"Dynamnically linked from: {self.original_file_path}"

    def provide_linking_file(self, linking_file: "RealFileObject"):
        """If no linking file currently specified, use the specified file as the source link."""
        if self.linking_file is None:
            self.linking_file = linking_file
        return

    def get_original_path(self) -> str:
        return self.original_file_path

    def get_target_paths(self) -> List[str]:
        return self.target_rel_paths

    def get_linked_paths(self) -> List[str]:
        if sys.platform == "darwin":
            if self.darwin_file_data is None:
                self.darwin_file_data = DarwinFileData(
                    originalFilePath=self.original_file_path,
                    linkedFrom=None if (
                            self.linking_file is None) else self.linking_file.darwin_file_data,
                    strictRPath=False)
            return self.darwin_file_data.getResolvedPaths()
        elif sys.platform == "win32":
            #TODO: Complete this code for Windows / Linux (move over code from Freezer _GetDependentFiles)
            raise FileTrackerException("Need to implement")
        elif sys.platform == "linux":
            raise FileTrackerException("Need to implement")
        raise FileTrackerException(f"Unknown platform: {sys.platform}")

    def copy_to(self, dest_root:str):
        """
        Copy the file into the specified target location relative to dest_path
        """
        abs_dest_root = os.path.abspath(dest_root)
        for tpath in self.target_rel_paths:
            abs_target_path = os.path.join(abs_dest_root, tpath)
            #ensure target path exists
            os.makedirs(os.path.dirname(abs_target_path), exist_ok=True)
            self.remove_file(abs_target_path)
            shutil.copyfile(self.original_file_path, abs_target_path)
            shutil.copystat(self.original_file_path, abs_target_path)
            if self.include_mode:
                shutil.copymode(self.original_file_path, abs_target_path)
            if self.force_write_access:
                if not os.access(abs_target_path, os.W_OK):
                    mode = os.stat(abs_target_path).st_mode
                    os.chmod(abs_target_path, mode | stat.S_IWUSR)
        return

class VirtualFileObject(FileObject):
    """Represents a file that should be created in frozen application, with specified content."""
    def __init__(self,
                 data: bytes,
                 reason: ReasonProtocol,
                 target_rel_paths: Optional[List[str]],
                 ):
        super().__init__(target_rel_paths=target_rel_paths, reason=reason)
        self.data: bytes = data
        return

    def __str__(self):
        return f"<VirtualFile {len(self.data)} bytes -> {self.target_rel_paths}>"

    def get_reason_name(self) -> str:
        """Returns a string identifying this file in reasons."""
        return f"Dynamnically linked from file dynamically created at: {self.target_rel_paths}"


    def copy_to(self, dest_root:str):
        """
        Copy the file into the specified target location relative to dest_path
        """
        abs_dest_root = os.path.abspath(dest_root)
        for tpath in self.target_rel_paths:
            target_abs_path = os.path.join(abs_dest_root, tpath)
            os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
            self.remove_file(target_abs_path)
            with open(target_abs_path, "wb") as f:
                f.write(self.data)
        return

class FileTracker:
    def __init__(self, copy_check_callback: Callable[[str], bool]):
        """
        :param copy_check_callback: A callback function to call to determine whether file as a specified path
                                    should be included in frozen application.
        """
        self.copy_check_callback = copy_check_callback
        # a dictionary of RealFileObjects by noramlized source path
        self.real_files: Dict[str, RealFileObject] = {}
        # a list of all File Objects created so far
        self.all_files: List[FileObject] = []
        # maps target paths to source File Objects
        self.source_for_target_path: Dict[str, FileObject] = {}
        self.links_check_queue: Deque[RealFileObject] = deque()
        return

    def print_copy_report(self):
        """Print a list of files copied into frozen application."""
        source_paths = list(self.real_files.keys())
        source_paths.sort()
        print("Source files copied:")
        for p in source_paths:
            print(f'  {p}')
        return

    def print_reasons_report(self):
        """Print a list of files copied into frozen application, as well as the reason that each file was included."""
        print("Reasons for including files:")
        n = 1
        REPORT_INDENT = 6
        wrapper = textwrap.TextWrapper(
            initial_indent=" " * REPORT_INDENT,
            width=100,
            subsequent_indent=" " * (REPORT_INDENT+3))
        def print_reasons(fobj: FileObject):
            reason_string = fobj.get_inclusion_reason().full_reason_string()
            reason_paras = reason_string.split("\n")
            for para in reason_paras:
                lines = wrapper.wrap(para)
                for line in lines: print(line)
            return

        for fobj in self.all_files:
            if isinstance(fobj, RealFileObject):
                print(f"   ({n:<5}) {fobj.original_file_path}:")
                print_reasons(fobj)
            elif isinstance(fobj, VirtualFileObject):
                print(f"   ({n:<5}) Created file -> {fobj.target_rel_paths}:")
                print_reasons(fobj)
            else:
                print("f  Unknown file type (?): {fobj}")
            n += 1
        return

    def file_is_marked_to_copy(self, source_path: str) -> bool:
        """Returns True if the specified file is already marked for copying,
        else False."""
        np = _norm_path(source_path)
        if np not in self.real_files:
            return False
        else:
            rf = self.real_files[np]
            if len(rf.get_target_paths()) > 0: return True
        return False

    def file_object_for_source_path(self, source_path: str) -> RealFileObject:
        """Gets the FileObject for a file marked for copying."""
        np = _norm_path(source_path)
        if np not in self.real_files:
            raise FileTrackerException("Attempt to get file object for file where no " 
                                  f"FileObject created: {source_path}")
        return self.real_files[np]

    def queue_for_links_check(self, fobj: RealFileObject):
        self.links_check_queue.append(fobj)
        return

    def mark_file(self,
                  original_file_path: str,
                  to_rel_path: Optional[str],
                  reason: ReasonProtocol,
                  copy_links: bool = False,
                  force_write_access: bool = False,
                  include_mode: bool = False,
                  relative_source: bool = False,
                  prioritize_links: bool = False,
                  ) -> FileObject:
        """Mark that file at fromLocation should be copied to toLocation in the
        target directory.  Returns the FileObject created to represent the file.
        :param original_file_path: The full path to the source file.
        :param to_rel_path: The relative path in the target directory (can be None, if we do not actually want to copy
                            this file, and just want to copy its links.
        :param copy_links: If True, files dynamically linked from this file are copied
        :param prioritize_links: If True, prioritize checking links for this file (do it before unprioritized files).
        :param reason: If specified, a ReasonProtocol object specifying why the file is being included.
        """
        # TODO: what was the point of this?
        if os.path.basename(original_file_path).startswith("Python"):
            print(f'{original_file_path} -> {to_rel_path}');
            print("Copying python")
            # raise FileTrackerException

        normalized_source = _norm_path(original_file_path)
        if to_rel_path is not None:
            to_rel_path = os.path.normcase(os.path.normpath(to_rel_path))

        if normalized_source in self.real_files:
            # file object already created for the source.
            # just add a new copying destination (if applicable) and mark to
            # copy dependencies
            realfile = self.real_files[normalized_source]
            if to_rel_path is not None:
                realfile.add_target_rel_path(path=to_rel_path)
                self.source_for_target_path[to_rel_path] = realfile
            if realfile.copy_links is False and copy_links:
                realfile.copy_links = True
            if prioritize_links:
                self.queue_for_links_check(realfile)
            return realfile

        if to_rel_path in self.source_for_target_path:
            msg = f"Attempting to copying second file to same " + \
                  f"destination: {original_file_path}->{to_rel_path} " + \
                  f"(other: {self.source_for_target_path[to_rel_path]}"
            if WEAK_WARNING: print(f"WARNING: {msg}")
            else: raise FileTrackerException(msg)

        if to_rel_path is None: target_paths = []
        else: target_paths = [to_rel_path]

        # if reason is None: reason = BaseReason("No reason specified (?)")

        realfile = RealFileObject(original_file_path=normalized_source,
                                  reason=reason,
                                  target_rel_paths=target_paths,
                                  copy_links=copy_links,
                                  force_write_access=force_write_access,
                                  include_mode=include_mode,
                                  relative_source=relative_source)
        self.real_files[normalized_source] = realfile
        self.all_files.append(realfile)
        if to_rel_path is not None:
            self.source_for_target_path[to_rel_path] = realfile
        if prioritize_links:
            self.queue_for_links_check(realfile)

        return realfile

    def mark_file_to_create(self,
                            to_rel_path: str,
                            data: bytes,
                            reason: ReasonProtocol,
                            ) -> FileObject:
        """
        Record that a file should be created at a specified location with specified contents. Returns FileObject
        representing the created file.
        """
        to_rel_path = _norm_path(to_rel_path)
        if to_rel_path in self.source_for_target_path:
            # TODO, simply update options on the FileObject
            raise FileTrackerException("Attempting to create second file a location "
                                  f'\n target: {to_rel_path}')

        # if reason is None: reason = BaseReason("No reason specified (?)")

        fobj = VirtualFileObject(reason=reason,
                                 target_rel_paths=[to_rel_path],
                                 data = data)
        self.all_files.append(fobj)
        self.source_for_target_path[to_rel_path] = fobj
        return fobj

    def add_links(self):
        """Go through files marked to have links copied, and determine and
        add any additional files that are dynamically linked."""

        # ensure that all files to be copied with links are put in queue for processing
        # (files with prioritize_links=True will already be in queue)
        for fobj in self.all_files:
            if isinstance(fobj, RealFileObject) and fobj.copy_links:
                self.queue_for_links_check(fobj=fobj)

        # process files in the queue until empty
        print("Adding dependencies for:")
        while len(self.links_check_queue) > 0:
            fobj = self.links_check_queue.popleft()
            print(f"  {fobj}")
            self.add_links_for_file(subject_file=fobj)
            pass
        return

    def add_links_for_file(self, subject_file: RealFileObject):
        """Add the dynamic links for the file."""
        # return if links not supposed to be copied, or if links already processed for file
        if not subject_file.copy_links or subject_file.links_processed:
            return

        subject_file.links_processed = True  # record that subject_file is now having links processed

        linked_paths = subject_file.get_linked_paths()
        for path in linked_paths:
            path = _norm_path(path)
            # if file has been marked for exclusion, skip over it
            # TODO: we should maybe make a no-copying, non-linking file for this case, so the file at least appears in
            #  self.real_files, when the time comes up update the links.
            if not self.copy_check_callback(path):
                continue
            # if we are already planning to copy file, just making sure its links are copied
            if path in self.real_files:
                linked_file = self.real_files[path]
                if len(linked_file.get_target_paths()) == 0:
                    raise FileTrackerException("Linking to a file not being copied anywhere.")
                    #TODO: In this case, presumably we should just add a copy target?
                linked_file.copy_links = True  # set links on target file to be copied.
                linked_file.linking_file = subject_file
                self.queue_for_links_check(linked_file)
                pass
            else: # otherwise, need to create a new file object.
                target_path = os.path.basename(path) # TODO: need to update this with appropriate path
                linked_file = RealFileObject(original_file_path=path,
                                             target_rel_paths=[target_path],
                                             linking_file=subject_file,
                                             copy_links=True,
                                             include_mode=subject_file.include_mode,
                                             force_write_access=subject_file.force_write_access,
                                             relative_source=subject_file.relative_source)
                self.all_files.append( linked_file )
                self.real_files[path] = linked_file
                #TODO: Need to check if that target is already used, an find a non-conflicting name
                self.source_for_target_path[target_path] = linked_file
                self.queue_for_links_check(linked_file)
                pass
        return

    def copy_all_files(self, dest_root: str):
        """Copies all marked files into the target directory."""
        # print("All files to copy:")
        # print(self.all_files)
        for fobj in self.all_files:
            print(f'Copying: {fobj}')
            fobj.copy_to(dest_root=dest_root)
            pass
        return

    def fixup_dynamic_links(self, path: str):
        """Where necessary, fixes dynamic links appearing in copied files.
        Only required for Darwin.
        :param path: The location where all the files are located when doing the fixup
        (this is different from target_directory, since files will have been copied into
        app bundle directory)
        """

        if sys.platform != "darwin":
            return

        # TODO: complete this
        #       needs to update the dynamic links in each of the copied MachO files.  Also need to detect @rpaths that were not yet
        #       resolved, and make guesses (based on set of files being copied)

        return