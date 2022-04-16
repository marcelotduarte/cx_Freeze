"""A collection of functions which are triggered automatically by finder when
certain packages are included or not found."""
# pylint: disable=unused-argument,invalid-name,too-many-lines

import collections.abc
import os
import sys
import sysconfig
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from typing import List, Optional, Tuple

from .common import code_object_replace
from .finder import ModuleFinder
from .module import Module

MINGW = sysconfig.get_platform().startswith("mingw")
WIN32 = sys.platform == "win32"


def initialize(finder: ModuleFinder) -> None:
    """Upon initialization of the finder, this routine is called to set up some
    automatic exclusions for various platforms."""
    # py2 modules that have been removed or renamed in py3
    for name in collections.abc.__all__:
        finder.exclude_module(f"collections.{name}")
    for name in (
        "Charset",
        "Encoders",
        "Errors",
        "FeedParser",
        "Generator",
        "Header",
        "Iterators",
        "Message",
        "Parser",
        "Utils",
        "base64MIME",
        "quopriMIME",
    ):
        finder.exclude_module(f"email.{name}")
    finder.exclude_module("__builtin__")
    finder.exclude_module("__main__")
    finder.exclude_module("_winreg")
    finder.exclude_module("audiodev")
    finder.exclude_module("anydbm")
    finder.exclude_module("BaseHTTPServer")
    finder.exclude_module("Bastion")
    finder.exclude_module("bsddb")
    finder.exclude_module("cPickle")
    finder.exclude_module("commands")
    finder.exclude_module("ConfigParser")
    finder.exclude_module("Cookie")
    finder.exclude_module("copy_reg")
    finder.exclude_module("cStringIO")
    finder.exclude_module("dbhash")
    finder.exclude_module("dircache")
    finder.exclude_module("dl")
    finder.exclude_module("dumbdbm")
    finder.exclude_module("dummy_thread")
    finder.exclude_module("FCNTL")
    finder.exclude_module("fl")
    finder.exclude_module("fm")
    finder.exclude_module("fpformat")
    finder.exclude_module("gl")
    finder.exclude_module("gdbm")
    finder.exclude_module("htmllib")
    finder.exclude_module("HTMLParser")
    finder.exclude_module("httplib")
    finder.exclude_module("hotshot")
    finder.exclude_module("ihooks")
    finder.exclude_module("imputil")
    finder.exclude_module("linuxaudiodev")
    finder.exclude_module("md5")
    finder.exclude_module("Nav")
    finder.exclude_module("new")
    finder.exclude_module("mutex")
    finder.exclude_module("Pickle")
    finder.exclude_module("Queue")
    finder.exclude_module("rexec")
    finder.exclude_module("robotparser")
    finder.exclude_module("sgmllib")
    finder.exclude_module("sha")
    finder.exclude_module("SocketServer")
    finder.exclude_module("statvfs")
    finder.exclude_module("StringIO")
    finder.exclude_module("sunaudiodev")
    finder.exclude_module("thread")
    finder.exclude_module("Tkinter")
    finder.exclude_module("toaiff")
    finder.exclude_module("urllib.quote")
    finder.exclude_module("urllib.quote_plus")
    finder.exclude_module("urllib.unquote")
    finder.exclude_module("urllib.unquote_plus")
    finder.exclude_module("urllib.urlencode")
    finder.exclude_module("urllib.urlopen")
    finder.exclude_module("urllib.urlretrieve")
    finder.exclude_module("urllib2")
    finder.exclude_module("urlparse")
    finder.exclude_module("user")
    finder.exclude_module("UserDict")
    finder.exclude_module("UserList")
    finder.exclude_module("UserString")
    finder.exclude_module("whichdb")
    # macos specfic removed in py3
    # https://docs.python.org/2.7/library/mac.html?highlight=removed
    finder.exclude_module("autoGIL")
    finder.exclude_module("Carbon")
    finder.exclude_module("ColorPicker")
    finder.exclude_module("EasyDialogs")
    finder.exclude_module("findertools")
    finder.exclude_module("FrameWork")
    finder.exclude_module("ic")
    finder.exclude_module("MacOS")
    finder.exclude_module("macostools")
    # macpython removed
    finder.exclude_module("aetools")
    finder.exclude_module("aepack")
    finder.exclude_module("aetypes")
    finder.exclude_module("applesingle")
    finder.exclude_module("buildtools")
    finder.exclude_module("cfmfile")
    finder.exclude_module("icopen")
    finder.exclude_module("macerros")
    finder.exclude_module("macresource")
    finder.exclude_module("PixMapWrapper")
    finder.exclude_module("videoreader")
    finder.exclude_module("W")
    # sgi removed
    finder.exclude_module("al")
    finder.exclude_module("imgfile")
    finder.exclude_module("jpeg")
    finder.exclude_module("cd")
    finder.exclude_module("sv")
    # internal modules
    finder.exclude_module("_frozen_importlib")
    finder.exclude_module("_frozen_importlib_external")
    finder.exclude_module("os.path")
    # confused names in Windows
    finder.exclude_module("multiprocessing.Pool")
    finder.exclude_module("multiprocessing.Process")
    # exclusion by platform/os
    if os.name == "nt":
        finder.exclude_module("fcntl")
        finder.exclude_module("grp")
        finder.exclude_module("pwd")
        finder.exclude_module("termios")
    else:
        finder.exclude_module("_overlapped")
        finder.exclude_module("_subprocess")
        finder.exclude_module("_winapi")
        finder.exclude_module("msilib")
        finder.exclude_module("msvcrt")
        finder.exclude_module("multiprocessing._multiprocessing")
        finder.exclude_module("nt")
        finder.exclude_module("nturl2path")
        finder.exclude_module("pyHook")
        finder.exclude_module("pythoncom")
        finder.exclude_module("pywintypes")
        finder.exclude_module("winerror")
        finder.exclude_module("winsound")
        finder.exclude_module("win32api")
        finder.exclude_module("win32con")
        finder.exclude_module("win32com.shell")
        finder.exclude_module("win32gui")
        finder.exclude_module("win32event")
        finder.exclude_module("win32evtlog")
        finder.exclude_module("win32evtlogutil")
        finder.exclude_module("win32file")
        finder.exclude_module("win32pdh")
        finder.exclude_module("win32pipe")
        finder.exclude_module("win32process")
        finder.exclude_module("win32security")
        finder.exclude_module("win32service")
        finder.exclude_module("win32stat")
        finder.exclude_module("win32wnet")
        finder.exclude_module("winreg")
        finder.exclude_module("wx.activex")
    if os.name != "posix":
        finder.exclude_module("posix")
    if sys.platform != "darwin":
        finder.exclude_module("ctypes.macholib.dyld")
        finder.exclude_module("mac")
        finder.exclude_module("macpath")
        finder.exclude_module("macurl2path")
        finder.exclude_module("_scproxy")
    if os.name != "os2":
        finder.exclude_module("os2")
        finder.exclude_module("os2emxpath")
        finder.exclude_module("_emx_link")
    if os.name != "ce":
        finder.exclude_module("ce")
    if os.name != "riscos":
        finder.exclude_module("riscos")
        finder.exclude_module("riscosenviron")
        finder.exclude_module("riscospath")
        finder.exclude_module("rourl2path")
    if not sys.platform.startswith("java"):
        finder.exclude_module("com.sun")
        finder.exclude_module("java")
        finder.exclude_module("org.python")
    if not sys.platform.startswith("OpenVMS"):
        finder.exclude_module("vms_lib")
    if "__pypy__" not in sys.builtin_module_names:
        finder.exclude_module("__pypy__")


def load_aiofiles(finder: ModuleFinder, module: Module) -> None:
    """The aiofiles must be loaded as a package."""
    finder.include_package("aiofiles")


def load_asyncio(finder: ModuleFinder, module: Module) -> None:
    """The asyncio must be loaded as a package."""
    finder.include_package("asyncio")


def load_babel(finder: ModuleFinder, module: Module) -> None:
    """The babel must be loaded as a package, and has pickeable data."""
    finder.include_package("babel")
    module.in_file_system = 1


def load_bcrypt(finder: ModuleFinder, module: Module) -> None:
    """The bcrypt package requires the _cffi_backend module
    (loaded implicitly."""
    finder.include_module("_cffi_backend")


def load_boto(finder: ModuleFinder, module: Module) -> None:
    """the boto package uses 'six' fake modules."""
    finder.exclude_module("boto.vendored.six.moves")


def load_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """The cElementTree module implicitly loads the elementtree.ElementTree
    module; make sure this happens."""
    finder.include_module("elementtree.ElementTree")


def load_ceODBC(finder: ModuleFinder, module: Module) -> None:
    """The ceODBC module implicitly imports both datetime and decimal;
    make sure this happens."""
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_certifi(finder: ModuleFinder, module: Module) -> None:
    """The certifi package, in python 3.7 and up, uses importlib.resources
    to locate the cacert.pem in zip packages.
    In previous versions, it is expected to be stored in the file system."""
    if module.in_file_system == 0:
        if sys.version_info < (3, 7):
            module.in_file_system = 1
            return
        cacert = Path(__import__("certifi").where())
        finder.zip_include_files(cacert, Path("certifi", cacert.name))


def load__cffi_backend(finder: ModuleFinder, module: Module) -> None:
    """Add the cffi metadata for _cffi_backend module."""
    module.update_distribution("cffi")


def load_cffi_cparser(finder: ModuleFinder, module: Module) -> None:
    """The cffi.cparser module can use a extension if present."""
    try:
        cffi = __import__("cffi", fromlist=["_pycparser"])
        pycparser = getattr(cffi, "_pycparser")
        finder.include_module(pycparser.__name__)
    except (ImportError, AttributeError):
        finder.exclude_module("cffi._pycparser")


def load_crc32c(finder: ModuleFinder, module: Module) -> None:
    """The google.crc32c module requires _cffi_backend module."""
    finder.include_module("_cffi_backend")


def load_clr(finder: ModuleFinder, module: Module) -> None:
    """The pythonnet package (imported as 'clr') needs Python.Runtime.dll
    in runtime."""
    dll_name = "Python.Runtime.dll"
    finder.include_files(module.file.parent / dll_name, Path("lib", dll_name))


def load_cryptography_hazmat_bindings__openssl(
    finder: ModuleFinder, module: Module
) -> None:
    """The cryptography module requires the _cffi_backend module."""
    finder.include_module("_cffi_backend")


def load_cryptography_hazmat_bindings__padding(
    finder: ModuleFinder, module: Module
) -> None:
    """The cryptography module requires the _cffi_backend module."""
    finder.include_module("_cffi_backend")


def load_Crypto_Cipher(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Cipher subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_Hash(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Hash subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_Math(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Math subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_Protocol(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Protocol subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_PublicKey(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.PublicKey subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_Util(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Util subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.include_package(module.name)


def load_Crypto_Util__file_system(
    finder: ModuleFinder, module: Module
) -> None:
    """The patch for pycryptodome package."""
    # WARNING: do not touch this code string
    code_to_inject = """
import os

def pycryptodome_filename(dir_comps, filename):
    import sys
    if dir_comps[0] != "Crypto":
        raise ValueError("Only available for modules under 'Crypto'")
    dir_comps = list(dir_comps) + [filename]
    root_lib = os.path.join(os.path.dirname(sys.executable), "lib")
    return os.path.join(root_lib, ".".join(dir_comps))
"""
    if module.in_file_system == 0 and module.code is not None:
        new_code = compile(code_to_inject, str(module.file), "exec")
        co_func = new_code.co_consts[2]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, constant in enumerate(consts):
            if isinstance(constant, type(code)) and constant.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the _ctypes module in Python 3.8+ requires an additional
    libffi dll to be present in the build directory."""
    if WIN32 and sys.version_info >= (3, 8) and not MINGW:
        dll_pattern = "libffi-*.dll"
        dll_dir = Path(sys.base_prefix, "DLLs")
        for dll_path in dll_dir.glob(dll_pattern):
            finder.include_files(dll_path, Path("lib", dll_path.name))


def load_cv2(finder: ModuleFinder, module: Module) -> None:
    """Versions of cv2 (opencv-python) above 4.5.3 require additional
    configuration files.

    Additionally, on Linux the opencv_python.libs directory is not
    copied across for versions above 4.5.3 unless the cv2 package is
    included."""
    finder.include_package("cv2")

    dest_dir = Path("lib", "cv2")
    cv2_dir = module.path[0]
    for path in cv2_dir.glob("config*.py"):
        finder.include_files(path, dest_dir / path.name)


def load_cx_Oracle(finder: ModuleFinder, module: Module) -> None:
    """The cx_Oracle module implicitly imports datetime; make sure this
    happens."""
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_datetime(finder: ModuleFinder, module: Module) -> None:
    """The datetime module implicitly imports time; make sure this happens."""
    finder.include_module("time")


def load_docutils_frontend(finder: ModuleFinder, module: Module) -> None:
    """The optik module is the old name for the optparse module; ignore the
    module if it cannot be found."""
    module.ignore_names.add("optik")


def load_dummy_threading(finder: ModuleFinder, module: Module) -> None:
    """The dummy_threading module plays games with the name of the threading
    module for its own purposes; ignore that here."""
    finder.exclude_module("_dummy_threading")


def load_flask_compress(finder: ModuleFinder, module: Module) -> None:
    """flask-compress requires its metadata."""
    module.update_distribution("Flask_Compress")


def load_ftplib(finder: ModuleFinder, module: Module) -> None:
    """The ftplib module attempts to import the SOCKS module; ignore this
    module if it cannot be found."""
    module.ignore_names.add("SOCKS")


def load_gevent(finder: ModuleFinder, module: Module) -> None:
    """The gevent must be loaded as a package."""
    finder.include_package("gevent")


def load_GifImagePlugin(finder: ModuleFinder, module: Module) -> None:
    """The GifImagePlugin module optionally imports the _imaging_gif module"""
    module.ignore_names.add("_imaging_gif")


def load_glib(finder: ModuleFinder, module: Module) -> None:
    """Ignore globals that are imported."""
    module.global_names.update(
        [
            "GError",
            "IOChannel",
            "IO_ERR",
            "IO_FLAG_APPEND",
            "IO_FLAG_GET_MASK",
            "IO_FLAG_IS_READABLE",
            "IO_FLAG_IS_SEEKABLE",
            "IO_FLAG_IS_WRITEABLE",
            "IO_FLAG_MASK",
            "IO_FLAG_NONBLOCK",
            "IO_FLAG_SET_MASK",
            "IO_HUP",
            "IO_IN",
            "IO_NVAL",
            "IO_OUT",
            "IO_PRI",
            "IO_STATUS_AGAIN",
            "IO_STATUS_EOF",
            "IO_STATUS_ERROR",
            "IO_STATUS_NORMAL",
            "Idle",
            "MainContext",
            "MainLoop",
            "OPTION_ERROR",
            "OPTION_ERROR_BAD_VALUE",
            "OPTION_ERROR_FAILED",
            "OPTION_ERROR_UNKNOWN_OPTION",
            "OPTION_FLAG_FILENAME",
            "OPTION_FLAG_HIDDEN",
            "OPTION_FLAG_IN_MAIN",
            "OPTION_FLAG_NOALIAS",
            "OPTION_FLAG_NO_ARG",
            "OPTION_FLAG_OPTIONAL_ARG",
            "OPTION_FLAG_REVERSE",
            "OPTION_REMAINING",
            "OptionContext",
            "OptionGroup",
            "PRIORITY_DEFAULT",
            "PRIORITY_DEFAULT_IDLE",
            "PRIORITY_HIGH",
            "PRIORITY_HIGH_IDLE",
            "PRIORITY_LOW",
            "Pid",
            "PollFD",
            "SPAWN_CHILD_INHERITS_STDIN",
            "SPAWN_DO_NOT_REAP_CHILD",
            "SPAWN_FILE_AND_ARGV_ZERO",
            "SPAWN_LEAVE_DESCRIPTORS_OPEN",
            "SPAWN_SEARCH_PATH",
            "SPAWN_STDERR_TO_DEV_NULL",
            "SPAWN_STDOUT_TO_DEV_NULL",
            "Source",
            "Timeout",
            "child_watch_add",
            "filename_display_basename",
            "filename_display_name",
            "filename_from_utf8",
            "get_application_name",
            "get_current_time",
            "get_prgname",
            "glib_version",
            "idle_add",
            "io_add_watch",
            "main_context_default",
            "main_depth",
            "markup_escape_text",
            "set_application_name",
            "set_prgname",
            "source_remove",
            "spawn_async",
            "timeout_add",
            "timeout_add_seconds",
        ]
    )


def load_googleapiclient(finder: ModuleFinder, module: Module) -> None:
    """Add the googleapiclient metadata for googleapiclient package."""
    module.update_distribution("google_api_python_client")


def load_googleapiclient_discovery(
    finder: ModuleFinder, module: Module
) -> None:
    """The googleapiclient.discovery module needs discovery_cache subpackage
    in file system."""
    discovery_cache = finder.include_package("googleapiclient.discovery_cache")
    discovery_cache.in_file_system = 1


def load_google_cloud_storage(finder: ModuleFinder, module: Module) -> None:
    """The google.cloud.storage package always uses the parent module."""
    finder.include_package("google.cloud")


def load_gtk__gtk(finder: ModuleFinder, module: Module) -> None:
    """The gtk._gtk module has a number of implicit imports."""
    finder.include_module("atk")
    finder.include_module("cairo")
    finder.include_module("gio")
    finder.include_module("pango")
    finder.include_module("pangocairo")


def load_h5py(finder: ModuleFinder, module: Module) -> None:
    """h5py module has a number of implicit imports"""
    finder.include_module("h5py.defs")
    finder.include_module("h5py.utils")
    finder.include_module("h5py._proxy")
    try:
        api_gen = __import__("h5py", fromlist=["api_gen"]).api_gen
        finder.include_module(api_gen.__name__)
    except (ImportError, AttributeError):
        pass
    finder.include_module("h5py._errors")
    finder.include_module("h5py.h5ac")


def load_h5py_wrapper(finder: ModuleFinder, module: Module) -> None:
    """h5py_wrapper module requires future and pytest-runner"""
    finder.include_module("future")
    finder.include_module("ptr")


def load_hashlib(finder: ModuleFinder, module: Module) -> None:
    """hashlib's fallback modules don't exist if the equivalent OpenSSL
    algorithms are loaded from _hashlib, so we can ignore the error."""
    module.ignore_names.update(["_md5", "_sha", "_sha256", "_sha512"])


def load_hdfdict(finder: ModuleFinder, module: Module) -> None:
    """hdfdict module requires h5py_wrapper and PyYAML"""
    finder.include_module("h5py_wrapper")
    finder.include_package("yaml")


def load_idna(finder: ModuleFinder, module: Module) -> None:
    """The idna module implicitly loads data; make sure this happens."""
    finder.include_module("idna.idnadata")


def load_lxml(finder: ModuleFinder, module: Module) -> None:
    """The lxml package uses an extension."""
    finder.include_module("lxml._elementpath")


def load_llvmlite(finder: ModuleFinder, module: Module) -> None:
    """The llvmlite must be loaded as package."""
    finder.include_package("llvmlite")
    finder.exclude_module("llvmlite.tests")


def load_matplotlib(finder: ModuleFinder, module: Module) -> None:
    """The matplotlib package requires mpl-data subdirectory."""
    data_path = module.path[0] / "mpl-data"
    target_path = Path("lib", module.name, "mpl-data")
    # After matplotlib 3.4 mpl-data is guaranteed to be a subdirectory.
    if not data_path.is_dir():
        data_path = __import__("matplotlib").get_data_path()
        need_patch = True
    else:
        need_patch = module.in_file_system == 0
    finder.include_files(data_path, target_path, copy_dependent_files=False)
    finder.include_package("matplotlib")
    finder.exclude_module("matplotlib.tests")
    finder.exclude_module("matplotlib.testing")
    if not need_patch or module.code is None:
        return
    code_to_inject = f"""
def _get_data_path():
    import os, sys
    return os.path.join(os.path.dirname(sys.executable), "{target_path!s}")
"""
    for code_str in [
        code_to_inject,
        code_to_inject.replace("_get_data_path", "get_data_path"),
    ]:
        new_code = compile(code_str, str(module.file), "exec")
        co_func = new_code.co_consts[0]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, constant in enumerate(consts):
            if isinstance(constant, type(code)) and constant.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy must be loaded as a package; support for pypi version and
    numpy+mkl version - tested with 1.19.5+mkl, 1.20.3+mkl, 1.21.0+mkl,
    1.21.1+mkl, 1.21.2+mkl and 1.21.2 from conda-forge."""
    finder.include_package("numpy")

    if WIN32:
        numpy_dir = module.path[0]
        # numpy+mkl from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
        libs_dir = numpy_dir / "DLLs"
        if not libs_dir.is_dir():
            # numpy+mkl from conda-forge
            libs_dir = Path(sys.base_prefix, "Library", "bin")
        if libs_dir.is_dir():
            dest_dir = Path("lib", "numpy_mkl")
            for path in libs_dir.glob("mkl_*.dll"):
                finder.include_files(path, dest_dir / path.name)
            for path in libs_dir.glob("lib*.dll"):
                finder.include_files(path, dest_dir / path.name)
            finder.add_constant("MKL_PATH", str(dest_dir))
            finder.exclude_module("numpy.DLLs")

            # do not check dependencies already handled
            extension = EXTENSION_SUFFIXES[0]
            for path in numpy_dir.rglob(f"*{extension}"):
                finder.exclude_dependent_files(path)

        # support for old versions (numpy <= 1.18.2)
        if module.in_file_system == 0:
            # copy any file at site-packages/numpy/.libs
            libs_dir = numpy_dir / ".libs"
            if libs_dir.is_dir():
                finder.include_files(libs_dir, "lib")

    # exclude the tests
    finder.exclude_module("numpy.compat.tests")
    finder.exclude_module("numpy.core.tests")
    finder.exclude_module("numpy.distutils.tests")
    finder.exclude_module("numpy.f2py.tests")
    finder.exclude_module("numpy.fft.tests")
    finder.exclude_module("numpy.lib.tests")
    finder.exclude_module("numpy.linalg.tests")
    finder.exclude_module("numpy.ma.tests")
    finder.exclude_module("numpy.matrixlib.tests")
    finder.exclude_module("numpy.polynomial.tests")
    finder.exclude_module("numpy.random._examples")
    finder.exclude_module("numpy.random.tests")
    finder.exclude_module("numpy.tests")
    finder.exclude_module("numpy.typing.tests")


def load_numpy_core_numerictypes(finder: ModuleFinder, module: Module) -> None:
    """The numpy.core.numerictypes module adds a number of items to itself
    dynamically; define these to avoid spurious errors about missing
    modules."""
    module.global_names.update(
        [
            "bool_",
            "cdouble",
            "complexfloating",
            "csingle",
            "double",
            "float64",
            "float_",
            "inexact",
            "intc",
            "int32",
            "number",
            "single",
        ]
    )


def load_numpy_distutils_command_scons(
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("numscons")


def load_numpy_distutils_misc_util(
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("numscons")


def load_numpy_distutils_system_info(
    finder: ModuleFinder, module: Module
) -> None:
    """The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("Numeric")


def load_numpy_f2py___version__(finder: ModuleFinder, module: Module) -> None:
    """The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found."""
    module.ignore_names.add("__svn_version__")


def load_numpy_linalg(finder: ModuleFinder, module: Module) -> None:
    """The numpy.linalg module implicitly loads the lapack_lite module; make
    sure this happens."""
    finder.include_module("numpy.linalg.lapack_lite")


def load_numpy_random_mtrand(finder: ModuleFinder, module: Module) -> None:
    """The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules."""
    module.global_names.update(["rand", "randn"])


def load_Numeric(finder: ModuleFinder, module: Module) -> None:
    """The Numeric module optionally loads the dotblas module; ignore the error
    if this modules does not exist."""
    module.ignore_names.add("dotblas")


def load_pandas(finder: ModuleFinder, module: Module) -> None:
    """The pandas has dynamic imports."""
    finder.include_package("pandas._libs")
    finder.exclude_module("pandas.tests")


def load_pikepdf(finder: ModuleFinder, module: Module) -> None:
    """The pikepdf must be loaded as a package."""
    finder.include_package("pikepdf")


def load_PIL(finder: ModuleFinder, module: Module) -> None:
    """The Pillow must be loaded as a package."""
    finder.include_package("PIL")


def load_plotly(finder: ModuleFinder, module: Module) -> None:
    """The plotly must be loaded as a package."""
    finder.include_package("plotly")


def load_pkg_resources(finder: ModuleFinder, module: Module) -> None:
    """The pkg_resources must be loaded as a package;
    dynamically loaded modules in subpackages is growing."""
    finder.include_package("pkg_resources")


def load_postgresql_lib(finder: ModuleFinder, module: Module) -> None:
    """The postgresql.lib module requires the libsys.sql file to be included
    so make sure that file is included."""
    filename = "libsys.sql"
    finder.include_files(module.path[0] / filename, filename)


def load_pty(finder: ModuleFinder, module: Module) -> None:
    """The sgi module is not needed for this module to function."""
    module.ignore_names.add("sgi")


def load_ptr(finder: ModuleFinder, module: Module) -> None:
    """pytest-runner requires its metadata"""
    module.update_distribution("pytest-runner")


def load_pycountry(finder: ModuleFinder, module: Module) -> None:
    """The pycountry module has data in subdirectories."""
    finder.exclude_module("pycountry.tests")
    module.in_file_system = 1


def load_pycparser(finder: ModuleFinder, module: Module) -> None:
    """These files are missing which causes
    permission denied issues on windows when they are regenerated."""
    finder.include_module("pycparser.lextab")
    finder.include_module("pycparser.yacctab")


def load_pydantic(finder: ModuleFinder, module: Module) -> None:
    """The pydantic package is compiled by Cython (the imports are hidden)."""
    finder.include_module("colorsys")
    finder.include_module("dataclasses")  # support in v 1.7+
    finder.include_module("datetime")
    finder.include_module("decimal")
    finder.include_module("functools")
    finder.include_module("ipaddress")
    finder.include_package("json")
    finder.include_module("pathlib")
    finder.include_module("typing_extensions")  # support in v 1.8
    finder.include_module("uuid")


def load_pygments(finder: ModuleFinder, module: Module) -> None:
    """The pygments package dynamically load styles."""
    finder.include_package("pygments.styles")
    finder.include_package("pygments.lexers")
    finder.include_package("pygments.formatters")


def load_pyodbc(finder: ModuleFinder, module: Module) -> None:
    """The pyodbc module implicitly imports others modules;
    make sure this happens."""
    for mod in ("datetime", "decimal", "hashlib", "locale", "uuid"):
        finder.include_module(mod)


def _qt_implementation(module: Module) -> str:
    """Helper function to get the name of the Qt implementation (PyQt5)."""
    return module.name.split(".")[0]


def _qt_library_paths(name: str) -> List[str]:
    """Cache the QtCore library paths."""
    if _qt_library_paths.data:
        return _qt_library_paths.data
    try:
        qtcore = __import__(name, fromlist=["QtCore"]).QtCore
    except RuntimeError:
        print("WARNING: Tried to load multiple incompatible Qt ", end="")
        print("wrappers. Some incorrect files may be copied.")
        qtcore = None
    else:
        data = [Path(p) for p in qtcore.QCoreApplication.libraryPaths()]
    if not data:
        # check the common location for conda
        plugins_path = Path(sys.base_prefix, "Library", "plugins")
        if plugins_path.exists():
            data.append(plugins_path)
        elif qtcore:
            # use a hack
            app = qtcore.QCoreApplication([])
            data = [Path(p) for p in app.libraryPaths()]
    if not data and qtcore:
        # Qt Plugins can be in a plugins directory next to the Qt libraries
        qt_root_dir = Path(qtcore.__file__).parent
        data.append(qt_root_dir / "plugins")
        data.append(qt_root_dir / "Qt5" / "plugins")
        data.append(qt_root_dir / "Qt" / "plugins")
    _qt_library_paths.data = data
    return data


_qt_library_paths.data: List[Path] = []


def get_qt_subdir_paths(name: str, subdir: str) -> List[Tuple[Path, Path]]:
    """Helper function to get a list of source and target paths of Qt
    subdirectories, indicated to be used in include_files."""
    include_files = []
    for library_dir in _qt_library_paths(name):
        if library_dir.parts[-1] == "plugins":
            library_dir = library_dir.parent
        source_path = library_dir / subdir
        if not source_path.exists():
            continue
        if library_dir.parts[-1] == name:  # {name}/{subdir}
            target_path = Path("lib") / name / subdir
        elif library_dir.parts[-2] == name:  # {name}/Qt*/{subdir}
            target_path = Path("lib") / name / library_dir.parts[-1] / subdir
        else:
            target_path = Path("lib") / name / "Qt" / subdir
        include_files.append((source_path, target_path))
    return include_files


def get_qt_plugins_paths(name: str, plugins: str) -> List[Tuple[str, str]]:
    """Helper function to get a list of source and target paths of Qt plugins,
    indicated to be used in include_files."""
    return get_qt_subdir_paths(name, str(Path("plugins", plugins)))


def copy_qt_data(name: str, subdir: str, finder: ModuleFinder) -> None:
    """Helper function to find and copy Qt resources, translations, etc."""
    for source_path, target_path in get_qt_subdir_paths(name, subdir):
        finder.include_files(source_path, target_path)


def copy_qt_plugins(name: str, plugins: str, finder: ModuleFinder) -> None:
    """Helper function to find and copy Qt plugins."""
    for source_path, target_path in get_qt_plugins_paths(name, plugins):
        finder.include_files(source_path, target_path)


def load_PyQt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5/PySide2 init to locate and load plugins."""
    if module.code is None:
        return
    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
    # With PySide2 the same happens in some versions.
    # So, this hack will be used to:
    # - fix empty libraryPaths
    # - workaround issues with anaconda
    # - locate plugins when using zip_include_packages
    name = _qt_implementation(module)
    code_string = module.file.read_text()
    code_string += f"""
# cx_Freeze patch start
import sys
from pathlib import Path
from {name}.QtCore import QCoreApplication

executable_dir = Path(sys.executable).parent
qt_root_dir = executable_dir / "lib" / "{name}"
plugins_dir = qt_root_dir / "Qt5" / "plugins"  # PyQt5 5.15.4
if not plugins_dir.is_dir():
    plugins_dir = qt_root_dir / "Qt" / "plugins"
if not plugins_dir.is_dir():
    plugins_dir = qt_root_dir / "plugins"
if plugins_dir.is_dir():
    QCoreApplication.addLibraryPath(plugins_dir.as_posix())
# cx_Freeze patch end
"""
    module.code = compile(code_string, str(module.file), "exec")
    if module.in_file_system == 0:
        module.in_file_system = 2  # use optimized mode
    finder.include_module(f"{name}.QtCore")  # imported by all modules


def load_PyQt5_phonon(finder: ModuleFinder, module: Module) -> None:
    """In Windows, phonon5.dll requires an additional dll phonon_ds94.dll to
    be present in the build directory inside a folder phonon_backend."""
    if WIN32:
        name = _qt_implementation(module)
        copy_qt_plugins(name, "phonon_backend", finder)


def load_PyQt5_Qt(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.Qt module is an extension module which imports a number of
    other modules and injects their namespace into its own. It seems a
    foolish way of doing things but perhaps there is some hidden advantage
    to this technique over pure Python; ignore the absence of some of
    the modules since not every installation includes all of them."""
    name = _qt_implementation(module)
    for mod in (
        "_qt",
        "QtSvg",
        "Qsci",
        "QtAssistant",
        "QtNetwork",
        "QtOpenGL",
        "QtScript",
        "QtSql",
        "QtSvg",
        "QtTest",
        "QtXml",
    ):
        try:
            finder.include_module(f"{name}.{mod}")
        except ImportError:
            pass


def load_PyQt5_QtCharts(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_PyQt5_QtCore(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module."""
    name = _qt_implementation(module)
    try:
        finder.include_module(f"{name}.sip")  # PyQt5 >= 5.11
    except ImportError:
        finder.include_module("sip")
    try:
        finder.include_module(f"{name}._qt")
    except ImportError:
        pass


def load_PyQt5_QtDataVisualization(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_PyQt5_QtGui(finder: ModuleFinder, module: Module) -> None:
    """There is a chance that QtGui will use some image formats, then, add the
    image format plugins."""
    name = _qt_implementation(module)
    copy_qt_plugins(name, "imageformats", finder)
    # On Qt5, we need the platform plugins. For simplicity, we just copy
    # any that are installed.
    copy_qt_plugins(name, "platforms", finder)
    copy_qt_plugins(name, "styles", finder)


def load_PyQt5_QtHelp(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_PyQt5_QtLocation(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtPositioning")


def load_PyQt5_QtMultimedia(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtMultimediaWidgets")
    copy_qt_plugins(name, "audio", finder)
    copy_qt_plugins(name, "mediaservice", finder)


def load_PyQt5_QtMultimediaWidgets(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtMultimedia")


def load_PyQt5_QtOpenGL(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "renderers", finder)


def load_PyQt5_QtPositioning(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    copy_qt_plugins(name, "position", finder)


def load_PyQt5_QtPrintSupport(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "printsupport", finder)


def load_PyQt5_QtQml(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    copy_qt_plugins(name, "qmltooling", finder)


def load_PyQt5_QtSCriptTools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    finder.include_module(f"{name}.QtScript")


def load_PyQt5_QtSql(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")
    copy_qt_plugins(name, "sqldrivers", finder)


def load_PyQt5_QtSvg(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_PyQt5_QtTest(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_PyQt5_QtUiTools(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWidgets")


def load_PyQt5_QtWebEngine(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebEngineCore")


def load_PyQt5_QtWebEngineCore(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")
    finder.include_module(f"{name}.QtNetwork")


def load_PyQt5_QtWebEngineWidgets(
    finder: ModuleFinder, module: Module
) -> None:
    """This module depends on another module, data and plugins."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtWebChannel")
    finder.include_module(f"{name}.QtWebEngineCore")
    finder.include_module(f"{name}.QtPrintSupport")
    if WIN32:
        copy_qt_data(name, "QtWebEngineProcess.exe", finder)
    else:
        copy_qt_data(name, "libexec", finder)
    copy_qt_data(name, "resources", finder)
    copy_qt_data(name, "translations", finder)
    copy_qt_plugins(name, "webview", finder)
    copy_qt_plugins(name, "xcbglintegrations", finder)


def load_PyQt5_QtWebKit(finder: ModuleFinder, module: Module) -> None:
    """This module depends on other modules."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    finder.include_module(f"{name}.QtGui")


def load_PyQt5_QtWebSockets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_PyQt5_QtWidgets(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtGui")


def load_PyQt5_QtXmlPatterns(finder: ModuleFinder, module: Module) -> None:
    """This module depends on another module."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")


def load_PyQt5_uic(finder: ModuleFinder, module: Module) -> None:
    """The uic module makes use of "plugins" that need to be read directly and
    cannot be frozen; the PyQt5.QtWebKit and PyQt5.QtNetwork modules are
    also implicity loaded."""
    name = _qt_implementation(module)
    finder.include_module(f"{name}.QtNetwork")
    try:
        finder.include_module(f"{name}.QtWebKit")
    except ImportError:
        pass
    source_dir = module.path[0] / "widget-plugins"
    finder.include_files(source_dir, f"{name}.uic.widget-plugins")


# PySide2 start
load_PySide2 = load_PyQt5
load_PySide2_Qt = load_PyQt5_Qt
load_PySide2_QtCharts = load_PyQt5_QtCharts
# load_PySide2_QtCore does not need to map
load_PySide2_QtDataVisualization = load_PyQt5_QtDataVisualization
load_PySide2_QtGui = load_PyQt5_QtGui
load_PySide2_QtHelp = load_PyQt5_QtHelp
load_PySide2_QtLocation = load_PyQt5_QtLocation
load_PySide2_QtMultimedia = load_PyQt5_QtMultimedia
load_PySide2_QtMultimediaWidgets = load_PyQt5_QtMultimediaWidgets
load_PySide2_QtOpenGL = load_PyQt5_QtOpenGL
load_PySide2_QtPositioning = load_PyQt5_QtPositioning
load_PySide2_QtPrintSupport = load_PyQt5_QtPrintSupport
load_PySide2_QtQml = load_PyQt5_QtQml
load_PySide2_QtSCriptTools = load_PyQt5_QtSCriptTools
load_PySide2_QtSql = load_PyQt5_QtSql
load_PySide2_QtSvg = load_PyQt5_QtSvg
load_PySide2_QtTest = load_PyQt5_QtTest
load_PySide2_QtUiTools = load_PyQt5_QtUiTools
load_PySide2_QtWebEngine = load_PyQt5_QtWebEngine
load_PySide2_QtWebEngineCore = load_PyQt5_QtWebEngineCore
load_PySide2_QtWebEngineWidgets = load_PyQt5_QtWebEngineWidgets
load_PySide2_QtWebKit = load_PyQt5_QtWebKit
load_PySide2_QtWebSockets = load_PyQt5_QtWebSockets
load_PySide2_QtWidgets = load_PyQt5_QtWidgets
load_PySide2_QtXmlPatterns = load_PyQt5_QtXmlPatterns
load_PySide2_uic = load_PyQt5_uic
# PySide2 end


def load_pyqtgraph(finder: ModuleFinder, module: Module) -> None:
    """The pyqtgraph package must be loaded as a package."""
    finder.include_package("pyqtgraph")


def load_pytest(finder: ModuleFinder, module: Module) -> None:
    """The pytest package implicitly imports others modules;
    make sure this happens."""
    pytest = __import__("pytest")
    for mod in pytest.freeze_includes():
        finder.include_module(mod)


def load_pythoncom(finder: ModuleFinder, module: Module) -> None:
    """The pythoncom module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in
    the target directory."""
    pythoncom = __import__("pythoncom")
    filename = Path(pythoncom.__file__)
    finder.include_files(
        filename, Path("lib", filename.name), copy_dependent_files=False
    )


def load_pytz(finder: ModuleFinder, module: Module) -> None:
    """The pytz module requires timezone data to be found in a known directory
    or in the zip file where the package is written."""
    target_path = Path("lib", "pytz", "zoneinfo")
    data_path = module.path[0] / "zoneinfo"
    if not data_path.is_dir():
        # Fedora (and possibly other systems) use a separate location to
        # store timezone data so look for that here as well
        pytz = __import__("pytz")
        data_path = Path(
            getattr(pytz, "_tzinfo_dir", None)
            or os.getenv("PYTZ_TZDATADIR")
            or "/usr/share/zoneinfo"
        )
        if data_path.is_dir():
            finder.add_constant("PYTZ_TZDATADIR", str(target_path))
    if data_path.is_dir():
        if module.in_file_system >= 1:
            finder.include_files(
                data_path, target_path, copy_dependent_files=False
            )
        else:
            finder.zip_include_files(data_path, Path("pytz", "zoneinfo"))


def load_pywintypes(finder: ModuleFinder, module: Module) -> None:
    """The pywintypes module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in the
    target directory."""
    pywintypes = __import__("pywintypes")
    filename = Path(pywintypes.__file__)
    finder.include_files(
        filename, Path("lib", filename.name), copy_dependent_files=False
    )


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """The reportlab module loads a submodule rl_settings via exec so force
    its inclusion here."""
    finder.include_module("reportlab.rl_settings")


def load_sentry(finder: ModuleFinder, module: Module) -> None:
    """The Sentry.io SDK"""
    finder.include_module("sentry_sdk.integrations.stdlib")
    finder.include_module("sentry_sdk.integrations.excepthook")
    finder.include_module("sentry_sdk.integrations.dedupe")
    finder.include_module("sentry_sdk.integrations.atexit")
    finder.include_module("sentry_sdk.integrations.modules")
    finder.include_module("sentry_sdk.integrations.argv")
    finder.include_module("sentry_sdk.integrations.logging")
    finder.include_module("sentry_sdk.integrations.threading")


def load_scipy(finder: ModuleFinder, module: Module) -> None:
    """The scipy module loads items within itself in a way that causes
    problems without the entire package and a number of other subpackages
    being present."""
    finder.include_package("scipy._lib")
    finder.include_package("scipy.misc")
    if WIN32:
        finder.exclude_module("scipy.spatial.cKDTree")


def load_scipy_linalg(finder: ModuleFinder, module: Module) -> None:
    """The scipy.linalg module loads items within itself in a way that causes
    problems without the entire package being present."""
    module.global_names.add("norm")
    finder.include_package("scipy.linalg")


def load_scipy_linalg_interface_gen(
    finder: ModuleFinder, module: Module
) -> None:
    """The scipy.linalg.interface_gen module optionally imports the pre module;
    ignore the error if this module cannot be found."""
    module.ignore_names.add("pre")


def load_scipy_ndimage(finder: ModuleFinder, module: Module) -> None:
    """The scipy.ndimage must be loaded as a package."""
    finder.exclude_module("scipy.ndimage.tests")
    finder.include_package("scipy.ndimage")


def load_scipy_sparse_csgraph(finder: ModuleFinder, module: Module) -> None:
    """The scipy.sparse.csgraph must be loaded as a package."""
    finder.exclude_module("scipy.sparse.csgraph.tests")
    finder.include_package("scipy.sparse.csgraph")


def load_scipy_sparse_linalg_dsolve_linsolve(
    finder: ModuleFinder, module: Module
) -> None:
    """The scipy.linalg.dsolve.linsolve optionally loads scikits.umfpack."""
    module.ignore_names.add("scikits.umfpack")


def load_scipy_spatial_transform(finder: ModuleFinder, module: Module) -> None:
    """The scipy.spatial.transform must be loaded as a package."""
    finder.include_package("scipy.spatial.transform")
    finder.exclude_module("scipy.spatial.transform.tests")


def load_scipy_special(finder: ModuleFinder, module: Module) -> None:
    """The scipy.special must be loaded as a package."""
    finder.include_package("scipy.special")


def load_scipy_special__cephes(finder: ModuleFinder, module: Module) -> None:
    """The scipy.special._cephes is an extension module and the scipy module
    imports * from it in places; advertise the global names that are used
    in order to avoid spurious errors about missing modules."""
    module.global_names.add("gammaln")


def load_scipy_stats(finder: ModuleFinder, module: Module) -> None:
    """The scipy.stats must be loaded as a package."""
    finder.include_package("scipy.stats")
    finder.exclude_module("scipy.stats.tests")


def load_skimage(finder: ModuleFinder, module: Module) -> None:
    """The skimage package."""
    finder.include_package("skimage.io")
    # exclude all tests
    finder.exclude_module("skimage.color.tests")
    finder.exclude_module("skimage.data.tests")
    finder.exclude_module("skimage.draw.tests")
    finder.exclude_module("skimage.exposure.tests")
    finder.exclude_module("skimage.feature.tests")
    finder.exclude_module("skimage.filters.tests")
    finder.exclude_module("skimage.graph.tests")
    finder.exclude_module("skimage.io.tests")
    finder.exclude_module("skimage.measure.tests")
    finder.exclude_module("skimage.metrics.tests")
    finder.exclude_module("skimage.morphology.tests")
    finder.exclude_module("skimage.restoration.tests")
    finder.exclude_module("skimage.segmentation.tests")
    finder.exclude_module("skimage._shared.tests")
    finder.exclude_module("skimage.transform.tests")
    finder.exclude_module("skimage.util.tests")
    finder.exclude_module("skimage.viewer.tests")


def load_skimage_feature_orb_cy(finder: ModuleFinder, module: Module) -> None:
    """The skimage.feature.orb_cy is a extension that load a module."""
    finder.include_module("skimage.feature._orb_descriptor_positions")


def load_setuptools(finder: ModuleFinder, module: Module) -> None:
    """The setuptools must be loaded as a package, to prevent it to break in
    the future."""
    finder.include_package("setuptools")


def load_setuptools_extension(finder: ModuleFinder, module: Module) -> None:
    """The setuptools.extension module optionally loads
    Pyrex.Distutils.build_ext but its absence is not considered an error."""
    module.ignore_names.add("Pyrex.Distutils.build_ext")


def load_site(finder: ModuleFinder, module: Module) -> None:
    """The site module optionally loads the sitecustomize and usercustomize
    modules; ignore the error if these modules do not exist."""
    module.ignore_names.update(["sitecustomize", "usercustomize"])


def load_sqlite3(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the sqlite3 module requires an additional dll sqlite3.dll to
    be present in the build directory."""
    if WIN32 and not MINGW:
        dll_name = "sqlite3.dll"
        dll_path = Path(sys.base_prefix, "DLLs", dll_name)
        if not dll_path.exists():
            dll_path = Path(sys.base_prefix, "Library", "bin", dll_name)
        finder.include_files(dll_path, Path("lib", dll_name))
    finder.include_package("sqlite3")


def load_six(finder: ModuleFinder, module: Module) -> None:
    """The six module creates fake modules."""
    finder.exclude_module("six.moves")


def load_ssl(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the SSL module in Python 3.7+ requires additional dlls to
    be present in the build directory."""
    if WIN32 and sys.version_info >= (3, 7) and not MINGW:
        for dll_search in ["libcrypto-*.dll", "libssl-*.dll"]:
            libs_dir = Path(sys.base_prefix, "DLLs")
            for dll_path in libs_dir.glob(dll_search):
                finder.include_files(dll_path, Path("lib", dll_path.name))


def load_sysconfig(finder: ModuleFinder, module: Module) -> None:
    """The sysconfig module implicitly loads _sysconfigdata."""
    get_data_name = getattr(sysconfig, "_get_sysconfigdata_name", None)
    if get_data_name is None:
        datafile = "_sysconfigdata"
    else:
        if not hasattr(sys, "abiflags"):
            sys.abiflags = ""
        datafile = get_data_name()
    finder.include_module(datafile)


def load_tensorflow(finder: ModuleFinder, module: Module) -> None:
    """The tensorflow package implicitly loads some packages."""
    finder.include_package("tensorboard")
    finder.include_package("tensorflow.compiler")
    finder.include_package("tensorflow.python")


def load_time(finder: ModuleFinder, module: Module) -> None:
    """The time module implicitly loads _strptime; make sure this happens."""
    finder.include_module("_strptime")


def load_tkinter(finder: ModuleFinder, module: Module) -> None:
    """The tkinter module has data files that are required to be loaded so
    ensure that they are copied into the directory that is expected at
    runtime."""
    if WIN32:
        tkinter = __import__("tkinter")
        root_names = "tcl", "tk"
        environ_names = "TCL_LIBRARY", "TK_LIBRARY"
        version_vars = tkinter.TclVersion, tkinter.TkVersion
        zipped = zip(environ_names, version_vars, root_names)
        for env_name, ver_var, mod_name in zipped:
            dir_name = mod_name + str(ver_var)
            try:
                lib_texts = os.environ[env_name]
            except KeyError:
                if MINGW:
                    lib_texts = Path(sys.base_prefix, "lib", dir_name)
                else:
                    lib_texts = Path(sys.base_prefix, "tcl", dir_name)
            target_path = Path("lib", "tkinter", dir_name)
            finder.add_constant(env_name, str(target_path))
            finder.include_files(lib_texts, target_path)
            if not MINGW:
                dll_name = dir_name.replace(".", "") + "t.dll"
                dll_path = Path(sys.base_prefix, "DLLs", dll_name)
                finder.include_files(dll_path, Path("lib", dll_name))


def load_twisted_conch_ssh_transport(
    finder: ModuleFinder, module: Module
) -> None:
    """The twisted.conch.ssh.transport module uses __import__ builtin to
    dynamically load different ciphers at runtime."""
    finder.include_package("Crypto.Cipher")


def load_twitter(finder: ModuleFinder, module: Module) -> None:
    """The twitter module tries to load the simplejson, json and django.utils
    module in an attempt to locate any module that will implement the
    necessary protocol; ignore these modules if they cannot be found."""
    module.ignore_names.update(["json", "simplejson", "django.utils"])


def load_uvloop(finder: ModuleFinder, module: Module) -> None:
    """The uvloop module implicitly loads an extension module."""
    finder.include_module("uvloop._noop")


def load_win32api(finder: ModuleFinder, module: Module) -> None:
    """The win32api module implicitly loads the pywintypes module; make sure
    this happens."""
    finder.exclude_dependent_files(module.file)
    finder.include_module("pywintypes")


def load_win32com(finder: ModuleFinder, module: Module) -> None:
    """The win32com package manipulates its search path at runtime to include
    the sibling directory called win32comext; simulate that by changing the
    search path in a similar fashion here."""
    module.path.append(module.file.parent.parent / "win32comext")


def load_win32file(finder: ModuleFinder, module: Module) -> None:
    """The win32file module implicitly loads the pywintypes and win32timezone
    module; make sure this happens."""
    finder.include_module("pywintypes")
    finder.include_module("win32timezone")


def load_wx_lib_pubsub_core(finder: ModuleFinder, module: Module) -> None:
    """The wx.lib.pubsub.core module modifies the search path which cannot
    be done in a frozen application in the same way; modify the module
    search path here instead so that the right modules are found; note
    that this only works if the import of wx.lib.pubsub.setupkwargs
    occurs first."""
    module.path.insert(0, module.file.parent / "kwargs")


def load_Xlib_display(finder: ModuleFinder, module: Module) -> None:
    """The Xlib.display module implicitly loads a number of extension modules;
    make sure this happens."""
    finder.include_module("Xlib.ext.xtest")
    finder.include_module("Xlib.ext.shape")
    finder.include_module("Xlib.ext.xinerama")
    finder.include_module("Xlib.ext.record")
    finder.include_module("Xlib.ext.composite")
    finder.include_module("Xlib.ext.randr")


def load_Xlib_support_connect(finder: ModuleFinder, module: Module) -> None:
    """The Xlib.support.connect module implicitly loads a platform specific
    module; make sure this happens."""
    if sys.platform.split("-", maxsplit=1)[0] == "OpenVMS":
        module_name = "vms_connect"
    else:
        module_name = "unix_connect"
    finder.include_module(f"Xlib.support.{module_name}")


def load_Xlib_XK(finder: ModuleFinder, module: Module) -> None:
    """The Xlib.XK module implicitly loads some keysymdef modules; make sure
    this happens."""
    finder.include_module("Xlib.keysymdef.miscellany")
    finder.include_module("Xlib.keysymdef.latin1")


def load_xml_etree_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """The xml.etree.cElementTree module implicitly loads the
    xml.etree.ElementTree module; make sure this happens."""
    finder.include_module("xml.etree.ElementTree")


def load_zmq(finder: ModuleFinder, module: Module) -> None:
    """The zmq package loads zmq.backend.cython dynamically and links
    dynamically to zmq.libzmq or shared lib. Tested in pyzmq 16.0.4 (py36),
    19.0.2 (MSYS2 py39) up to 22.2.1 (from pip and from conda)."""
    finder.include_package("zmq.backend.cython")
    if WIN32:
        # For pyzmq 22 the libzmq dependencies are located in
        # site-packages/pyzmq.libs
        libzmq_folder = "pyzmq.libs"
        libs_dir = module.path[0].parent / libzmq_folder
        if libs_dir.exists():
            finder.include_files(libs_dir, Path("lib", libzmq_folder))
    # Include the bundled libzmq library, if it exists
    try:
        finder.include_module("zmq.libzmq")
    except ImportError:
        pass  # assume libzmq is not bundled
    finder.exclude_module("zmq.tests")


def load_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """The zoneinfo package requires timezone data, that
    can be the in tzdata package, if installed."""
    tzdata: Optional[Module] = None
    source: Optional[Path] = None
    try:
        tzdata = finder.include_package("tzdata")
        # store tzdata along with zoneinfo
        tzdata.in_file_system = module.in_file_system
    except ImportError:
        zoneinfo = __import__(module.name, fromlist=["TZPATH"])
        if zoneinfo.TZPATH:
            for path in zoneinfo.TZPATH:
                if path.endswith("zoneinfo"):
                    source = Path(path)
                    break
        if source:
            # without tzdata, copy only zoneinfo directory
            # in Linux: /usr/share/zoneinfo
            target = Path("lib", "tzdata", "zoneinfo")
            finder.include_files(source, target, copy_dependent_files=False)
            finder.add_constant("PYTHONTZPATH", str(source))
    if tzdata is None:
        return
    # when the tzdata exists, copy other files in this directory
    source = tzdata.path[0]
    target = Path("lib", "tzdata")
    if tzdata.in_file_system >= 1:
        finder.include_files(source, target, copy_dependent_files=False)
    else:
        finder.zip_include_files(source, "tzdata")


load_backports_zoneinfo = load_zoneinfo


def load_zope_component(finder: ModuleFinder, module: Module) -> None:
    """The zope.component package requires the presence of the pkg_resources
    module but it uses a dynamic, not static import to do its work."""
    finder.include_module("pkg_resources")


def missing_gdk(finder: ModuleFinder, caller: Module) -> None:
    """The gdk module is buried inside gtk so there is no need to concern
    ourselves with an error saying that it cannot be found."""
    caller.ignore_names.add("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """This module is not necessairly present so ignore it when it cannot be
    found."""
    caller.ignore_names.add("ltihooks")


def missing_readline(finder: ModuleFinder, caller: Module) -> None:
    """The readline module is not normally present on Windows but it also may
    be so instead of excluding it completely, ignore it if it can't be found.
    """
    if WIN32:
        caller.ignore_names.add("readline")
