"""A collection of functions which are triggered automatically by finder when
certain packages are included or not found.
"""

# ruff: noqa: ARG001
from __future__ import annotations

import sys
import sysconfig
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_CONDA, IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import CONCURRENT_FUTURES_GLOBAL_NAMES
from cx_Freeze.hooks.qthooks import get_qt_plugins_paths  # noqa: F401

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def load_abc(finder: ModuleFinder, module: Module) -> None:
    """Optimize abc module."""
    try:
        finder.include_module("_abc")
        module.exclude_names.add("_py_abc")
    except ImportError:
        finder.include_module("_py_abc")
        module.ignore_names.add("_abc")


def load_aiofiles(finder: ModuleFinder, module: Module) -> None:
    """The aiofiles must be loaded as a package."""
    finder.include_package("aiofiles")


def load_argon2(finder: ModuleFinder, module: Module) -> None:
    """The argon2-cffi package requires the _cffi_backend module
    (loaded implicitly).
    """
    if module.distribution is None:
        module.update_distribution("argon2-cffi")
        finder.include_module("_cffi_backend")


def load_babel(finder: ModuleFinder, module: Module) -> None:
    """The babel must be loaded as a package, and has pickeable data."""
    finder.include_package("babel")
    module.in_file_system = 1


def load_bcrypt(finder: ModuleFinder, module: Module) -> None:
    """The bcrypt < 4.0 package requires the _cffi_backend module
    (loaded implicitly).
    """
    # bcrypt < 4 supports Python <= 3.10
    if module.distribution is None or module.distribution.version[0] < 4:
        finder.include_module("_cffi_backend")


def load_boto(finder: ModuleFinder, module: Module) -> None:
    """The boto package uses 'six' fake modules."""
    finder.exclude_module("boto.vendored.six.moves")


def load_boto3(finder: ModuleFinder, module: Module) -> None:
    """The boto3 package."""
    finder.include_package("boto3.dynamodb")
    finder.include_package("boto3.ec2")
    finder.include_package("boto3.s3")
    finder.include_files(module.file.parent / "data", "lib/boto3/data")


def load_ceODBC(finder: ModuleFinder, module: Module) -> None:
    """The ceODBC module implicitly imports both datetime and decimal;
    make sure this happens.
    """
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_certifi(finder: ModuleFinder, module: Module) -> None:
    """The certifi package uses importlib.resources to locate the cacert.pem
    in zip packages.
    """
    if module.in_file_system == 0:
        cacert = Path(__import__("certifi").where())
        finder.zip_include_files(cacert, Path("certifi", cacert.name))


def load__cffi_backend(finder: ModuleFinder, module: Module) -> None:
    """Add the cffi metadata for _cffi_backend module."""
    module.update_distribution("cffi")


def load_cffi_cparser(finder: ModuleFinder, module: Module) -> None:
    """The cffi.cparser module can use a extension if present."""
    try:
        finder.include_module("cffi._pycparser")
    except ImportError:
        module.ignore_names.add("cffi._pycparser")


def load_charset_normalizer(finder: ModuleFinder, module: Module) -> None:
    """The charset_normalizer package."""
    finder.exclude_module("charset_normalizer.cli")


def load_charset_normalizer_md(finder: ModuleFinder, module: Module) -> None:
    """The charset_normalizer package implicitly imports a extension module."""
    mypyc = module.file.parent / ("md__mypyc" + "".join(module.file.suffixes))
    if mypyc.exists():
        finder.include_module("charset_normalizer.md__mypyc")


def load_collections(finder: ModuleFinder, module: Module) -> None:
    """Sets the alias for collections.abc."""
    try:
        finder.include_module("collections.abc")
    except ImportError:
        # collections.abc module does not exist in Python 3.13+
        # >>> _sys.modules['collections.abc'] = _collections_abc
        finder.add_alias("collections.abc", "_collections_abc")


def load_concurrent_futures(finder: ModuleFinder, module: Module) -> None:
    """Ignore names that should not be confused with modules to be imported."""
    module.global_names.update(CONCURRENT_FUTURES_GLOBAL_NAMES)


def load_crc32c(finder: ModuleFinder, module: Module) -> None:
    """The google.crc32c module requires _cffi_backend module."""
    finder.include_module("_cffi_backend")


def load_cryptography(finder: ModuleFinder, module: Module) -> None:
    """The cryptography module requires the _cffi_backend module."""
    include_cffi = True
    if module.distribution and module.distribution.requires:
        include_cffi = False
        for req in module.distribution.requires:
            if req.startswith("cffi"):
                include_cffi = True
                break
    if include_cffi:
        finder.include_module("_cffi_backend")


def load_ctypes_util(finder: ModuleFinder, module: Module) -> None:
    """The ctypes.util module should filter import names."""
    if not IS_MACOS:
        finder.exclude_module("ctypes.macholib")
        module.ignore_names.add("ctypes.macholib.dyld")
    if not sys.platform.startswith("aix"):
        module.exclude_names.add("ctypes._aix")


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """The _ctypes module requires an additional dependency to be present
    in the build directory.
    """
    if IS_WINDOWS:
        parts = ["DLLs", "Library/bin"]
        patterns = ["libffi-*.dll", "ffi-*.dll"]
        for part in parts:
            for pattern in patterns:
                for source in Path(sys.base_prefix, part).glob(pattern):
                    target = f"lib/{source.name}"
                    finder.lib_files[source] = target
                    finder.include_files(source, target)
    # Python 3.14+
    with suppress(ImportError):
        finder.include_module("ctypes._layout")


def load_cx_Oracle(finder: ModuleFinder, module: Module) -> None:
    """The cx_Oracle module implicitly imports datetime; make sure this
    happens.
    """
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_datetime(finder: ModuleFinder, module: Module) -> None:
    """Optimize datetime module."""
    if "_pydatetime" in sys.stdlib_module_names:  # py 3.12+
        try:
            finder.include_module("_datetime")
            finder.include_module("time")
            module.exclude_names.add("_pydatetime")
        except ImportError:
            finder.include_module("_pydatetime")
            module.ignore_names.add("_datetime")


def load_decimal(finder: ModuleFinder, module: Module) -> None:
    """Optimize decimal module."""
    try:
        finder.include_module("_decimal")
        module.exclude_names.add("_pydecimal")
    except ImportError:
        finder.include_module("_pydecimal")
        module.ignore_names.add("_decimal")


def load_discord(finder: ModuleFinder, module: Module) -> None:
    """py-cord requires its metadata."""
    module.update_distribution("py-cord")


def load_difflib(finder: ModuleFinder, module: Module) -> None:
    """The difflib module uses doctest for tests and shouldn't be imported."""
    module.exclude_names.add("doctest")


def load_flask_compress(finder: ModuleFinder, module: Module) -> None:
    """flask-compress requires its metadata."""
    module.update_distribution("Flask_Compress")


def load_gevent(finder: ModuleFinder, module: Module) -> None:
    """The gevent must be loaded as a package."""
    finder.include_package("gevent")


def load_GifImagePlugin(finder: ModuleFinder, module: Module) -> None:
    """The GifImagePlugin module optionally imports the _imaging_gif module."""
    module.ignore_names.add("_imaging_gif")


def load_googleapiclient(finder: ModuleFinder, module: Module) -> None:
    """Add the googleapiclient metadata for googleapiclient package."""
    module.update_distribution("google_api_python_client")


def load_googleapiclient_discovery(
    finder: ModuleFinder, module: Module
) -> None:
    """The googleapiclient.discovery module needs discovery_cache subpackage
    in file system.
    """
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
    """h5py module has a number of implicit imports."""
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
    """h5py_wrapper module requires future and pytest-runner."""
    finder.include_module("future")
    finder.include_module("ptr")


def load_hashlib(finder: ModuleFinder, module: Module) -> None:
    """The hashlib's fallback modules don't exist if the equivalent OpenSSL
    algorithms are loaded from _hashlib, so we can ignore the error.
    """
    module.ignore_names.update(["_md5", "_sha", "_sha256", "_sha512"])


def load_heapq(finder: ModuleFinder, module: Module) -> None:
    """The heapq module uses doctest for tests and shouldn't be imported."""
    module.exclude_names.add("doctest")


def load_hdfdict(finder: ModuleFinder, module: Module) -> None:
    """The hdfdict module requires h5py_wrapper and PyYAML."""
    finder.include_module("h5py_wrapper")
    finder.include_package("yaml")


def load_idna(finder: ModuleFinder, module: Module) -> None:
    """The idna module implicitly loads data; make sure this happens."""
    finder.include_module("idna.idnadata")


def load_imagej(finder: ModuleFinder, module: Module) -> None:
    """The pyimagej package requires its metadata."""
    module.update_distribution("pyimagej")


def load_jpype(finder: ModuleFinder, module: Module) -> None:
    """The JPype1 package requires its binary."""
    source = module.file.parent.parent / "org.jpype.jar"
    if source.exists():
        finder.include_files(
            source, f"lib/{source.name}", copy_dependent_files=False
        )


def load_librosa(finder: ModuleFinder, module: Module) -> None:
    """The librosa must be loaded as package."""
    finder.include_package("librosa")


def load_llvmlite(finder: ModuleFinder, module: Module) -> None:
    """The llvmlite must be loaded as package."""
    finder.include_package("llvmlite")
    finder.exclude_module("llvmlite.tests")


def load_lxml(finder: ModuleFinder, module: Module) -> None:
    """The lxml package uses an extension."""
    finder.include_module("lxml._elementpath")


def load_markdown(finder: ModuleFinder, module: Module) -> None:
    """The markdown package implicitly loads html.parser; make sure this
    happens.
    """
    finder.include_module("html.parser")


def load_Numeric(finder: ModuleFinder, module: Module) -> None:
    """The Numeric module optionally loads the dotblas module; ignore the error
    if this modules does not exist.
    """
    module.ignore_names.add("dotblas")


def load_orjson(finder: ModuleFinder, module: Module) -> None:
    """The orjson has dynamic imports."""
    finder.include_module("dataclasses")
    finder.include_module("datetime")
    finder.include_module("decimal")
    finder.include_module("enum")
    finder.include_package("json")
    finder.include_module("uuid")
    finder.include_package("zoneinfo")


def load_os(finder: ModuleFinder, module: Module) -> None:
    """Sets the alias for os.path."""
    if "posix" in sys.builtin_module_names:
        finder.add_alias("os.path", "posixpath")
    else:
        finder.add_alias("os.path", "ntpath")


def load_pickle(finder: ModuleFinder, module: Module) -> None:
    """The pickle module uses doctest for tests and shouldn't be imported."""
    module.exclude_names.add("doctest")


def load_pickletools(finder: ModuleFinder, module: Module) -> None:
    """The pickletools module uses doctest that shouldn't be imported."""
    module.exclude_names.add("doctest")


def load_pikepdf(finder: ModuleFinder, module: Module) -> None:
    """The pikepdf must be loaded as a package."""
    finder.include_package("pikepdf")


def load_platform(finder: ModuleFinder, module: Module) -> None:
    """The platform module should filter import names."""
    if not IS_MACOS:
        module.exclude_names.add("plistlib")


def load_plotly(finder: ModuleFinder, module: Module) -> None:
    """The plotly must be loaded as a package."""
    finder.include_package("plotly")


def load_postgresql_lib(finder: ModuleFinder, module: Module) -> None:
    """The postgresql.lib module requires the libsys.sql file to be included
    so make sure that file is included.
    """
    libsys = module.path[0] / "libsys.sql"
    if libsys.exists():
        finder.include_files(libsys, libsys.name)


def load_pty(finder: ModuleFinder, module: Module) -> None:
    """The sgi module is not needed for this module to function."""
    module.ignore_names.add("sgi")


def load_ptr(finder: ModuleFinder, module: Module) -> None:
    """pytest-runner requires its metadata."""
    module.update_distribution("pytest-runner")


def load_pycountry(finder: ModuleFinder, module: Module) -> None:
    """The pycountry module has data in subdirectories."""
    finder.exclude_module("pycountry.tests")
    module.in_file_system = 1


def load_pycparser(finder: ModuleFinder, module: Module) -> None:
    """These files are missing which causes
    permission denied issues on windows when they are regenerated.
    """
    finder.include_module("pycparser.lextab")
    finder.include_module("pycparser.yacctab")


def load_pyodbc(finder: ModuleFinder, module: Module) -> None:
    """The pyodbc module implicitly imports others modules;
    make sure this happens.
    """
    for mod in ("datetime", "decimal", "hashlib", "locale", "uuid"):
        finder.include_module(mod)


def load_pyreadstat(finder: ModuleFinder, module: Module) -> None:
    """The pyreadstat package must be loaded as a package."""
    finder.include_package("pyreadstat")
    finder.include_module("pandas")


def load_pyqtgraph(finder: ModuleFinder, module: Module) -> None:
    """The pyqtgraph package must be loaded as a package."""
    finder.include_package("pyqtgraph")


def load_pytest(finder: ModuleFinder, module: Module) -> None:
    """The pytest package implicitly imports others modules;
    make sure this happens.
    """
    pytest = __import__("pytest")
    for mod in pytest.freeze_includes():
        finder.include_module(mod)


def load_pythoncom(finder: ModuleFinder, module: Module) -> None:
    """The pythoncom module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in
    the target directory.
    """
    pythoncom = __import__("pythoncom")
    filename = Path(pythoncom.__file__)
    finder.include_files(
        filename, f"lib/{filename.name}", copy_dependent_files=IS_MINGW
    )


def load_pywintypes(finder: ModuleFinder, module: Module) -> None:
    """The pywintypes module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in the
    target directory.
    """
    pywintypes = __import__("pywintypes")
    filename = Path(pywintypes.__file__)
    finder.include_files(
        filename, f"lib/{filename.name}", copy_dependent_files=IS_MINGW
    )


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """The reportlab module loads a submodule rl_settings via exec so force
    its inclusion here.
    """
    finder.include_module("reportlab.rl_settings")


def load_sentry_sdk(finder: ModuleFinder, module: Module) -> None:
    """The Sentry.io SDK."""
    finder.include_module("sentry_sdk.integrations.stdlib")
    finder.include_module("sentry_sdk.integrations.excepthook")
    finder.include_module("sentry_sdk.integrations.dedupe")
    finder.include_module("sentry_sdk.integrations.atexit")
    finder.include_module("sentry_sdk.integrations.modules")
    finder.include_module("sentry_sdk.integrations.argv")
    finder.include_module("sentry_sdk.integrations.logging")
    finder.include_module("sentry_sdk.integrations.threading")


def load_site(finder: ModuleFinder, module: Module) -> None:
    """The site module optionally loads the sitecustomize and usercustomize
    modules; ignore the error if these modules do not exist.
    """
    module.ignore_names.update(["sitecustomize", "usercustomize"])


def load_sqlite3(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the sqlite3 module requires an additional dll sqlite3.dll to
    be present in the build directory.
    """
    if IS_WINDOWS:
        parts = ["DLLs", "Library/bin"]
        for part in parts:
            source = Path(sys.base_prefix, part, "sqlite3.dll")
            if source.exists():
                target = f"lib/{source.name}"
                finder.lib_files[source] = target
                finder.include_files(source, target)
    finder.include_module("sqlite3.dump")


def load_sysconfig(finder: ModuleFinder, module: Module) -> None:
    """The sysconfig module implicitly loads _sysconfigdata."""
    if IS_WINDOWS:
        return
    get_data_name = getattr(sysconfig, "_get_sysconfigdata_name", None)
    if get_data_name is None:
        return
    with suppress(ImportError):
        finder.include_module(get_data_name())


def load_time(finder: ModuleFinder, module: Module) -> None:
    """The time module implicitly loads _strptime; make sure this happens."""
    finder.include_module("_strptime")


def load_typing(finder: ModuleFinder, module: Module) -> None:
    """Optimize typing module."""
    finder.add_alias("typing.io", "io")
    finder.add_alias("typing.re", "re")


def load_twisted_conch_ssh_transport(
    finder: ModuleFinder, module: Module
) -> None:
    """The twisted.conch.ssh.transport module uses __import__ builtin to
    dynamically load different ciphers at runtime.
    """
    finder.include_package("Crypto.Cipher")


def load_twitter(finder: ModuleFinder, module: Module) -> None:
    """The twitter module tries to load the simplejson, json and django.utils
    module in an attempt to locate any module that will implement the
    necessary protocol; ignore these modules if they cannot be found.
    """
    module.ignore_names.update(["json", "simplejson", "django.utils"])


def load_uvloop(finder: ModuleFinder, module: Module) -> None:
    """The uvloop module implicitly loads an extension module."""
    finder.include_module("uvloop._noop")


def load_win32api(finder: ModuleFinder, module: Module) -> None:
    """The win32api module implicitly loads the pywintypes module; make sure
    this happens.
    """
    finder.exclude_dependent_files(module.file)
    finder.include_module("pywintypes")


def load_win32com(finder: ModuleFinder, module: Module) -> None:
    """The win32com package manipulates its search path at runtime to include
    the sibling directory called win32comext; simulate that by changing the
    search path in a similar fashion here.
    """
    module.path.append(module.file.parent.parent / "win32comext")


def load_win32file(finder: ModuleFinder, module: Module) -> None:
    """The win32file module implicitly loads the pywintypes and win32timezone
    module; make sure this happens.
    """
    finder.include_module("pywintypes")
    finder.include_module("win32timezone")


def load_win32print(finder: ModuleFinder, module: Module) -> None:
    """The win32print module implicitly loads the pywintypes module;
    make sure this happens.
    """
    finder.include_module("pywintypes")


def load_xml_etree_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """The xml.etree.cElementTree module implicitly loads the
    xml.etree.ElementTree module; make sure this happens.
    """
    finder.include_module("xml.etree.ElementTree")


def load_yaml(finder: ModuleFinder, module: Module) -> None:
    """PyYAML requires its metadata."""
    module.update_distribution("PyYAML")


def load_zlib(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the zlib module requires the zlib.dll to be present in the
    executable directory if using conda-forge. However, the required shared
    library is zlib1.dll in official Python >= 3.12.
    """
    if not IS_WINDOWS:
        return
    if IS_CONDA:
        source = Path(sys.base_prefix, "Library/bin/zlib.dll")
        if source.exists():
            target = source.name
            finder.lib_files[source] = target
    else:
        # ensure zlib1.dll is copied if lief is not used in Python 3.12+
        for source in Path(sys.base_prefix, "DLLs").glob("zlib*.dll"):
            target = f"lib/{source.name}"
            finder.lib_files[source] = target
            finder.include_files(source, target)


#
# missing section
#


def missing_gdk(finder: ModuleFinder, caller: Module) -> None:
    """The gdk module is buried inside gtk so there is no need to concern
    ourselves with an error saying that it cannot be found.
    """
    caller.ignore_names.add("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """The ltihooks module is not necessarily present so ignore it when it
    cannot be found.
    """
    caller.ignore_names.add("ltihooks")


def missing_six_moves(finder: ModuleFinder, caller: Module) -> None:
    """The six module creates fake modules."""
    caller.ignore_names.add("six.moves")


def missing_typing_extensions(finder: ModuleFinder, caller: Module) -> None:
    """The typing_extensions module is not required at runtime, so ignore it
    when it cannot be found.
    """
    caller.ignore_names.add("typing_extensions")
