"""A collection of functions which are triggered automatically by finder when
certain packages are included or not found.
"""
# pylint: disable=invalid-name
# ruff: noqa: ARG001

from __future__ import annotations

import os
import sys
import sysconfig
from contextlib import suppress
from pathlib import Path

from .._compat import IS_MINGW, IS_WINDOWS
from ..finder import ModuleFinder
from ..module import Module
from ._qthooks import get_qt_plugins_paths  # noqa: F401


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
    """The bcrypt < 4.0 package requires the _cffi_backend module
    (loaded implicitly).
    """
    include_cffi = True
    if (
        module.distribution
        and int(module.distribution.version.split(".")[0]) >= 4
    ):
        include_cffi = False
    if include_cffi:
        finder.include_module("_cffi_backend")


def load_boto(finder: ModuleFinder, module: Module) -> None:
    """The boto package uses 'six' fake modules."""
    finder.exclude_module("boto.vendored.six.moves")


def load_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """The cElementTree module implicitly loads the elementtree.ElementTree
    module; make sure this happens.
    """
    finder.include_module("elementtree.ElementTree")


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
        cffi = __import__("cffi", fromlist=["_pycparser"])
        pycparser = getattr(cffi, "_pycparser")  # noqa: B009
        finder.include_module(pycparser.__name__)
    except (ImportError, AttributeError):
        finder.exclude_module("cffi._pycparser")


def load_charset_normalizer(finder: ModuleFinder, module: Module) -> None:
    """The charset_normalizer package."""
    finder.exclude_module("charset_normalizer.cli")


def load_charset_normalizer_md(finder: ModuleFinder, module: Module) -> None:
    """The charset_normalizer package implicitly imports a extension module."""
    mypyc = module.file.parent / ("md__mypyc" + "".join(module.file.suffixes))
    if mypyc.exists():
        finder.include_module("charset_normalizer.md__mypyc")


def load_crc32c(finder: ModuleFinder, module: Module) -> None:
    """The google.crc32c module requires _cffi_backend module."""
    finder.include_module("_cffi_backend")


def load_cryptography(finder: ModuleFinder, module: Module) -> None:
    """The cryptography module requires the _cffi_backend module."""
    if module.distribution and module.distribution.requires:
        include_cffi = False
        for req in module.distribution.requires:
            if req.startswith("cffi"):
                include_cffi = True
                break
    else:
        include_cffi = True
    if include_cffi:
        finder.include_module("_cffi_backend")


def load__ctypes(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the _ctypes module in Python 3.8+ requires an additional
    libffi dll to be present in the build directory.
    """
    if IS_WINDOWS and sys.version_info >= (3, 8):
        dll_pattern = "libffi-*.dll"
        dll_dir = Path(sys.base_prefix, "DLLs")
        for dll_path in dll_dir.glob(dll_pattern):
            finder.include_files(dll_path, Path("lib", dll_path.name))


def load_cx_Oracle(finder: ModuleFinder, module: Module) -> None:
    """The cx_Oracle module implicitly imports datetime; make sure this
    happens.
    """
    finder.include_module("datetime")
    finder.include_module("decimal")


def load_datetime(finder: ModuleFinder, module: Module) -> None:
    """The datetime module implicitly imports time; make sure this happens."""
    finder.include_module("time")


def load_docutils_frontend(finder: ModuleFinder, module: Module) -> None:
    """The optik module is the old name for the optparse module; ignore the
    module if it cannot be found.
    """
    module.ignore_names.add("optik")


def load_dummy_threading(finder: ModuleFinder, module: Module) -> None:
    """The dummy_threading module plays games with the name of the threading
    module for its own purposes; ignore that here.
    """
    finder.exclude_module("_dummy_threading")


def load_flask_compress(finder: ModuleFinder, module: Module) -> None:
    """flask-compress requires its metadata."""
    module.update_distribution("Flask_Compress")


def load_ftplib(finder: ModuleFinder, module: Module) -> None:
    """The ftplib module attempts to import the SOCKS module; ignore this
    module if it cannot be found.
    """
    module.ignore_names.add("SOCKS")


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


def load_lazy_loader(finder: ModuleFinder, module: Module) -> None:
    """Use load_lazy_loader 0.2+ to work with .pyc files."""
    if module.distribution.version < "0.2":
        raise SystemExit(
            "Please upgrade 'lazy_loader>=0.2' to support cx_Freeze"
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
    dynamically loaded modules in subpackages is growing.
    """
    finder.include_package("pkg_resources")


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
        filename, Path("lib", filename.name), copy_dependent_files=False
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
        filename, Path("lib", filename.name), copy_dependent_files=False
    )


def load_reportlab(finder: ModuleFinder, module: Module) -> None:
    """The reportlab module loads a submodule rl_settings via exec so force
    its inclusion here.
    """
    finder.include_module("reportlab.rl_settings")


def load_shapely(finder: ModuleFinder, module: Module) -> None:
    """The Shapely.libs directory is not copied."""
    libs_name = "Shapely.libs"
    source_dir = module.path[0].parent / libs_name
    if source_dir.exists():
        finder.include_files(source_dir, f"lib/{libs_name}")


def load_sentry(finder: ModuleFinder, module: Module) -> None:
    """The Sentry.io SDK."""
    finder.include_module("sentry_sdk.integrations.stdlib")
    finder.include_module("sentry_sdk.integrations.excepthook")
    finder.include_module("sentry_sdk.integrations.dedupe")
    finder.include_module("sentry_sdk.integrations.atexit")
    finder.include_module("sentry_sdk.integrations.modules")
    finder.include_module("sentry_sdk.integrations.argv")
    finder.include_module("sentry_sdk.integrations.logging")
    finder.include_module("sentry_sdk.integrations.threading")


def load_sklearn__distributor_init(
    finder: ModuleFinder, module: Module
) -> None:
    """On Windows the sklearn/.libs directory is not copied."""
    source_dir = module.parent.path[0] / ".libs"
    if source_dir.exists():
        # msvcp140 and vcomp140 dlls should be copied
        finder.include_files(source_dir, "lib")
        # patch the code to search the correct directory
        code_string = module.file.read_text(encoding="utf-8")
        code_string = code_string.replace(
            "libs_path =", "libs_path = __import__('sys').frozen_dir  #"
        )
        module.code = compile(code_string, os.fspath(module.file), "exec")


def load_setuptools(finder: ModuleFinder, module: Module) -> None:
    """The setuptools must be loaded as a package, to prevent it to break in
    the future.
    """
    finder.include_package("setuptools")


def load_setuptools_extension(finder: ModuleFinder, module: Module) -> None:
    """The setuptools.extension module optionally loads
    Pyrex.Distutils.build_ext but its absence is not considered an error.
    """
    module.ignore_names.add("Pyrex.Distutils.build_ext")


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
        dll_name = "sqlite3.dll"
        dll_path = Path(sys.base_prefix, "DLLs", dll_name)
        if not dll_path.exists():
            dll_path = Path(sys.base_prefix, "Library", "bin", dll_name)
        if dll_path.exists():
            finder.include_files(dll_path, Path("lib", dll_name))
    finder.include_package("sqlite3")


def load_six(finder: ModuleFinder, module: Module) -> None:
    """The six module creates fake modules."""
    finder.exclude_module("six.moves")


def load_ssl(finder: ModuleFinder, module: Module) -> None:
    """In Windows, the SSL module requires additional dlls to be present in the
    build directory.
    """
    if IS_WINDOWS:
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


def load_tokenizers(finder: ModuleFinder, module: Module) -> None:
    """On Linux the tokenizers.libs directory is not copied."""
    if module.path is None:
        return
    libs_name = "tokenizers.libs"
    source_dir = module.path[0].parent / libs_name
    if source_dir.exists():
        finder.include_files(source_dir, Path("lib", libs_name))


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


def load_wx_lib_pubsub_core(finder: ModuleFinder, module: Module) -> None:
    """The wx.lib.pubsub.core module modifies the search path which cannot
    be done in a frozen application in the same way; modify the module
    search path here instead so that the right modules are found; note
    that this only works if the import of wx.lib.pubsub.setupkwargs
    occurs first.
    """
    module.path.insert(0, module.file.parent / "kwargs")


def load_xml_etree_cElementTree(finder: ModuleFinder, module: Module) -> None:
    """The xml.etree.cElementTree module implicitly loads the
    xml.etree.ElementTree module; make sure this happens.
    """
    finder.include_module("xml.etree.ElementTree")


def load_yaml(finder: ModuleFinder, module: Module) -> None:
    """PyYAML requires its metadata."""
    module.update_distribution("PyYAML")


def load_zmq(finder: ModuleFinder, module: Module) -> None:
    """The zmq package loads zmq.backend.cython dynamically and links
    dynamically to zmq.libzmq or shared lib. Tested in pyzmq 16.0.4 (py36),
    19.0.2 (MSYS2 py39) up to 22.2.1 (from pip and from conda).
    """
    finder.include_package("zmq.backend.cython")
    if IS_WINDOWS or IS_MINGW:
        # For pyzmq 22 the libzmq dependencies are located in
        # site-packages/pyzmq.libs
        libzmq_folder = "pyzmq.libs"
        libs_dir = module.path[0].parent / libzmq_folder
        if libs_dir.exists():
            finder.include_files(libs_dir, Path("lib", libzmq_folder))
    # Include the bundled libzmq library, if it exists
    with suppress(ImportError):
        finder.include_module("zmq.libzmq")
    finder.exclude_module("zmq.tests")


def load_zoneinfo(finder: ModuleFinder, module: Module) -> None:
    """The zoneinfo package requires timezone data, that
    can be the in tzdata package, if installed.
    """
    tzdata: Module | None = None
    source: Path | None = None
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
        if source and source.is_dir():
            # without tzdata, copy only zoneinfo directory
            # in Linux: /usr/share/zoneinfo
            target = Path("lib", "tzdata", "zoneinfo")
            finder.include_files(source, target, copy_dependent_files=False)
            finder.add_constant("PYTHONTZPATH", os.fspath(source))
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
    module but it uses a dynamic, not static import to do its work.
    """
    finder.include_module("pkg_resources")


def missing_gdk(finder: ModuleFinder, caller: Module) -> None:
    """The gdk module is buried inside gtk so there is no need to concern
    ourselves with an error saying that it cannot be found.
    """
    caller.ignore_names.add("gdk")


def missing_ltihooks(finder: ModuleFinder, caller: Module) -> None:
    """The ltihooks module is not necessairly present so ignore it when it
    cannot be found.
    """
    caller.ignore_names.add("ltihooks")


def missing_readline(finder: ModuleFinder, caller: Module) -> None:
    """The readline module is not normally present on Windows but it also may
    be so instead of excluding it completely, ignore it if it can't be found.
    """
    if IS_WINDOWS:
        caller.ignore_names.add("readline")
