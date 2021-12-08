import collections.abc
from importlib.machinery import EXTENSION_SUFFIXES
import os
from pathlib import Path
import sys
import sysconfig
from typing import List, Optional, Tuple

from .common import code_object_replace
from .finder import ModuleFinder
from .module import Module

MINGW = sysconfig.get_platform().startswith("mingw")
WIN32 = sys.platform == "win32"


def initialize(finder: ModuleFinder) -> None:
    """
    Upon initialization of the finder, this routine is called to set up some
    automatic exclusions for various platforms.
    """
    # py2 modules that have been removed or renamed in py3
    for name in collections.abc.__all__:
        finder.ExcludeModule("collections." + name)
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
        finder.ExcludeModule("email." + name)
    finder.ExcludeModule("__builtin__")
    finder.ExcludeModule("__main__")
    finder.ExcludeModule("_winreg")
    finder.ExcludeModule("audiodev")
    finder.ExcludeModule("anydbm")
    finder.ExcludeModule("BaseHTTPServer")
    finder.ExcludeModule("Bastion")
    finder.ExcludeModule("bsddb")
    finder.ExcludeModule("cPickle")
    finder.ExcludeModule("commands")
    finder.ExcludeModule("ConfigParser")
    finder.ExcludeModule("Cookie")
    finder.ExcludeModule("copy_reg")
    finder.ExcludeModule("cStringIO")
    finder.ExcludeModule("dbhash")
    finder.ExcludeModule("dircache")
    finder.ExcludeModule("dl")
    finder.ExcludeModule("dumbdbm")
    finder.ExcludeModule("dummy_thread")
    finder.ExcludeModule("FCNTL")
    finder.ExcludeModule("fl")
    finder.ExcludeModule("fm")
    finder.ExcludeModule("fpformat")
    finder.ExcludeModule("gl")
    finder.ExcludeModule("gdbm")
    finder.ExcludeModule("htmllib")
    finder.ExcludeModule("HTMLParser")
    finder.ExcludeModule("httplib")
    finder.ExcludeModule("hotshot")
    finder.ExcludeModule("ihooks")
    finder.ExcludeModule("imputil")
    finder.ExcludeModule("linuxaudiodev")
    finder.ExcludeModule("md5")
    finder.ExcludeModule("Nav")
    finder.ExcludeModule("new")
    finder.ExcludeModule("mutex")
    finder.ExcludeModule("Pickle")
    finder.ExcludeModule("Queue")
    finder.ExcludeModule("rexec")
    finder.ExcludeModule("robotparser")
    finder.ExcludeModule("sgmllib")
    finder.ExcludeModule("sha")
    finder.ExcludeModule("SocketServer")
    finder.ExcludeModule("statvfs")
    finder.ExcludeModule("StringIO")
    finder.ExcludeModule("sunaudiodev")
    finder.ExcludeModule("thread")
    finder.ExcludeModule("Tkinter")
    finder.ExcludeModule("toaiff")
    finder.ExcludeModule("urllib.quote")
    finder.ExcludeModule("urllib.quote_plus")
    finder.ExcludeModule("urllib.unquote")
    finder.ExcludeModule("urllib.unquote_plus")
    finder.ExcludeModule("urllib.urlencode")
    finder.ExcludeModule("urllib.urlopen")
    finder.ExcludeModule("urllib.urlretrieve")
    finder.ExcludeModule("urllib2")
    finder.ExcludeModule("urlparse")
    finder.ExcludeModule("user")
    finder.ExcludeModule("UserDict")
    finder.ExcludeModule("UserList")
    finder.ExcludeModule("UserString")
    finder.ExcludeModule("whichdb")
    # macos specfic removed in py3
    # https://docs.python.org/2.7/library/mac.html?highlight=removed
    finder.ExcludeModule("autoGIL")
    finder.ExcludeModule("Carbon")
    finder.ExcludeModule("ColorPicker")
    finder.ExcludeModule("EasyDialogs")
    finder.ExcludeModule("findertools")
    finder.ExcludeModule("FrameWork")
    finder.ExcludeModule("ic")
    finder.ExcludeModule("MacOS")
    finder.ExcludeModule("macostools")
    # macpython removed
    finder.ExcludeModule("aetools")
    finder.ExcludeModule("aepack")
    finder.ExcludeModule("aetypes")
    finder.ExcludeModule("applesingle")
    finder.ExcludeModule("buildtools")
    finder.ExcludeModule("cfmfile")
    finder.ExcludeModule("icopen")
    finder.ExcludeModule("macerros")
    finder.ExcludeModule("macresource")
    finder.ExcludeModule("PixMapWrapper")
    finder.ExcludeModule("videoreader")
    finder.ExcludeModule("W")
    # sgi removed
    finder.ExcludeModule("al")
    finder.ExcludeModule("imgfile")
    finder.ExcludeModule("jpeg")
    finder.ExcludeModule("cd")
    finder.ExcludeModule("sv")
    # internal modules
    finder.ExcludeModule("_frozen_importlib")
    finder.ExcludeModule("_frozen_importlib_external")
    finder.ExcludeModule("os.path")
    # confused names in Windows
    finder.ExcludeModule("multiprocessing.Pool")
    finder.ExcludeModule("multiprocessing.Process")
    # exclusion by platform/os
    if os.name == "nt":
        finder.ExcludeModule("fcntl")
        finder.ExcludeModule("grp")
        finder.ExcludeModule("pwd")
        finder.ExcludeModule("termios")
    else:
        finder.ExcludeModule("_overlapped")
        finder.ExcludeModule("_subprocess")
        finder.ExcludeModule("_winapi")
        finder.ExcludeModule("msilib")
        finder.ExcludeModule("msvcrt")
        finder.ExcludeModule("multiprocessing._multiprocessing")
        finder.ExcludeModule("nt")
        finder.ExcludeModule("nturl2path")
        finder.ExcludeModule("pyHook")
        finder.ExcludeModule("pythoncom")
        finder.ExcludeModule("pywintypes")
        finder.ExcludeModule("winerror")
        finder.ExcludeModule("winsound")
        finder.ExcludeModule("win32api")
        finder.ExcludeModule("win32con")
        finder.ExcludeModule("win32com.shell")
        finder.ExcludeModule("win32gui")
        finder.ExcludeModule("win32event")
        finder.ExcludeModule("win32evtlog")
        finder.ExcludeModule("win32evtlogutil")
        finder.ExcludeModule("win32file")
        finder.ExcludeModule("win32pdh")
        finder.ExcludeModule("win32pipe")
        finder.ExcludeModule("win32process")
        finder.ExcludeModule("win32security")
        finder.ExcludeModule("win32service")
        finder.ExcludeModule("win32stat")
        finder.ExcludeModule("win32wnet")
        finder.ExcludeModule("winreg")
        finder.ExcludeModule("wx.activex")
    if os.name != "posix":
        finder.ExcludeModule("posix")
    if sys.platform != "darwin":
        finder.ExcludeModule("ctypes.macholib.dyld")
        finder.ExcludeModule("mac")
        finder.ExcludeModule("macpath")
        finder.ExcludeModule("macurl2path")
        finder.ExcludeModule("_scproxy")
    if os.name != "os2":
        finder.ExcludeModule("os2")
        finder.ExcludeModule("os2emxpath")
        finder.ExcludeModule("_emx_link")
    if os.name != "ce":
        finder.ExcludeModule("ce")
    if os.name != "riscos":
        finder.ExcludeModule("riscos")
        finder.ExcludeModule("riscosenviron")
        finder.ExcludeModule("riscospath")
        finder.ExcludeModule("rourl2path")
    if not sys.platform.startswith("java"):
        finder.ExcludeModule("com.sun")
        finder.ExcludeModule("java")
        finder.ExcludeModule("org.python")
    if not sys.platform.startswith("OpenVMS"):
        finder.ExcludeModule("vms_lib")
    if "__pypy__" not in sys.builtin_module_names:
        finder.ExcludeModule("__pypy__")


def load_aiofiles(finder: ModuleFinder, module: Module) -> None:
    """The aiofiles must be loaded as a package."""
    finder.IncludePackage("aiofiles")


def load_asyncio(finder: ModuleFinder, module: Module) -> None:
    """The asyncio must be loaded as a package."""
    finder.IncludePackage("asyncio")


def load_babel(finder: ModuleFinder, module: Module) -> None:
    """The babel must be loaded as a package, and has pickeable data."""
    finder.IncludePackage("babel")
    module.in_file_system = 1


def load_bcrypt(finder: ModuleFinder, module: Module) -> None:
    """The bcrypt package requires the _cffi_backend module (loaded implicitly)"""
    finder.IncludeModule("_cffi_backend")


def load_boto(finder: ModuleFinder, module: Module) -> None:
    """the boto package uses 'six' fake modules."""
    finder.ExcludeModule("boto.vendored.six.moves")


def load_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """
    The cElementTree module implicitly loads the elementtree.ElementTree
    module; make sure this happens.
    """
    finder.IncludeModule("elementtree.ElementTree")


def load_ceODBC(finder: ModuleFinder, module: Module) -> None:
    """
    The ceODBC module implicitly imports both datetime and decimal;
    make sure this happens.
    """
    finder.IncludeModule("datetime")
    finder.IncludeModule("decimal")


def load_certifi(finder: ModuleFinder, module: Module) -> None:
    """
    The certifi package, in python 3.7 and up, uses importlib.resources
    to locate the cacert.pem in zip packages.
    In previous versions, it is expected to be stored in the file system.
    """
    if module.in_file_system == 0:
        if sys.version_info < (3, 7):
            module.in_file_system = 1
            return
        cacert = Path(__import__("certifi").where())
        finder.ZipIncludeFiles(cacert, Path("certifi", cacert.name))


def load__cffi_backend(finder: ModuleFinder, module: Module) -> None:
    """Add the cffi metadata for _cffi_backend module."""
    module.update_distribution("cffi")


def load_cffi_cparser(finder: ModuleFinder, module: Module) -> None:
    """The cffi.cparser module can use a extension if present."""
    try:
        cffi = __import__("cffi", fromlist=["_pycparser"])
        pycparser = getattr(cffi, "_pycparser")
        finder.IncludeModule(pycparser.__name__)
    except (ImportError, AttributeError):
        finder.ExcludeModule("cffi._pycparser")


def load_crc32c(finder: ModuleFinder, module: Module) -> None:
    """The google.crc32c module requires _cffi_backend module."""
    finder.IncludeModule("_cffi_backend")


def load_clr(finder: ModuleFinder, module: Module) -> None:
    """
    The pythonnet package (imported as 'clr') needs Python.Runtime.dll
    in runtime.
    """
    dll_name = "Python.Runtime.dll"
    finder.IncludeFiles(module.file.parent / dll_name, Path("lib", dll_name))


def load_cryptography_hazmat_bindings__openssl(
    finder: ModuleFinder, module: Module
) -> None:
    """The cryptography module requires the _cffi_backend module."""
    finder.IncludeModule("_cffi_backend")


def load_cryptography_hazmat_bindings__padding(
    finder: ModuleFinder, module: Module
) -> None:
    """The cryptography module requires the _cffi_backend module."""
    finder.IncludeModule("_cffi_backend")


def load_Crypto_Cipher(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Cipher subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_Hash(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Hash subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_Math(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Math subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_Protocol(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Protocol subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_PublicKey(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.PublicKey subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_Util(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Util subpackage of pycryptodome package."""
    if module.in_file_system == 0:
        finder.IncludePackage(module.name)


def load_Crypto_Util__file_system(
    finder: ModuleFinder, module: Module
) -> None:
    """The pycryptodome package"""
    # WARNING: do not touch this code string
    PYCRYPTODOME_CODE_STR = """
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
        new_code = compile(PYCRYPTODOME_CODE_STR, str(module.file), "exec")
        co_func = new_code.co_consts[2]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, c in enumerate(consts):
            if isinstance(c, type(code)) and c.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the _ctypes module in Python 3.8+ requires an additional
    libffi dll to be present in the build directory.
    """
    if WIN32 and sys.version_info >= (3, 8) and not MINGW:
        dll_pattern = "libffi-*.dll"
        dll_dir = Path(sys.base_prefix, "DLLs")
        for dll_path in dll_dir.glob(dll_pattern):
            finder.IncludeFiles(dll_path, Path("lib", dll_path.name))


def load_cv2(finder: ModuleFinder, module: Module) -> None:
    """
    Versions of cv2 (opencv-python) above 4.5.3 require additional
    configuration files.

    Additionally, on Linux the opencv_python.libs directory is not
    copied across for versions above 4.5.3 unless the cv2 package is
    included.
    """
    finder.IncludePackage("cv2")

    dest_dir = Path("lib", "cv2")
    cv2_dir = module.path[0]
    for path in cv2_dir.glob("config*.py"):
        finder.IncludeFiles(path, dest_dir / path.name)


def load_cx_Oracle(finder: ModuleFinder, module: Module) -> None:
    """
    The cx_Oracle module implicitly imports datetime; make sure this
    happens.
    """
    finder.IncludeModule("datetime")
    finder.IncludeModule("decimal")


def load_datetime(finder: ModuleFinder, module: Module) -> None:
    """The datetime module implicitly imports time; make sure this happens."""
    finder.IncludeModule("time")


def load_docutils_frontend(finder: ModuleFinder, module: Module) -> None:
    """
    The optik module is the old name for the optparse module; ignore the
    module if it cannot be found.
    """
    module.ignore_names.add("optik")


def load_dummy_threading(finder: ModuleFinder, module: Module) -> None:
    """
    The dummy_threading module plays games with the name of the threading
    module for its own purposes; ignore that here.
    """
    finder.ExcludeModule("_dummy_threading")


def load_flask_compress(finder: ModuleFinder, module: Module) -> None:
    """flask-compress requires its metadata."""
    module.update_distribution("Flask_Compress")


def load_ftplib(finder: ModuleFinder, module: Module) -> None:
    """
    The ftplib module attempts to import the SOCKS module; ignore this
    module if it cannot be found.
    """
    module.ignore_names.add("SOCKS")


def load_gevent(finder: ModuleFinder, module: Module) -> None:
    """The gevent must be loaded as a package."""
    finder.IncludePackage("gevent")


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
    discovery_cache = finder.IncludePackage("googleapiclient.discovery_cache")
    discovery_cache.in_file_system = 1


def load_google_cloud_storage(finder: ModuleFinder, module: Module) -> None:
    """The google.cloud.storage package always uses the parent module."""
    finder.IncludePackage("google.cloud")


def load_gtk__gtk(finder: ModuleFinder, module: Module) -> None:
    """The gtk._gtk module has a number of implicit imports."""
    finder.IncludeModule("atk")
    finder.IncludeModule("cairo")
    finder.IncludeModule("gio")
    finder.IncludeModule("pango")
    finder.IncludeModule("pangocairo")


def load_h5py(finder: ModuleFinder, module: Module) -> None:
    """h5py module has a number of implicit imports"""
    finder.IncludeModule("h5py.defs")
    finder.IncludeModule("h5py.utils")
    finder.IncludeModule("h5py._proxy")
    try:
        api_gen = __import__("h5py", fromlist=["api_gen"]).api_gen
        finder.IncludeModule(api_gen.__name__)
    except (ImportError, AttributeError):
        pass
    finder.IncludeModule("h5py._errors")
    finder.IncludeModule("h5py.h5ac")


def load_h5py_wrapper(finder: ModuleFinder, module: Module) -> None:
    """h5py_wrapper module requires future and pytest-runner"""
    finder.IncludeModule("future")
    finder.IncludeModule("ptr")


def load_hashlib(finder: ModuleFinder, module: Module) -> None:
    """hashlib's fallback modules don't exist if the equivalent OpenSSL
    algorithms are loaded from _hashlib, so we can ignore the error."""
    module.ignore_names.update(["_md5", "_sha", "_sha256", "_sha512"])


def load_hdfdict(finder: ModuleFinder, module: Module) -> None:
    """hdfdict module requires h5py_wrapper and PyYAML"""
    finder.IncludeModule("h5py_wrapper")
    finder.IncludePackage("yaml")


def load_idna(finder: ModuleFinder, module: Module) -> None:
    """The idna module implicitly loads data; make sure this happens."""
    finder.IncludeModule("idna.idnadata")


def load_lxml(finder: ModuleFinder, module: Module) -> None:
    """The lxml package uses an extension."""
    finder.IncludeModule("lxml._elementpath")


def load_llvmlite(finder: ModuleFinder, module: Module) -> None:
    """The llvmlite must be loaded as package."""
    finder.IncludePackage("llvmlite")
    finder.ExcludeModule("llvmlite.tests")


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
    finder.IncludeFiles(data_path, target_path, copy_dependent_files=False)
    finder.IncludePackage("matplotlib")
    finder.ExcludeModule("matplotlib.tests")
    finder.ExcludeModule("matplotlib.testing")
    if not need_patch or module.code is None:
        return
    CODE_STR = f"""
def _get_data_path():
    return os.path.join(os.path.dirname(sys.executable), "{target_path!s}")
"""
    for code_str in [CODE_STR, CODE_STR.replace("_get_data_", "get_data_")]:
        new_code = compile(code_str, str(module.file), "exec")
        co_func = new_code.co_consts[0]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i, c in enumerate(consts):
            if isinstance(c, type(code)) and c.co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy must be loaded as a package; support for pypi version and
    numpy+mkl version - tested with 1.19.5+mkl, 1.20.3+mkl, 1.21.0+mkl,
    1.21.1+mkl, 1.21.2+mkl and 1.21.2 from conda-forge."""
    finder.IncludePackage("numpy")

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
                finder.IncludeFiles(path, dest_dir / path.name)
            for path in libs_dir.glob("lib*.dll"):
                finder.IncludeFiles(path, dest_dir / path.name)
            finder.AddConstant("MKL_PATH", str(dest_dir))
            finder.ExcludeModule("numpy.DLLs")

            # do not check dependencies already handled
            extension = EXTENSION_SUFFIXES[0]
            for path in numpy_dir.rglob(f"*{extension}"):
                finder.ExcludeDependentFiles(path)

        # support for old versions (numpy <= 1.18.2)
        if module.in_file_system == 0:
            # copy any file at site-packages/numpy/.libs
            libs_dir = numpy_dir / ".libs"
            if libs_dir.is_dir():
                finder.IncludeFiles(libs_dir, "lib")

    # exclude the tests
    finder.ExcludeModule("numpy.compat.tests")
    finder.ExcludeModule("numpy.core.tests")
    finder.ExcludeModule("numpy.distutils.tests")
    finder.ExcludeModule("numpy.f2py.tests")
    finder.ExcludeModule("numpy.fft.tests")
    finder.ExcludeModule("numpy.lib.tests")
    finder.ExcludeModule("numpy.linalg.tests")
    finder.ExcludeModule("numpy.ma.tests")
    finder.ExcludeModule("numpy.matrixlib.tests")
    finder.ExcludeModule("numpy.polynomial.tests")
    finder.ExcludeModule("numpy.random._examples")
    finder.ExcludeModule("numpy.random.tests")
    finder.ExcludeModule("numpy.tests")
    finder.ExcludeModule("numpy.typing.tests")


def load_numpy_core_numerictypes(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.core.numerictypes module adds a number of items to itself
    dynamically; define these to avoid spurious errors about missing
    modules.
    """
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
    """
    The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_misc_util(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("numscons")


def load_numpy_distutils_system_info(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("Numeric")


def load_numpy_f2py___version__(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found.
    """
    module.ignore_names.add("__svn_version__")


def load_numpy_linalg(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.linalg module implicitly loads the lapack_lite module; make
    sure this happens.
    """
    finder.IncludeModule("numpy.linalg.lapack_lite")


def load_numpy_random_mtrand(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.random.mtrand module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules.
    """
    module.global_names.update(["rand", "randn"])


def load_Numeric(finder: ModuleFinder, module: Module) -> None:
    """
    The Numeric module optionally loads the dotblas module; ignore the error
    if this modules does not exist.
    """
    module.ignore_names.add("dotblas")


def load_pandas(finder: ModuleFinder, module: Module) -> None:
    """The pandas has dynamic imports."""
    finder.IncludePackage("pandas._libs")
    finder.ExcludeModule("pandas.tests")


def load_pikepdf(finder: ModuleFinder, module: Module) -> None:
    """The pikepdf must be loaded as a package."""
    finder.IncludePackage("pikepdf")


def load_PIL(finder: ModuleFinder, module: Module) -> None:
    """The Pillow must be loaded as a package."""
    finder.IncludePackage("PIL")


def load_plotly(finder: ModuleFinder, module: Module) -> None:
    """The plotly must be loaded as a package."""
    finder.IncludePackage("plotly")


def load_pkg_resources(finder: ModuleFinder, module: Module) -> None:
    """
    The pkg_resources must be loaded as a package;
    dynamically loaded modules in subpackages is growing.
    """
    finder.IncludePackage("pkg_resources")


def load_postgresql_lib(finder: ModuleFinder, module: Module) -> None:
    """
    The postgresql.lib module requires the libsys.sql file to be included
    so make sure that file is included.
    """
    filename = "libsys.sql"
    finder.IncludeFiles(module.path[0] / filename, filename)


def load_pty(finder: ModuleFinder, module: Module) -> None:
    """The sgi module is not needed for this module to function."""
    module.ignore_names.add("sgi")


def load_ptr(finder: ModuleFinder, module: Module) -> None:
    """pytest-runner requires its metadata"""
    module.update_distribution("pytest-runner")


def load_pycountry(finder: ModuleFinder, module: Module) -> None:
    """The pycountry module has data in subdirectories."""
    finder.ExcludeModule("pycountry.tests")
    module.in_file_system = 1


def load_pycparser(finder: ModuleFinder, module: Module) -> None:
    """
    These files are missing which causes
    permission denied issues on windows when they are regenerated.
    """
    finder.IncludeModule("pycparser.lextab")
    finder.IncludeModule("pycparser.yacctab")


def load_pydantic(finder: ModuleFinder, module: Module) -> None:
    """
    The pydantic package is compiled by Cython (and the imports are hidden).
    """
    finder.IncludeModule("colorsys")
    finder.IncludeModule("dataclasses")  # support in v 1.7+
    finder.IncludeModule("datetime")
    finder.IncludeModule("decimal")
    finder.IncludeModule("functools")
    finder.IncludeModule("ipaddress")
    finder.IncludePackage("json")
    finder.IncludeModule("pathlib")
    finder.IncludeModule("typing_extensions")  # support in v 1.8
    finder.IncludeModule("uuid")


def load_pygments(finder: ModuleFinder, module: Module) -> None:
    """The pygments package dynamically load styles."""
    finder.IncludePackage("pygments.styles")
    finder.IncludePackage("pygments.lexers")
    finder.IncludePackage("pygments.formatters")


def load_pyodbc(finder: ModuleFinder, module: Module) -> None:
    """
    The pyodbc module implicitly imports others modules;
    make sure this happens.
    """
    for mod in ("datetime", "decimal", "hashlib", "locale", "uuid"):
        finder.IncludeModule(mod)


# cache the QtCore library paths
_qtcore_library_paths = []


def _qt_implementation(module: Module) -> str:
    """Helper function to get the name of the Qt implementation (PyQt5)."""
    return module.name.split(".")[0]


def _qt_library_paths(name: str) -> List[str]:
    global _qtcore_library_paths
    if _qtcore_library_paths:
        return _qtcore_library_paths
    try:
        qtcore = __import__(name, fromlist=["QtCore"]).QtCore
    except RuntimeError:
        print("WARNING: Tried to load multiple incompatible Qt ", end="")
        print("wrappers. Some incorrect files may be copied.")
        qtcore = None
    else:
        _qtcore_library_paths = [
            Path(p) for p in qtcore.QCoreApplication.libraryPaths()
        ]
    if not _qtcore_library_paths:
        # check the common location for conda
        plugins_path = Path(sys.base_prefix, "Library", "plugins")
        if plugins_path.exists():
            _qtcore_library_paths.append(plugins_path)
        elif qtcore:
            # use a hack
            app = qtcore.QCoreApplication([])
            _qtcore_library_paths = [Path(p) for p in app.libraryPaths()]
    if not _qtcore_library_paths and qtcore:
        # Qt Plugins can be in a plugins directory next to the Qt libraries
        pyqt5_root_dir = Path(qtcore.__file__).parent
        _qtcore_library_paths.append(pyqt5_root_dir / "plugins")
        _qtcore_library_paths.append(pyqt5_root_dir / "Qt5" / "plugins")
        _qtcore_library_paths.append(pyqt5_root_dir / "Qt" / "plugins")
    return _qtcore_library_paths


def get_qt_plugins_paths(name: str, plugins: str) -> List[Tuple[str, str]]:
    """Helper function to get a list of source and target paths of Qt plugins,
    indicated to be used in include_files."""
    include_files = []
    for library_dir in _qt_library_paths(name):
        if library_dir.parts[-1] != "plugins":
            continue
        source_path = library_dir / plugins
        if not source_path.exists():
            continue
        if source_path.parts[-3] == name:  # {name}/plugins/{plugins}
            target_path = Path("lib").joinpath(*source_path.parts[-3:])
        elif source_path.parts[-4] == name:  # {name}/Qt*/plugins/{plugins}
            target_path = Path("lib").joinpath(*source_path.parts[-4:])
        else:
            # fallback plugins path to be used by load_PyQt5.
            target_path = Path("lib") / name / "Qt" / "plugins" / plugins
        include_files.append((source_path, target_path))
    return include_files


def copy_qt_plugins(name: str, plugins: str, finder: ModuleFinder) -> None:
    """Helper function to find and copy Qt plugins."""
    for source_path, target_path in get_qt_plugins_paths(name, plugins):
        finder.IncludeFiles(source_path, target_path)


def load_PyQt5(finder: ModuleFinder, module: Module) -> None:
    """Inject code in PyQt5/PySide2 init to locate and load plugins."""
    if module.code is None:
        return
    # With PyQt5 5.15.4, if the folder name contains non-ascii characters, the
    # libraryPaths returns empty. Prior to this version, this doesn't happen.
    # However, this hack will be used to workaround issues with anaconda and/or
    # with the use of zip_include_packages too.
    # With PySide2, the opposite happens. In PySide2 5.15.2, folders with non-
    # ascii work, but in previous versions (5.15.1, 5.13.x, 5.12.0) they don't.
    name = _qt_implementation(module)
    code_string = module.file.read_text()
    code_string += f"""
# cx_Freeze patch start
import os, sys
from .QtCore import QCoreApplication

executable_dir = os.path.dirname(sys.executable)
pyqt5_root_dir = os.path.join(executable_dir, "lib", "{name}")
plugins_dir = os.path.join(pyqt5_root_dir, "Qt5", "plugins")  # PyQt5 5.15.4
if not os.path.isdir(plugins_dir):
    plugins_dir = os.path.join(pyqt5_root_dir, "Qt", "plugins")  # others
library_paths = [os.path.normcase(p) for p in QCoreApplication.libraryPaths()]
if os.path.normcase(plugins_dir) not in library_paths:
    library_paths = QCoreApplication.libraryPaths() + [plugins_dir]
    QCoreApplication.setLibraryPaths(library_paths)
# cx_Freeze patch end
"""
    module.code = compile(code_string, str(module.file), "exec")
    if module.in_file_system == 0:
        module.in_file_system = 2  # use optimized mode


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
    finder.IncludeModule(f"{name}.QtCore")
    finder.IncludeModule(f"{name}.QtGui")
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
            finder.IncludeModule(f"{name}.{mod}")
        except ImportError:
            pass


def load_PyQt5_QtCore(finder: ModuleFinder, module: Module) -> None:
    """The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module."""
    name = _qt_implementation(module)
    try:
        finder.IncludeModule(f"{name}.sip")  # PyQt5 >= 5.11
    except ImportError:
        finder.IncludeModule("sip")
    try:
        finder.IncludeModule(f"{name}._qt")
    except ImportError:
        pass


def load_PyQt5_QtGui(finder: ModuleFinder, module: Module) -> None:
    """There is a chance that GUI will use some image formats
    add the image format plugins."""
    name = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtCore")
    copy_qt_plugins(name, "imageformats", finder)
    # On Qt5, we need the platform plugins. For simplicity, we just copy
    # any that are installed.
    copy_qt_plugins(name, "platforms", finder)


def load_PyQt5_QtMultimedia(finder: ModuleFinder, module: Module) -> None:
    name = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtCore")
    finder.IncludeModule(f"{name}.QtMultimediaWidgets")
    copy_qt_plugins(name, "mediaservice", finder)


def load_PyQt5_QtPrintSupport(finder: ModuleFinder, module: Module) -> None:
    name = _qt_implementation(module)
    copy_qt_plugins(name, "printsupport", finder)


def load_PyQt5_QtWebKit(finder: ModuleFinder, module: Module) -> None:
    name = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtNetwork")
    finder.IncludeModule(f"{name}.QtGui")


def load_PyQt5_QtWidgets(finder: ModuleFinder, module: Module) -> None:
    name = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtGui")


def load_PyQt5_uic(finder: ModuleFinder, module: Module) -> None:
    """The uic module makes use of "plugins" that need to be read directly and
    cannot be frozen; the PyQt5.QtWebKit and PyQt5.QtNetwork modules are
    also implicity loaded."""
    name = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtNetwork")
    try:
        finder.IncludeModule(f"{name}.QtWebKit")
    except ImportError:
        pass
    source_dir = module.path[0] / "widget-plugins"
    finder.IncludeFiles(source_dir, f"{name}.uic.widget-plugins")


# PySide2 start
load_PySide2 = load_PyQt5
load_PySide2_Qt = load_PyQt5_Qt
# load_PySide2_QtCore is not necessary
load_PySide2_QtGui = load_PyQt5_QtGui
load_PySide2_QtMultimedia = load_PyQt5_QtMultimedia
load_PySide2_QtPrintSupport = load_PyQt5_QtPrintSupport
load_PySide2_QtWebKit = load_PyQt5_QtWebKit
load_PySide2_QtWidgets = load_PyQt5_QtWidgets
load_PySide2_uic = load_PyQt5_uic
# PySide2 end


def load_pyqtgraph(finder: ModuleFinder, module: Module) -> None:
    """The pyqtgraph package must be loaded as a package."""
    finder.IncludePackage("pyqtgraph")


def load_pytest(finder: ModuleFinder, module: Module) -> None:
    """
    The pytest package implicitly imports others modules;
    make sure this happens.
    """
    pytest = __import__("pytest")
    for mod in pytest.freeze_includes():
        finder.IncludeModule(mod)


def load_pythoncom(finder: ModuleFinder, module: Module) -> None:
    """
    The pythoncom module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in
    the target directory.
    """
    pythoncom = __import__("pythoncom")
    filename = Path(pythoncom.__file__)
    finder.IncludeFiles(
        filename, Path("lib", filename.name), copy_dependent_files=False
    )


def load_pytz(finder: ModuleFinder, module: Module) -> None:
    """
    The pytz module requires timezone data to be found in a known directory
    or in the zip file where the package is written.
    """
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
            finder.AddConstant("PYTZ_TZDATADIR", str(target_path))
    if data_path.is_dir():
        if module.in_file_system >= 1:
            finder.IncludeFiles(
                data_path, target_path, copy_dependent_files=False
            )
        else:
            finder.ZipIncludeFiles(data_path, Path("pytz", "zoneinfo"))


def load_pywintypes(finder: ModuleFinder, module: Module) -> None:
    """
    The pywintypes module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in the
    target directory.
    """
    pywintypes = __import__("pywintypes")
    filename = Path(pywintypes.__file__)
    finder.IncludeFiles(
        filename, Path("lib", filename.name), copy_dependent_files=False
    )


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """
    The reportlab module loads a submodule rl_settings via exec so force
    its inclusion here.
    """
    finder.IncludeModule("reportlab.rl_settings")


def load_sentry(finder: ModuleFinder, module: Module) -> None:
    """
    The Sentry.io SDK
    """
    finder.IncludeModule("sentry_sdk.integrations.stdlib")
    finder.IncludeModule("sentry_sdk.integrations.excepthook")
    finder.IncludeModule("sentry_sdk.integrations.dedupe")
    finder.IncludeModule("sentry_sdk.integrations.atexit")
    finder.IncludeModule("sentry_sdk.integrations.modules")
    finder.IncludeModule("sentry_sdk.integrations.argv")
    finder.IncludeModule("sentry_sdk.integrations.logging")
    finder.IncludeModule("sentry_sdk.integrations.threading")


def load_scipy(finder: ModuleFinder, module: Module) -> None:
    """
    The scipy module loads items within itself in a way that causes
    problems without the entire package and a number of other subpackages
    being present.
    """
    finder.IncludePackage("scipy._lib")
    finder.IncludePackage("scipy.misc")
    if WIN32:
        finder.ExcludeModule("scipy.spatial.cKDTree")


def load_scipy_linalg(finder: ModuleFinder, module: Module) -> None:
    """
    The scipy.linalg module loads items within itself in a way that causes
    problems without the entire package being present.
    """
    module.global_names.add("norm")
    finder.IncludePackage("scipy.linalg")


def load_scipy_linalg_interface_gen(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The scipy.linalg.interface_gen module optionally imports the pre module;
    ignore the error if this module cannot be found.
    """
    module.ignore_names.add("pre")


def load_scipy_ndimage(finder: ModuleFinder, module: Module) -> None:
    """The scipy.ndimage must be loaded as a package."""
    finder.ExcludeModule("scipy.ndimage.tests")
    finder.IncludePackage("scipy.ndimage")


def load_scipy_sparse_csgraph(finder: ModuleFinder, module: Module) -> None:
    """The scipy.sparse.csgraph must be loaded as a package."""
    finder.ExcludeModule("scipy.sparse.csgraph.tests")
    finder.IncludePackage("scipy.sparse.csgraph")


def load_scipy_sparse_linalg_dsolve_linsolve(
    finder: ModuleFinder, module: Module
) -> None:
    """The scipy.linalg.dsolve.linsolve optionally loads scikits.umfpack."""
    module.ignore_names.add("scikits.umfpack")


def load_scipy_spatial_transform(finder: ModuleFinder, module: Module) -> None:
    """The scipy.spatial.transform must be loaded as a package."""
    finder.IncludePackage("scipy.spatial.transform")
    finder.ExcludeModule("scipy.spatial.transform.tests")


def load_scipy_special(finder: ModuleFinder, module: Module) -> None:
    """The scipy.special must be loaded as a package."""
    finder.IncludePackage("scipy.special")


def load_scipy_special__cephes(finder: ModuleFinder, module: Module) -> None:
    """
    The scipy.special._cephes is an extension module and the scipy module
    imports * from it in places; advertise the global names that are used
    in order to avoid spurious errors about missing modules.
    """
    module.global_names.add("gammaln")


def load_scipy_stats(finder: ModuleFinder, module: Module) -> None:
    """The scipy.stats must be loaded as a package."""
    finder.IncludePackage("scipy.stats")
    finder.ExcludeModule("scipy.stats.tests")


def load_skimage(finder: ModuleFinder, module: Module) -> None:
    """The skimage package."""
    finder.IncludePackage("skimage.io")
    # exclude all tests
    finder.ExcludeModule("skimage.color.tests")
    finder.ExcludeModule("skimage.data.tests")
    finder.ExcludeModule("skimage.draw.tests")
    finder.ExcludeModule("skimage.exposure.tests")
    finder.ExcludeModule("skimage.feature.tests")
    finder.ExcludeModule("skimage.filters.tests")
    finder.ExcludeModule("skimage.graph.tests")
    finder.ExcludeModule("skimage.io.tests")
    finder.ExcludeModule("skimage.measure.tests")
    finder.ExcludeModule("skimage.metrics.tests")
    finder.ExcludeModule("skimage.morphology.tests")
    finder.ExcludeModule("skimage.restoration.tests")
    finder.ExcludeModule("skimage.segmentation.tests")
    finder.ExcludeModule("skimage._shared.tests")
    finder.ExcludeModule("skimage.transform.tests")
    finder.ExcludeModule("skimage.util.tests")
    finder.ExcludeModule("skimage.viewer.tests")


def load_skimage_feature_orb_cy(finder: ModuleFinder, module: Module) -> None:
    """The skimage.feature.orb_cy is a extension that load a module."""
    finder.IncludeModule("skimage.feature._orb_descriptor_positions")


def load_setuptools(finder: ModuleFinder, module: Module) -> None:
    """
    The setuptools must be loaded as a package, to prevent it to break in the
    future.
    """
    finder.IncludePackage("setuptools")


def load_setuptools_extension(finder: ModuleFinder, module: Module) -> None:
    """
    The setuptools.extension module optionally loads
    Pyrex.Distutils.build_ext but its absence is not considered an error.
    """
    module.ignore_names.add("Pyrex.Distutils.build_ext")


def load_site(finder: ModuleFinder, module: Module) -> None:
    """
    The site module optionally loads the sitecustomize and usercustomize
    modules; ignore the error if these modules do not exist.
    """
    module.ignore_names.update(["sitecustomize", "usercustomize"])


def load_sqlite3(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the sqlite3 module requires an additional dll sqlite3.dll to
    be present in the build directory.
    """
    if WIN32 and not MINGW:
        dll_name = "sqlite3.dll"
        dll_path = Path(sys.base_prefix, "DLLs", dll_name)
        if not dll_path.exists():
            dll_path = Path(sys.base_prefix, "Library", "bin", dll_name)
        finder.IncludeFiles(dll_path, Path("lib", dll_name))
    finder.IncludePackage("sqlite3")


def load_six(finder: ModuleFinder, module: Module) -> None:
    """the six module creates fake modules."""
    finder.ExcludeModule("six.moves")


def load_ssl(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the SSL module in Python 3.7+ requires additional dlls to
    be present in the build directory.
    """
    if WIN32 and sys.version_info >= (3, 7) and not MINGW:
        for dll_search in ["libcrypto-*.dll", "libssl-*.dll"]:
            libs_dir = Path(sys.base_prefix, "DLLs")
            for dll_path in libs_dir.glob(dll_search):
                finder.IncludeFiles(dll_path, Path("lib", dll_path.name))


def load_sysconfig(finder: ModuleFinder, module: Module) -> None:
    """The sysconfig module implicitly loads _sysconfigdata."""
    get_data_name = getattr(sysconfig, "_get_sysconfigdata_name", None)
    if get_data_name is None:
        datafile = "_sysconfigdata"
    else:
        if not hasattr(sys, "abiflags"):
            sys.abiflags = ""
        datafile = get_data_name()
    finder.IncludeModule(datafile)


def load_tensorflow(finder: ModuleFinder, module: Module) -> None:
    """The tensorflow package implicitly loads some packages."""
    finder.IncludePackage("tensorboard")
    finder.IncludePackage("tensorflow.compiler")
    finder.IncludePackage("tensorflow.python")


def load_time(finder: ModuleFinder, module: Module) -> None:
    """The time module implicitly loads _strptime; make sure this happens."""
    finder.IncludeModule("_strptime")


def load_tkinter(finder: ModuleFinder, module: Module) -> None:
    """
    The tkinter module has data files that are required to be loaded so
    ensure that they are copied into the directory that is expected at
    runtime.
    """
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
            finder.AddConstant(env_name, str(target_path))
            finder.IncludeFiles(lib_texts, target_path)
            if not MINGW:
                dll_name = dir_name.replace(".", "") + "t.dll"
                dll_path = Path(sys.base_prefix, "DLLs", dll_name)
                finder.IncludeFiles(dll_path, Path("lib", dll_name))


def load_twisted_conch_ssh_transport(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The twisted.conch.ssh.transport module uses __import__ builtin to
    dynamically load different ciphers at runtime.
    """
    finder.IncludePackage("Crypto.Cipher")


def load_twitter(finder: ModuleFinder, module: Module) -> None:
    """
    The twitter module tries to load the simplejson, json and django.utils
    module in an attempt to locate any module that will implement the
    necessary protocol; ignore these modules if they cannot be found.
    """
    module.ignore_names.update(["json", "simplejson", "django.utils"])


def load_uvloop(finder: ModuleFinder, module: Module) -> None:
    """The uvloop module implicitly loads an extension module."""
    finder.IncludeModule("uvloop._noop")


def load_win32api(finder: ModuleFinder, module: Module) -> None:
    """
    The win32api module implicitly loads the pywintypes module; make sure
    this happens.
    """
    finder.ExcludeDependentFiles(module.file)
    finder.IncludeModule("pywintypes")


def load_win32com(finder: ModuleFinder, module: Module) -> None:
    """
    The win32com package manipulates its search path at runtime to include
    the sibling directory called win32comext; simulate that by changing the
    search path in a similar fashion here.
    """
    module.path.append(module.file.parent.parent / "win32comext")


def load_win32file(finder: ModuleFinder, module: Module) -> None:
    """
    The win32file module implicitly loads the pywintypes and win32timezone
    module; make sure this happens.
    """
    finder.IncludeModule("pywintypes")
    finder.IncludeModule("win32timezone")


def load_wx_lib_pubsub_core(finder: ModuleFinder, module: Module) -> None:
    """
    The wx.lib.pubsub.core module modifies the search path which cannot
    be done in a frozen application in the same way; modify the module
    search path here instead so that the right modules are found; note
    that this only works if the import of wx.lib.pubsub.setupkwargs
    occurs first.
    """
    module.path.insert(0, module.file.parent / "kwargs")


def load_Xlib_display(finder: ModuleFinder, module: Module) -> None:
    """
    The Xlib.display module implicitly loads a number of extension modules;
    make sure this happens.
    """
    finder.IncludeModule("Xlib.ext.xtest")
    finder.IncludeModule("Xlib.ext.shape")
    finder.IncludeModule("Xlib.ext.xinerama")
    finder.IncludeModule("Xlib.ext.record")
    finder.IncludeModule("Xlib.ext.composite")
    finder.IncludeModule("Xlib.ext.randr")


def load_Xlib_support_connect(finder: ModuleFinder, module: Module) -> None:
    """
    The Xlib.support.connect module implicitly loads a platform specific
    module; make sure this happens.
    """
    if sys.platform.split("-", maxsplit=1)[0] == "OpenVMS":
        module_name = "vms_connect"
    else:
        module_name = "unix_connect"
    finder.IncludeModule(f"Xlib.support.{module_name}")


def load_Xlib_XK(finder: ModuleFinder, module: Module) -> None:
    """
    The Xlib.XK module implicitly loads some keysymdef modules; make sure
    this happens.
    """
    finder.IncludeModule("Xlib.keysymdef.miscellany")
    finder.IncludeModule("Xlib.keysymdef.latin1")


def load_xml_etree_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """
    The xml.etree.cElementTree module implicitly loads the
    xml.etree.ElementTree module; make sure this happens.
    """
    finder.IncludeModule("xml.etree.ElementTree")


def load_zmq(finder: ModuleFinder, module: Module) -> None:
    """The zmq package loads zmq.backend.cython dynamically and links
    dynamically to zmq.libzmq or shared lib. Tested in pyzmq 16.0.4 (py36),
    19.0.2 (MSYS2 py39) up to 22.2.1 (from pip and from conda)."""
    finder.IncludePackage("zmq.backend.cython")
    if WIN32:
        # For pyzmq 22 the libzmq dependencies are located in
        # site-packages/pyzmq.libs
        libzmq_folder = "pyzmq.libs"
        libs_dir = module.path[0].parent / libzmq_folder
        if libs_dir.exists():
            finder.IncludeFiles(libs_dir, Path("lib", libzmq_folder))
    # Include the bundled libzmq library, if it exists
    try:
        finder.IncludeModule("zmq.libzmq")
    except ImportError:
        pass  # assume libzmq is not bundled
    finder.ExcludeModule("zmq.tests")


def load_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """The zoneinfo package requires timezone data, that
    can be the in tzdata package, if installed."""
    tzdata: Optional[Module] = None
    source: Optional[Path] = None
    try:
        tzdata = finder.IncludePackage("tzdata")
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
            finder.IncludeFiles(source, target, copy_dependent_files=False)
            finder.AddConstant("PYTHONTZPATH", str(source))
    if tzdata is None:
        return
    # when the tzdata exists, copy other files in this directory
    source = tzdata.path[0]
    target = Path("lib", "tzdata")
    if tzdata.in_file_system >= 1:
        finder.IncludeFiles(source, target, copy_dependent_files=False)
    else:
        finder.ZipIncludeFiles(source, "tzdata")


load_backports_zoneinfo = load_zoneinfo


def load_zope_component(finder: ModuleFinder, module: Module) -> None:
    """
    The zope.component package requires the presence of the pkg_resources
    module but it uses a dynamic, not static import to do its work.
    """
    finder.IncludeModule("pkg_resources")


def missing_gdk(finder: ModuleFinder, caller: Module) -> None:
    """
    The gdk module is buried inside gtk so there is no need to concern
    ourselves with an error saying that it cannot be found.
    """
    caller.ignore_names.add("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """
    This module is not necessairly present so ignore it when it cannot be
    found.
    """
    caller.ignore_names.add("ltihooks")


def missing_readline(finder: ModuleFinder, caller: Module) -> None:
    """
    The readline module is not normally present on Windows but it also may be
    so instead of excluding it completely, ignore it if it can't be found.
    """
    if WIN32:
        caller.ignore_names.add("readline")
