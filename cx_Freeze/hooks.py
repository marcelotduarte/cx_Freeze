import glob
import os
import sys
import sysconfig
from typing import Any, Optional, Tuple

from .common import code_object_replace
from .finder import ModuleFinder
from .module import Module

MINGW = sysconfig.get_platform() == "mingw"
WIN32 = sys.platform == "win32"


def initialize(finder: ModuleFinder) -> None:
    """
    Upon initialization of the finder, this routine is called to set up some
    automatic exclusions for various platforms.
    """
    # py2 modules that have been removed or renamed in py3
    import collections.abc

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
    if not sys.platform.startswith("OpenVMS"):
        finder.ExcludeModule("vms_lib")


def load_aiofiles(finder: ModuleFinder, module: Module) -> None:
    """The aiofiles must be loaded as a package."""
    finder.IncludePackage("aiofiles")


def load_asyncio(finder: ModuleFinder, module: Module) -> None:
    """The asyncio must be loaded as a package."""
    finder.IncludePackage("asyncio")


def load_babel(finder: ModuleFinder, module: Module) -> None:
    """The babel must be loaded as a package, and has pickeable data."""
    finder.IncludePackage("babel")
    module.store_in_file_system = True


def load_bcrypt(finder: ModuleFinder, module: Module) -> None:
    """The bcrypt package requires the _cffi_backend module (loaded implicitly)"""
    finder.IncludeModule("_cffi_backend")


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
    if not module.in_file_system:
        if sys.version_info < (3, 7):
            module.store_in_file_system = True
            return
        cacert = __import__("certifi").where()
        target = "certifi/" + os.path.basename(cacert)
        finder.ZipIncludeFiles(cacert, target)


def load_cffi_cparser(finder: ModuleFinder, module: Module) -> None:
    """The cffi.cparser module can use a extension if present."""
    try:
        cffi = __import__("cffi", fromlist=["_pycparser"])
        pycparser = getattr(cffi, "_pycparser")
        finder.IncludeModule(pycparser.__name__)
    except (ImportError, AttributeError):
        finder.ExcludeModule("cffi._pycparser")


def load_crc32c(finder: ModuleFinder, module: Module) -> None:
    """The google.crc32c module requires _cffi_backend module"""
    finder.IncludeModule("_cffi_backend")


def load_clr(finder: ModuleFinder, module: Module) -> None:
    """
    The pythonnet package (imported as 'clr') needs Python.Runtime.dll
    in runtime.
    """
    module_dir = os.path.dirname(module.file)
    dll_name = "Python.Runtime.dll"
    finder.IncludeFiles(
        os.path.join(module_dir, dll_name), os.path.join("lib", dll_name)
    )


def load_cryptography_hazmat_bindings__openssl(
    finder: ModuleFinder, module: Module
) -> None:
    """The cryptography module requires the cffi module"""
    finder.IncludeModule("cffi")


def load_cryptography_hazmat_bindings__padding(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The cryptography module requires the _cffi_backend module
    (loaded implicitly).
    """
    finder.IncludeModule("_cffi_backend")


def load_Crypto_Cipher(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Cipher subpackage of pycryptodome package."""
    if not module.in_file_system:
        finder.IncludePackage(module.name)


def load_Crypto_Hash(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Hash subpackage of pycryptodome package."""
    if not module.in_file_system:
        finder.IncludePackage(module.name)


def load_Crypto_Math(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Math subpackage of pycryptodome package."""
    if not module.in_file_system:
        finder.IncludePackage(module.name)


def load_Crypto_Protocol(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Protocol subpackage of pycryptodome package."""
    if not module.in_file_system:
        finder.IncludePackage(module.name)


def load_Crypto_PublicKey(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.PublicKey subpackage of pycryptodome package."""
    if not module.in_file_system:
        finder.IncludePackage(module.name)


def load_Crypto_Util(finder: ModuleFinder, module: Module) -> None:
    """The Crypto.Util subpackage of pycryptodome package."""
    if not module.in_file_system:
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
    if not module.in_file_system and module.code is not None:
        new_code = compile(PYCRYPTODOME_CODE_STR, module.file, "exec")
        co_func = new_code.co_consts[2]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i in range(len(consts)):
            if isinstance(consts[i], type(code)) and consts[i].co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the _ctypes module in Python 3.8+ requires an additional dll
    libffi-7.dll to be present in the build directory.
    """
    if WIN32 and sys.version_info >= (3, 8) and not MINGW:
        dll_name = "libffi-7.dll"
        dll_path = os.path.join(sys.base_prefix, "DLLs", dll_name)
        finder.IncludeFiles(dll_path, os.path.join("lib", dll_name))


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
    module.IgnoreName("optik")


def load_dummy_threading(finder: ModuleFinder, module: Module) -> None:
    """
    The dummy_threading module plays games with the name of the threading
    module for its own purposes; ignore that here.
    """
    finder.ExcludeModule("_dummy_threading")


def load_ftplib(finder: ModuleFinder, module: Module) -> None:
    """
    The ftplib module attempts to import the SOCKS module; ignore this
    module if it cannot be found.
    """
    module.IgnoreName("SOCKS")


def load_gevent(finder: ModuleFinder, module: Module) -> None:
    """The gevent must be loaded as a package."""
    finder.IncludePackage("gevent")


def load_GifImagePlugin(finder: ModuleFinder, module: Module) -> None:
    """The GifImagePlugin module optionally imports the _imaging_gif module"""
    module.IgnoreName("_imaging_gif")


def load_glib(finder: ModuleFinder, module: Module) -> None:
    """Ignore globals that are imported."""
    module.AddGlobalName("GError")
    module.AddGlobalName("IOChannel")
    module.AddGlobalName("IO_ERR")
    module.AddGlobalName("IO_FLAG_APPEND")
    module.AddGlobalName("IO_FLAG_GET_MASK")
    module.AddGlobalName("IO_FLAG_IS_READABLE")
    module.AddGlobalName("IO_FLAG_IS_SEEKABLE")
    module.AddGlobalName("IO_FLAG_IS_WRITEABLE")
    module.AddGlobalName("IO_FLAG_MASK")
    module.AddGlobalName("IO_FLAG_NONBLOCK")
    module.AddGlobalName("IO_FLAG_SET_MASK")
    module.AddGlobalName("IO_HUP")
    module.AddGlobalName("IO_IN")
    module.AddGlobalName("IO_NVAL")
    module.AddGlobalName("IO_OUT")
    module.AddGlobalName("IO_PRI")
    module.AddGlobalName("IO_STATUS_AGAIN")
    module.AddGlobalName("IO_STATUS_EOF")
    module.AddGlobalName("IO_STATUS_ERROR")
    module.AddGlobalName("IO_STATUS_NORMAL")
    module.AddGlobalName("Idle")
    module.AddGlobalName("MainContext")
    module.AddGlobalName("MainLoop")
    module.AddGlobalName("OPTION_ERROR")
    module.AddGlobalName("OPTION_ERROR_BAD_VALUE")
    module.AddGlobalName("OPTION_ERROR_FAILED")
    module.AddGlobalName("OPTION_ERROR_UNKNOWN_OPTION")
    module.AddGlobalName("OPTION_FLAG_FILENAME")
    module.AddGlobalName("OPTION_FLAG_HIDDEN")
    module.AddGlobalName("OPTION_FLAG_IN_MAIN")
    module.AddGlobalName("OPTION_FLAG_NOALIAS")
    module.AddGlobalName("OPTION_FLAG_NO_ARG")
    module.AddGlobalName("OPTION_FLAG_OPTIONAL_ARG")
    module.AddGlobalName("OPTION_FLAG_REVERSE")
    module.AddGlobalName("OPTION_REMAINING")
    module.AddGlobalName("OptionContext")
    module.AddGlobalName("OptionGroup")
    module.AddGlobalName("PRIORITY_DEFAULT")
    module.AddGlobalName("PRIORITY_DEFAULT_IDLE")
    module.AddGlobalName("PRIORITY_HIGH")
    module.AddGlobalName("PRIORITY_HIGH_IDLE")
    module.AddGlobalName("PRIORITY_LOW")
    module.AddGlobalName("Pid")
    module.AddGlobalName("PollFD")
    module.AddGlobalName("SPAWN_CHILD_INHERITS_STDIN")
    module.AddGlobalName("SPAWN_DO_NOT_REAP_CHILD")
    module.AddGlobalName("SPAWN_FILE_AND_ARGV_ZERO")
    module.AddGlobalName("SPAWN_LEAVE_DESCRIPTORS_OPEN")
    module.AddGlobalName("SPAWN_SEARCH_PATH")
    module.AddGlobalName("SPAWN_STDERR_TO_DEV_NULL")
    module.AddGlobalName("SPAWN_STDOUT_TO_DEV_NULL")
    module.AddGlobalName("Source")
    module.AddGlobalName("Timeout")
    module.AddGlobalName("child_watch_add")
    module.AddGlobalName("filename_display_basename")
    module.AddGlobalName("filename_display_name")
    module.AddGlobalName("filename_from_utf8")
    module.AddGlobalName("get_application_name")
    module.AddGlobalName("get_current_time")
    module.AddGlobalName("get_prgname")
    module.AddGlobalName("glib_version")
    module.AddGlobalName("idle_add")
    module.AddGlobalName("io_add_watch")
    module.AddGlobalName("main_context_default")
    module.AddGlobalName("main_depth")
    module.AddGlobalName("markup_escape_text")
    module.AddGlobalName("set_application_name")
    module.AddGlobalName("set_prgname")
    module.AddGlobalName("source_remove")
    module.AddGlobalName("spawn_async")
    module.AddGlobalName("timeout_add")
    module.AddGlobalName("timeout_add_seconds")


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


def load_hashlib(finder: ModuleFinder, module: Module) -> None:
    """
    hashlib's fallback modules don't exist if the equivalent OpenSSL
    algorithms are loaded from _hashlib, so we can ignore the error.
    """
    module.IgnoreName("_md5")
    module.IgnoreName("_sha")
    module.IgnoreName("_sha256")
    module.IgnoreName("_sha512")


def load_h5py(finder: ModuleFinder, module: Module) -> None:
    """h5py module has a number of implicit imports"""
    finder.IncludeModule("h5py.defs")
    finder.IncludeModule("h5py.utils")
    finder.IncludeModule("h5py._proxy")
    try:
        api_gen = __import__("h5py", fromlist=["api_gen"]).api_gen
        finder.IncludeModule(api_gen.__name__)
    except ImportError:
        pass
    finder.IncludeModule("h5py._errors")
    finder.IncludeModule("h5py.h5ac")


def load_idna(finder: ModuleFinder, module: Module) -> None:
    """The idna module implicitly loads data; make sure this happens."""
    finder.IncludeModule("idna.idnadata")


def load_lxml(finder: ModuleFinder, module: Module) -> None:
    """The lxml package uses an extension."""
    finder.IncludeModule("lxml._elementpath")


def load_matplotlib(finder: ModuleFinder, module: Module) -> None:
    """
    The matplotlib package requires mpl-data in a subdirectory of the
    package.
    """
    MATPLOTLIB_CODE_STR = """
def _get_data_path():
    return os.path.join(os.path.dirname(sys.executable), '{}')
"""
    data_path = __import__("matplotlib").get_data_path()
    target_path = os.path.join("lib", module.name, "mpl-data")
    finder.IncludeFiles(data_path, target_path, copy_dependent_files=False)
    if module.code is not None:
        code_str = MATPLOTLIB_CODE_STR.format(target_path)
        new_code = compile(code_str, module.file, "exec")
        co_func = new_code.co_consts[0]
        name = co_func.co_name
        code = module.code
        consts = list(code.co_consts)
        for i in range(len(consts)):
            if isinstance(consts[i], type(code)) and consts[i].co_name == name:
                consts[i] = co_func
                break
        module.code = code_object_replace(code, co_consts=consts)
    finder.ExcludeModule("matplotlib.tests")
    finder.IncludePackage("matplotlib")


def load_numpy(finder: ModuleFinder, module: Module) -> None:
    """The numpy must be loaded as a package."""
    finder.ExcludeModule("numpy.random._examples")
    finder.IncludePackage("numpy")
    if not module.in_file_system:
        # version 1.18.3+ changed the location of dll/so
        numpy = __import__("numpy")
        version = tuple([int(n) for n in numpy.__version__.split(".")])
        del numpy
        if version >= (1, 18, 3):
            module.store_in_file_system = True


def load_numpy_core_multiarray(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.core.multiarray module is an extension module and the numpy
    module imports * from this module; define the list of global names
    available to this module in order to avoid spurious errors about missing
    modules.
    """
    module.AddGlobalName("arange")


def load_numpy_core_numerictypes(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.core.numerictypes module adds a number of items to itself
    dynamically; define these to avoid spurious errors about missing
    modules.
    """
    module.AddGlobalName("bool_")
    module.AddGlobalName("cdouble")
    module.AddGlobalName("complexfloating")
    module.AddGlobalName("csingle")
    module.AddGlobalName("double")
    module.AddGlobalName("float64")
    module.AddGlobalName("float_")
    module.AddGlobalName("inexact")
    module.AddGlobalName("intc")
    module.AddGlobalName("int32")
    module.AddGlobalName("number")
    module.AddGlobalName("single")


def load_numpy_core_umath(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.core.umath module is an extension module and the numpy module
    imports * from this module; define the list of global names available
    to this module in order to avoid spurious errors about missing
    modules.
    """
    module.AddGlobalName("add")
    module.AddGlobalName("absolute")
    module.AddGlobalName("arccos")
    module.AddGlobalName("arccosh")
    module.AddGlobalName("arcsin")
    module.AddGlobalName("arcsinh")
    module.AddGlobalName("arctan")
    module.AddGlobalName("arctanh")
    module.AddGlobalName("bitwise_and")
    module.AddGlobalName("bitwise_or")
    module.AddGlobalName("bitwise_xor")
    module.AddGlobalName("ceil")
    module.AddGlobalName("conj")
    module.AddGlobalName("conjugate")
    module.AddGlobalName("cosh")
    module.AddGlobalName("divide")
    module.AddGlobalName("fabs")
    module.AddGlobalName("floor")
    module.AddGlobalName("floor_divide")
    module.AddGlobalName("fmod")
    module.AddGlobalName("greater")
    module.AddGlobalName("hypot")
    module.AddGlobalName("invert")
    module.AddGlobalName("isfinite")
    module.AddGlobalName("isinf")
    module.AddGlobalName("isnan")
    module.AddGlobalName("less")
    module.AddGlobalName("left_shift")
    module.AddGlobalName("log")
    module.AddGlobalName("logical_and")
    module.AddGlobalName("logical_not")
    module.AddGlobalName("logical_or")
    module.AddGlobalName("logical_xor")
    module.AddGlobalName("maximum")
    module.AddGlobalName("minimum")
    module.AddGlobalName("multiply")
    module.AddGlobalName("negative")
    module.AddGlobalName("not_equal")
    module.AddGlobalName("power")
    module.AddGlobalName("remainder")
    module.AddGlobalName("right_shift")
    module.AddGlobalName("sign")
    module.AddGlobalName("sinh")
    module.AddGlobalName("sqrt")
    module.AddGlobalName("tan")
    module.AddGlobalName("tanh")
    module.AddGlobalName("true_divide")


def load_numpy_distutils_command_scons(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The numpy.distutils.command.scons module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.IgnoreName("numscons")


def load_numpy_distutils_misc_util(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The numpy.distutils.misc_util module optionally imports the numscons
    module; ignore the error if the module cannot be found.
    """
    module.IgnoreName("numscons")


def load_numpy_distutils_system_info(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The numpy.distutils.system_info module optionally imports the Numeric
    module; ignore the error if the module cannot be found.
    """
    module.IgnoreName("Numeric")


def load_numpy_f2py___version__(finder: ModuleFinder, module: Module) -> None:
    """
    The numpy.f2py.__version__ module optionally imports the __svn_version__
    module; ignore the error if the module cannot be found.
    """
    module.IgnoreName("__svn_version__")


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
    module.AddGlobalName("rand")
    module.AddGlobalName("randn")


def load_Numeric(finder: ModuleFinder, module: Module) -> None:
    """
    The Numeric module optionally loads the dotblas module; ignore the error
    if this modules does not exist.
    """
    module.IgnoreName("dotblas")


def load_pikepdf(finder: ModuleFinder, module: Module) -> None:
    """The pikepdf must be loaded as a package."""
    finder.IncludePackage("pikepdf")


def load_PIL(finder: ModuleFinder, module: Module) -> None:
    """The Pillow must be loaded as a package."""
    finder.IncludePackage("PIL")


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
    filename = os.path.join(module.path[0], "libsys.sql")
    finder.IncludeFiles(filename, os.path.basename(filename))


def load_pty(finder: ModuleFinder, module: Module) -> None:
    """The sgi module is not needed for this module to function."""
    module.IgnoreName("sgi")


def load_pycparser(finder: ModuleFinder, module: Module) -> None:
    """
    These files are missing which causes
    permission denied issues on windows when they are regenerated.
    """
    finder.IncludeModule("pycparser.lextab")
    finder.IncludeModule("pycparser.yacctab")


def load_pygments(finder: ModuleFinder, module: Module) -> None:
    """The pygments package dynamically load styles."""
    finder.IncludePackage("pygments.styles")
    finder.IncludePackage("pygments.lexers")
    finder.IncludePackage("pygments.formatters")


def load_pytest(finder: ModuleFinder, module: Module) -> None:
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
    finder.IncludeFiles(
        pythoncom.__file__,
        os.path.join("lib", os.path.basename(pythoncom.__file__)),
        copy_dependent_files=False,
    )


def load_pytz(finder: ModuleFinder, module: Module) -> None:
    """
    The pytz module requires timezone data to be found in a known directory
    or in the zip file where the package is written.
    """
    target_path = os.path.join("lib", "pytz", "zoneinfo")
    data_path = os.path.join(module.path[0], "zoneinfo")
    if not os.path.isdir(data_path):
        # Fedora (and possibly other systems) use a separate location to
        # store timezone data so look for that here as well
        pytz = __import__("pytz")
        data_path = (
            getattr(pytz, "_tzinfo_dir", None)
            or os.getenv("PYTZ_TZDATADIR")
            or "/usr/share/zoneinfo"
        )
        if data_path.endswith(os.sep):
            data_path = data_path[:-1]
        if os.path.isdir(data_path):
            finder.AddConstant("PYTZ_TZDATADIR", target_path)
    if os.path.isdir(data_path):
        if module.in_file_system:
            finder.IncludeFiles(
                data_path, target_path, copy_dependent_files=False
            )
        else:
            finder.ZipIncludeFiles(data_path, "pytz/zoneinfo")


def load_pywintypes(finder: ModuleFinder, module: Module) -> None:
    """
    The pywintypes module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in the
    target directory.
    """
    pywintypes = __import__("pywintypes")
    finder.IncludeFiles(
        pywintypes.__file__,
        os.path.join("lib", os.path.basename(pywintypes.__file__)),
        copy_dependent_files=False,
    )


# cache the QtCore module
_qtcore = None


def _qt_implementation(module: Module) -> Tuple[str, Any]:
    """Helper function to get name (PyQt5) and the QtCore module."""
    global _qtcore
    name = module.name.split(".")[0]
    if _qtcore is None:
        try:
            _qtcore = __import__(name, fromlist=["QtCore"]).QtCore
        except RuntimeError:
            print(
                "WARNING: Tried to load multiple incompatible Qt wrappers. "
                "Some incorrect files may be copied."
            )
    return name, _qtcore


def copy_qt_plugins(plugins, finder, qtcore):
    """Helper function to find and copy Qt plugins."""

    # Qt Plugins can either be in a plugins directory next to the Qt libraries,
    # or in other locations listed by QCoreApplication.libraryPaths()
    dir0 = os.path.join(os.path.dirname(qtcore.__file__), "plugins")
    for libpath in qtcore.QCoreApplication.libraryPaths() + [dir0]:
        sourcepath = os.path.join(str(libpath), plugins)
        if os.path.exists(sourcepath):
            finder.IncludeFiles(sourcepath, plugins)


def load_PyQt5_phonon(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, phonon5.dll requires an additional dll phonon_ds94.dll to
    be present in the build directory inside a folder phonon_backend.
    """
    if module.in_file_system:
        return
    _, qtcore = _qt_implementation(module)
    if WIN32:
        copy_qt_plugins("phonon_backend", finder, qtcore)


def sip_module_name(qtcore) -> str:
    """
    Returns the name of the sip module to import.
    (As of 5.11, the distributed wheels no longer provided for the sip module
    outside of the PyQt5 namespace).
    """
    version_string = qtcore.PYQT_VERSION_STR
    try:
        pyqt_version_ints = tuple(int(c) for c in version_string.split("."))
        if pyqt_version_ints >= (5, 11):
            return "PyQt5.sip"
    except Exception:
        pass
    return "sip"


def load_PyQt5_QtCore(finder: ModuleFinder, module: Module) -> None:
    """
    The PyQt5.QtCore module implicitly imports the sip module and,
    depending on configuration, the PyQt5._qt module.
    """
    if module.in_file_system:
        return
    name, qtcore = _qt_implementation(module)
    finder.IncludeModule(sip_module_name(qtcore))
    try:
        finder.IncludeModule(f"{name}._qt")
    except ImportError:
        pass


def load_PyQt5_Qt(finder: ModuleFinder, module: Module) -> None:
    """
    The PyQt5.Qt module is an extension module which imports a number of
    other modules and injects their namespace into its own. It seems a
    foolish way of doing things but perhaps there is some hidden advantage
    to this technique over pure Python; ignore the absence of some of
    the modules since not every installation includes all of them.
    """
    if module.in_file_system:
        return
    name, _ = _qt_implementation(module)
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


def load_PyQt5_uic(finder: ModuleFinder, module: Module) -> None:
    """
    The uic module makes use of "plugins" that need to be read directly and
    cannot be frozen; the PyQt5.QtWebKit and PyQt5.QtNetwork modules are
    also implicity loaded.
    """
    if module.in_file_system:
        return
    name, _ = _qt_implementation(module)
    source_dir = os.path.join(module.path[0], "widget-plugins")
    finder.IncludeFiles(source_dir, f"{name}.uic.widget-plugins")
    finder.IncludeModule(f"{name}.QtNetwork")
    try:
        finder.IncludeModule(f"{name}.QtWebKit")
    except ImportError:
        pass


def _QtGui(finder, module, version_str):
    name, qtcore = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtCore")
    copy_qt_plugins("imageformats", finder, qtcore)
    if version_str >= "5":
        # On Qt5, we need the platform plugins. For simplicity, we just copy
        # any that are installed.
        copy_qt_plugins("platforms", finder, qtcore)


def load_PyQt5_QtGui(finder: ModuleFinder, module: Module) -> None:
    """
    There is a chance that GUI will use some image formats
    add the image format plugins.
    """
    if module.in_file_system:
        return
    _, qtcore = _qt_implementation(module)
    _QtGui(finder, module, qtcore.QT_VERSION_STR)


def load_PyQt5_QtWidgets(finder: ModuleFinder, module: Module) -> None:
    if module.in_file_system:
        return
    finder.IncludeModule("PyQt5.QtGui")


def load_PyQt5_QtWebKit(finder: ModuleFinder, module: Module) -> None:
    if module.in_file_system:
        return
    name, _ = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtNetwork")
    finder.IncludeModule(f"{name}.QtGui")


def load_PyQt5_QtMultimedia(finder: ModuleFinder, module: Module) -> None:
    if module.in_file_system:
        return
    name, qtcore = _qt_implementation(module)
    finder.IncludeModule(f"{name}.QtCore")
    finder.IncludeModule(f"{name}.QtMultimediaWidgets")
    copy_qt_plugins("mediaservice", finder, qtcore)


def load_PyQt5_QtPrintSupport(finder: ModuleFinder, module: Module) -> None:
    if module.in_file_system:
        return
    _, qtcore = _qt_implementation(module)
    copy_qt_plugins("printsupport", finder, qtcore)


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """
    The reportlab module loads a submodule rl_settings via exec so force
    its inclusion here.
    """
    finder.IncludeModule("reportlab.rl_settings")


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
    module.AddGlobalName("norm")
    finder.IncludePackage("scipy.linalg")


def load_scipy_linalg_interface_gen(
    finder: ModuleFinder, module: Module
) -> None:
    """
    The scipy.linalg.interface_gen module optionally imports the pre module;
    ignore the error if this module cannot be found.
    """
    module.IgnoreName("pre")


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
    module.IgnoreName("scikits.umfpack")


def load_scipy_special(finder: ModuleFinder, module: Module) -> None:
    """The scipy.special must be loaded as a package."""
    finder.IncludePackage("scipy.special")


def load_scipy_special__cephes(finder: ModuleFinder, module: Module) -> None:
    """
    The scipy.special._cephes is an extension module and the scipy module
    imports * from it in places; advertise the global names that are used
    in order to avoid spurious errors about missing modules.
    """
    module.AddGlobalName("gammaln")


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
    module.IgnoreName("Pyrex.Distutils.build_ext")


def load_site(finder: ModuleFinder, module: Module) -> None:
    """
    The site module optionally loads the sitecustomize and usercustomize
    modules; ignore the error if these modules do not exist.
    """
    module.IgnoreName("sitecustomize")
    module.IgnoreName("usercustomize")


def load_sqlite3(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the sqlite3 module requires an additional dll sqlite3.dll to
    be present in the build directory.
    """
    if WIN32 and not MINGW:
        dll_name = "sqlite3.dll"
        dll_path = os.path.join(sys.base_prefix, "DLLs", dll_name)
        if not os.path.exists(dll_path):
            dll_path = os.path.join(
                sys.base_prefix, "Library", "bin", dll_name
            )
        finder.IncludeFiles(dll_path, os.path.join("lib", dll_name))
    finder.IncludePackage("sqlite3")


def load_ssl(finder: ModuleFinder, module: Module) -> None:
    """
    In Windows, the SSL module in Python 3.7+ requires additional dlls to
    be present in the build directory.
    """
    if WIN32 and sys.version_info >= (3, 7) and not MINGW:
        for dll_search in ["libcrypto-*.dll", "libssl-*.dll"]:
            for dll_path in glob.glob(
                os.path.join(sys.base_prefix, "DLLs", dll_search)
            ):
                dll_name = os.path.basename(dll_path)
                finder.IncludeFiles(dll_path, os.path.join("lib", dll_name))


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
                    lib_texts = os.path.join(sys.base_prefix, "lib", dir_name)
                else:
                    lib_texts = os.path.join(sys.base_prefix, "tcl", dir_name)
            target_path = os.path.join("lib", "tkinter", dir_name)
            finder.AddConstant(env_name, target_path)
            finder.IncludeFiles(lib_texts, target_path)
            if not MINGW:
                dll_name = dir_name.replace(".", "") + "t.dll"
                dll_path = os.path.join(sys.base_prefix, "DLLs", dll_name)
                finder.IncludeFiles(dll_path, os.path.join("lib", dll_name))


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
    module.IgnoreName("json")
    module.IgnoreName("simplejson")
    module.IgnoreName("django.utils")


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
    base_dir = os.path.dirname(os.path.dirname(module.file))
    module.path.append(os.path.join(base_dir, "win32comext"))


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
    dir_name = os.path.dirname(module.file)
    module.path.insert(0, os.path.join(dir_name, "kwargs"))


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
    if sys.platform.split("-")[0] == "OpenVMS":
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
    """
    The zmq package loads zmq.backend.cython dynamically and links
    dynamically to zmq.libzmq.
    """
    finder.IncludePackage("zmq.backend.cython")
    if WIN32:
        # Not sure yet if this is cross platform
        # Include the bundled libzmq library, if it exists
        try:
            libzmq = __import__("zmq", fromlist=["libzmq"]).libzmq
            filename = os.path.basename(libzmq.__file__)
            finder.IncludeFiles(
                os.path.join(module.path[0], filename), filename
            )
        except ImportError:
            pass  # No bundled libzmq library


def load_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """
    The zoneinfo package requires timezone data, that
    can be the in tzdata package, if installed.
    """
    tzdata: Optional[Module]
    try:
        tzdata = finder.IncludePackage("tzdata")
    except ImportError:
        tzdata = None
    if tzdata is None:
        return
    # store tzdata along with zoneinfo
    tzdata.store_in_file_system = module.in_file_system
    if tzdata.in_file_system:
        finder.IncludeFiles(
            tzdata.path[0],
            os.path.join("lib", "tzdata"),
            copy_dependent_files=False,
        )
    else:
        finder.ZipIncludeFiles(tzdata.path[0], "tzdata")


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
    caller.IgnoreName("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """
    This module is not necessairly present so ignore it when it cannot be
    found.
    """
    caller.IgnoreName("ltihooks")


def missing_readline(finder: ModuleFinder, caller: Module) -> None:
    """
    The readline module is not normally present on Windows but it also may be
    so instead of excluding it completely, ignore it if it can't be found.
    """
    if WIN32:
        caller.IgnoreName("readline")
