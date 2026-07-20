"""Hooks triggered by finder when certain packages are included.

Also, take care of missing modules.
"""

# ruff: noqa: ARG001
from __future__ import annotations

import sys
import sysconfig
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_CONDA, IS_MACOS, IS_MINGW, IS_WINDOWS
from cx_Freeze.hooks.global_names import (
    CONCURRENT_FUTURES_GLOBAL_NAMES,
    SQLITE3_GLOBAL_NAMES,
)
from cx_Freeze.hooks.qthooks import get_qt_plugins_paths  # noqa: F401

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


def _include_cffi_backend(finder: ModuleFinder, module: Module) -> None:
    """Include _cffi_backend module when required."""
    include_cffi = False
    if module.distribution and module.distribution.requires:
        for req in module.distribution.requires:
            if req.startswith("cffi"):
                include_cffi = True
                break
    if include_cffi:
        finder.include_module("_cffi_backend")


def load_abc(finder: ModuleFinder, module: Module) -> None:
    """Optimize abc module."""
    try:
        finder.include_module("_abc")
        module.exclude_names.add("_py_abc")
    except ImportError:
        finder.include_module("_py_abc")
        module.ignore_names.add("_abc")


def load_aiofiles(finder: ModuleFinder, module: Module) -> None:
    """Load aiofiles as a package."""
    finder.include_package("aiofiles")


def load__argon2_cffi_bindings(finder: ModuleFinder, module: Module) -> None:
    """Include _argon2_cffi_bindings package required by _cffi_backend module.

    This package is distributed with argon2-cffi package.
    """
    _include_cffi_backend(finder, module)


def load_babel(finder: ModuleFinder, module: Module) -> None:
    """Load babel as a package, because it has pickeable data."""
    finder.include_package("babel")
    module.in_file_system = 1


def load_bcrypt(finder: ModuleFinder, module: Module) -> None:
    """Include required _cffi_backend module (bcrypt < 4.0 only)."""
    _include_cffi_backend(finder, module)


def load_boto(finder: ModuleFinder, module: Module) -> None:
    """Include the 'six' fake modules used by boto package."""
    finder.exclude_module("boto.vendored.six.moves")


def load_boto3(finder: ModuleFinder, module: Module) -> None:
    """Include subpackages of boto3 package and data."""
    finder.include_package("boto3.dynamodb")
    finder.include_package("boto3.ec2")
    finder.include_package("boto3.s3")
    dist = module.distribution
    if dist:
        finder.include_files(dist.locate_file("boto3/data"), "lib/boto3/data")


def load_ceODBC(finder: ModuleFinder, module: Module) -> None:
    """Implicitly imports datetime and decimal required by ceODBC module."""
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_certifi(finder: ModuleFinder, module: Module) -> None:
    """Include the certificate in zipfile if required.

    The certifi package uses importlib.resources to locate the cacert.pem.
    """
    if module.in_file_system == 0:
        cacert = Path(__import__("certifi").where())
        finder.zip_include_files(cacert, Path("certifi", cacert.name))


def load_cffi_cparser(finder: ModuleFinder, module: Module) -> None:
    """Include an optional extension for cffi.cparser module."""
    try:
        finder.include_module("cffi._pycparser")
    except ImportError:
        module.ignore_names.add("cffi._pycparser")


def load_collections(finder: ModuleFinder, module: Module) -> None:
    """Set the alias for collections.abc."""
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
    """Include required _cffi_backend module (google.crc32c)."""
    _include_cffi_backend(finder, module)


def load_cryptography(finder: ModuleFinder, module: Module) -> None:
    """Include required _cffi_backend module (cryptography)."""
    _include_cffi_backend(finder, module)


def load_ctypes_util(finder: ModuleFinder, module: Module) -> None:
    """Filter import names in ctypes.util module."""
    if not IS_MACOS:
        finder.exclude_module("ctypes.macholib")
        module.ignore_names.add("ctypes.macholib.dyld")
    if sys.platform != "aix":
        module.exclude_names.add("ctypes._aix")


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """Include an additional dependency required by _ctypes module."""
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
    """Implicitly imports datetime and decimal required by cx_Oracle module."""
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
    finder.include_module("_strptime")


def load_decimal(finder: ModuleFinder, module: Module) -> None:
    """Optimize decimal module."""
    try:
        finder.include_module("_decimal")
        module.exclude_names.add("_pydecimal")
    except ImportError:
        finder.include_module("_pydecimal")
        module.ignore_names.add("_decimal")


def load_discord(finder: ModuleFinder, module: Module) -> None:
    """Add required metadata of py-cord."""
    module.update_distribution("py-cord")


def load_flask_compress(finder: ModuleFinder, module: Module) -> None:
    """Add required metadata of flask-compress."""
    module.update_distribution("Flask_Compress")


def load_gevent(finder: ModuleFinder, module: Module) -> None:
    """Load gevent as a package."""
    finder.include_package("gevent")


def load_GifImagePlugin(finder: ModuleFinder, module: Module) -> None:
    """Ignore optional imports of GifImagePlugin module."""
    module.ignore_names.add("_imaging_gif")


def load_googleapiclient(finder: ModuleFinder, module: Module) -> None:
    """Add required metadata of googleapiclient."""
    module.update_distribution("google_api_python_client")


def load_googleapiclient_discovery(
    finder: ModuleFinder, module: Module
) -> None:
    """Include required subpackage of googleapiclient.discovery module.

    The discovery_cache module should be in the file system.
    """
    discovery_cache = finder.include_package("googleapiclient.discovery_cache")
    if discovery_cache:
        discovery_cache.in_file_system = 1


def load_google_cloud_storage(finder: ModuleFinder, module: Module) -> None:
    """Include the parent module of google.cloud.storage package.

    It always uses the parent module.
    """
    finder.include_package("google.cloud")


def load_gtk__gtk(finder: ModuleFinder, module: Module) -> None:
    """Include a number of implicit imports of gtk._gtk module."""
    finder.include_module("atk")
    finder.include_module("cairo")
    finder.include_module("gio")
    finder.include_module("pango")
    finder.include_module("pangocairo")


def load_h5py(finder: ModuleFinder, module: Module) -> None:
    """Include a number of implicit imports of h5py module."""
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
    """Include module required by h5py_wrapper."""
    finder.include_module("future")
    finder.include_module("ptr")


def load_hashlib(finder: ModuleFinder, module: Module) -> None:
    """Ignore optional imports of hashlib module.

    The hashlib's fallback modules don't exist if the equivalent OpenSSL
    algorithms are loaded from _hashlib, so we can ignore the error.
    """
    module.ignore_names.update(["_md5", "_sha", "_sha256", "_sha512"])


def load_hdfdict(finder: ModuleFinder, module: Module) -> None:
    """Include required module of hdfdict module."""
    finder.include_module("h5py_wrapper")
    finder.include_package("yaml")


def load_idna(finder: ModuleFinder, module: Module) -> None:
    """Include data of idna."""
    finder.include_module("idna.idnadata")


def load_imagej(finder: ModuleFinder, module: Module) -> None:
    """Add metadata of pyimagej package."""
    module.update_distribution("pyimagej")


def load_jpype(finder: ModuleFinder, module: Module) -> None:
    """Add required binary of JPype1 package."""
    dist = module.distribution
    if dist:
        source = dist.locate_file("org.jpype.jar")
        if source.exists():
            finder.include_files(
                source, f"lib/{source.name}", copy_dependent_files=False
            )


def load_librosa(finder: ModuleFinder, module: Module) -> None:
    """Load librosa as package."""
    finder.include_package("librosa")


def load_llvmlite(finder: ModuleFinder, module: Module) -> None:
    """Load llvmlite as package."""
    finder.include_package("llvmlite")
    finder.exclude_module("llvmlite.tests")


def load_lxml(finder: ModuleFinder, module: Module) -> None:
    """Include and extension required by lxml package."""
    finder.include_module("lxml._elementpath")


def load_markdown(finder: ModuleFinder, module: Module) -> None:
    """Include module implicitly loaded by markdown package."""
    finder.include_module("html.parser")


def load_Numeric(finder: ModuleFinder, module: Module) -> None:
    """Ignore optional module loaded by Numeric module."""
    module.ignore_names.add("dotblas")


def load_orjson(finder: ModuleFinder, module: Module) -> None:
    """Include dynamic imports of orjson."""
    finder.include_module("dataclasses")
    finder.include_module("datetime")
    finder.include_module("decimal")
    finder.include_module("enum")
    finder.include_package("json")
    finder.include_module("uuid")
    finder.include_package("zoneinfo")


def load_os(finder: ModuleFinder, module: Module) -> None:
    """Set the alias for os.path."""
    if "posix" in sys.builtin_module_names:
        finder.add_alias("os.path", "posixpath")
    else:
        finder.add_alias("os.path", "ntpath")


def load_pikepdf(finder: ModuleFinder, module: Module) -> None:
    """Load pikepdf as a package."""
    finder.include_package("pikepdf")


def load_platform(finder: ModuleFinder, module: Module) -> None:
    """Exclude a module if not used by platform module."""
    if not IS_MACOS:
        module.exclude_names.add("plistlib")


def load_plotly(finder: ModuleFinder, module: Module) -> None:
    """Load plotly as a package."""
    finder.include_package("plotly")


def load_postgresql_lib(finder: ModuleFinder, module: Module) -> None:
    """Include required data of postgresql.lib module."""
    path = module.path
    if path:
        libsys = path[0] / "libsys.sql"
        if libsys.exists():
            finder.include_files(libsys, libsys.name)


def load_pty(finder: ModuleFinder, module: Module) -> None:
    """Ignore optional imports of pty module."""
    module.ignore_names.add("sgi")


def load_ptr(finder: ModuleFinder, module: Module) -> None:
    """Add metadata of pytest-runner."""
    module.update_distribution("pytest-runner")


def load_pycountry(finder: ModuleFinder, module: Module) -> None:
    """Use pycountry module in the file system.

    It has data in subdirectories.
    """
    finder.exclude_module("pycountry.tests")
    module.in_file_system = 1


def load_pyodbc(finder: ModuleFinder, module: Module) -> None:
    """Include implicitly imports of pyodbc module."""
    for mod in ("datetime", "decimal", "hashlib", "locale", "uuid"):
        finder.include_module(mod)


def load_pyreadstat(finder: ModuleFinder, module: Module) -> None:
    """Load pyreadstat as a package."""
    finder.include_package("pyreadstat")
    finder.include_module("pandas")


def load_pyqtgraph(finder: ModuleFinder, module: Module) -> None:
    """Load pyqtgraph as a package."""
    finder.include_package("pyqtgraph")


def load_pytest(finder: ModuleFinder, module: Module) -> None:
    """Include implicitly imports of pytest module."""
    pytest = __import__("pytest")
    for mod in pytest.freeze_includes():
        finder.include_module(mod)


def load_pythoncom(finder: ModuleFinder, module: Module) -> None:
    """Copy required DLL.

    The pythoncom module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in
    the target directory.
    """
    pythoncom = __import__("pythoncom")
    filename = pythoncom.__file__
    if filename:
        file = Path(filename)
        finder.include_files(
            file, f"lib/{file.name}", copy_dependent_files=IS_MINGW
        )


def load_pywintypes(finder: ModuleFinder, module: Module) -> None:
    """Copy required DLL.

    The pywintypes module is actually contained in a DLL but since those
    cannot be loaded directly in Python 2.5 and higher a special module is
    used to perform that task; simply use that technique directly to
    determine the name of the DLL and ensure it is included as a file in the
    target directory.
    """
    pywintypes = __import__("pywintypes")
    filename = pywintypes.__file__
    if filename:
        file = Path(filename)
        finder.include_files(
            file, f"lib/{file.name}", copy_dependent_files=IS_MINGW
        )


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """Include import of reportlab module, loaded via exec."""
    finder.include_module("reportlab.rl_settings")


def load_sentry_sdk(finder: ModuleFinder, module: Module) -> None:
    """Include implicitly imports of Sentry.io SDK."""
    finder.include_module("sentry_sdk.integrations.stdlib")
    finder.include_module("sentry_sdk.integrations.excepthook")
    finder.include_module("sentry_sdk.integrations.dedupe")
    finder.include_module("sentry_sdk.integrations.atexit")
    finder.include_module("sentry_sdk.integrations.modules")
    finder.include_module("sentry_sdk.integrations.argv")
    finder.include_module("sentry_sdk.integrations.logging")
    finder.include_module("sentry_sdk.integrations.threading")


def load__socket(finder: ModuleFinder, module: Module) -> None:
    """Include encodings.idna used by _sockets module."""
    finder.include_module("encodings.idna")


def load_sqlite3(finder: ModuleFinder, module: Module) -> None:
    """Include required DLL, in Windows, by sqlite3 module."""
    if IS_WINDOWS:
        parts = ["DLLs", "Library/bin"]
        for part in parts:
            source = Path(sys.base_prefix, part, "sqlite3.dll")
            if source.exists():
                target = f"lib/{source.name}"
                finder.lib_files[source] = target
                finder.include_files(source, target)
    finder.include_module("sqlite3.dump")
    module.global_names.update(SQLITE3_GLOBAL_NAMES)


def load_sysconfig(finder: ModuleFinder, module: Module) -> None:
    """Include _sysconfigdata implicitly loaded by sysconfig module."""
    if IS_WINDOWS:
        return
    get_data_name = getattr(sysconfig, "_get_sysconfigdata_name", None)
    if get_data_name is None:
        return
    with suppress(ImportError):
        finder.include_module(get_data_name())


def load_time(finder: ModuleFinder, module: Module) -> None:
    """Include a module implicitly imported by time."""
    finder.include_module("_strptime")


def load_typing(finder: ModuleFinder, module: Module) -> None:
    """Optimize typing module."""
    finder.add_alias("typing.io", "io")
    finder.add_alias("typing.re", "re")


def load_twitter(finder: ModuleFinder, module: Module) -> None:
    """Ignore optional modules.

    The twitter module tries to load the simplejson, json and django.utils
    module in an attempt to locate any module that will implement the
    necessary protocol; ignore these modules if they cannot be found.
    """
    module.ignore_names.update(["json", "simplejson", "django.utils"])


def load_uvloop(finder: ModuleFinder, module: Module) -> None:
    """Include an internal extension module of uvloop."""
    finder.include_module("uvloop._noop")


def load_win32api(finder: ModuleFinder, module: Module) -> None:
    """Include a module implicitly imported by win32api."""
    if module.file:
        finder.exclude_dependent_files(module.file)
    finder.include_module("pywintypes")


def load_win32com(finder: ModuleFinder, module: Module) -> None:
    """Manipulate the search path at runtime to include win32comext."""
    if module.file and module.path:
        module.path.append(module.file.parent.parent / "win32comext")


def load_win32file(finder: ModuleFinder, module: Module) -> None:
    """Include modules implicitly imported by win32file."""
    finder.include_module("pywintypes")
    finder.include_module("win32timezone")


def load_win32print(finder: ModuleFinder, module: Module) -> None:
    """Include a module implicitly imported by win32print."""
    finder.include_module("pywintypes")


def load_xml_etree_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """Include a module implicitly imported by xml.etree.cElementTree."""
    finder.include_module("xml.etree.ElementTree")


def load_yaml(finder: ModuleFinder, module: Module) -> None:
    """Add metadata of PyYAML."""
    module.update_distribution("PyYAML")


def load_zipfile(finder: ModuleFinder, module: Module) -> None:
    """Include encodings required by zipfile module."""
    finder.include_module("encodings.ascii")
    finder.include_module("encodings.cp437")


def load_zlib(finder: ModuleFinder, module: Module) -> None:
    """Include required DLL, in Windows, by zlib module.

    Using conda-forge, the required DLL is zlib.dll, however, using the
    official Python 3.12+, the requiref DLL is zlib1.dll.
    """
    if not IS_WINDOWS:
        return
    if IS_CONDA:
        source = Path(sys.base_prefix, "Library/bin/zlib.dll")
        if source.exists():
            target = source.name
            finder.lib_files[source] = target
    else:
        # ensure zlib1.dll is copied in Python 3.12+
        # (when Lief is installed, the DLL is detected)
        for source in Path(sys.base_prefix, "DLLs").glob("zlib*.dll"):
            target = f"lib/{source.name}"
            finder.lib_files[source] = target
            finder.include_files(source, target)


#
# missing section
#


def missing_gdk(finder: ModuleFinder, caller: Module) -> None:
    """Ignore module gdk, that is buried inside gtk."""
    caller.ignore_names.add("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """Ignore module ltihooks, if it is not found."""
    caller.ignore_names.add("ltihooks")


def missing_six_moves(finder: ModuleFinder, caller: Module) -> None:
    """Ignore the fake module that six module creates."""
    caller.ignore_names.add("six.moves")


def missing_typing_extensions(finder: ModuleFinder, caller: Module) -> None:
    """Ignore typing_extensions module when it cannot be found.

    Is not required at runtime, so ignore it.
    """
    caller.ignore_names.add("typing_extensions")
