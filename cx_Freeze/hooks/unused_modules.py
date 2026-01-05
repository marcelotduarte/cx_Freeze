"""Set of unused modules, named default excludes and default ignore names,
on various platforms and python versions.
"""

from __future__ import annotations

import collections.abc
import os
import sys

__all__ = ("DEFAULT_EXCLUDES", "DEFAULT_IGNORE_NAMES")

DEFAULT_EXCLUDES: set[str] = {
    # py2 modules that have been removed or renamed in py3
    "__builtin__",
    "audiodev",
    "anydbm",
    "BaseHTTPServer",
    "Bastion",
    "bsddb",
    "bsddb3",
    "CGIHTTPServer",
    "commands",
    "ConfigParser",
    "Cookie",
    "cookielib",
    "copy_reg",
    "cPickle",
    "cStringIO",
    "dbhash",
    "dircache",
    "dumbdbm",
    "dummy_thread",
    "email.Charset",
    "email.Encoders",
    "email.Errors",
    "email.FeedParser",
    "email.Generator",
    "email.Header",
    "email.Iterators",
    "email.Message",
    "email.Parser",
    "email.Utils",
    "email.base64MIME",
    "email.quopriMIME",
    "FCNTL",
    "fl",
    "fm",
    "fpformat",
    "gl",
    "gdbm",
    "htmlentitydefs",
    "htmllib",
    "HTMLParser",
    "httplib",
    "hotshot",
    "ihooks",
    "imputil",
    "linuxaudiodev",
    "markupbase",
    "md5",
    "mimetools",
    "MimeWriter",
    "mimify",
    "multifile",
    "Nav",
    "new",
    "mutex",
    "Pickle",
    "posixfile",
    "Queue",
    "rexec",
    "repr",
    "rfc822",
    "robotparser",
    "sets",
    "sgmllib",
    "sha",
    "SimpleHTTPServer",
    "SocketServer",
    "SOCKS",
    "statvfs",
    "StringIO",
    "sunaudiodev",
    "timing",
    "thread",
    "Tkinter",
    "toaiff",
    "urllib.quote",
    "urllib.quote_plus",
    "urllib.unquote",
    "urllib.unquote_plus",
    "urllib.urlencode",
    "urllib.urlopen",
    "urllib.urlretrieve",
    "urllib2",
    "urlparse",
    "user",
    "UserDict",
    "UserList",
    "UserString",
    "whichdb",
    "_winreg",  # named to winreg
    # macos specific removed in py3
    # https://docs.python.org/2.7/library/mac.html?highlight=removed
    "autoGIL",
    "Carbon",
    "ColorPicker",
    "EasyDialogs",
    "findertools",
    "FrameWork",
    "ic",
    "MacOS",
    "macostools",
    # macpython removed
    "aetypes",
    "aepack",
    "aetools",
    "applesingle",
    "buildtools",
    "cfmfile",
    "icopen",
    "macerros",
    "macresource",
    "PixMapWrapper",
    "videoreader",
    "W",
    # IRIX / sgi removed
    "al",
    "cd",
    "cddb",
    "cdplayer",
    "cl",
    "imgfile",
    "jpeg",
    "sv",
}
# old collections modules
DEFAULT_EXCLUDES.update(
    [f"collections.{name}" for name in collections.abc.__all__]
)
# exclusion by platform/os
if os.name != "nt":
    DEFAULT_EXCLUDES.update(
        [
            "msilib",
            "nturl2path",
            "pyHook",
            "pythoncom",
            "pywintypes",
            "winerror",
            "winsound",
            "win32api",
            "win32con",
            "win32com.client",
            "win32com.server",
            "win32com.server.dispatcher",
            "win32com.server.policy",
            "win32com.server.util",
            "win32com.shell",
            "win32gui",
            "win32event",
            "win32evtlog",
            "win32evtlogutil",
            "win32file",
            "win32pdh",
            "win32pipe",
            "win32process",
            "win32security",
            "win32service",
            "win32stat",
            "win32timezone",
            "win32wnet",
            "wx.activex",
        ]
    )

# removed by platform
if sys.platform != "aix":
    DEFAULT_EXCLUDES.add("_aix_support")
if sys.platform != "darwin":
    DEFAULT_EXCLUDES.update(
        [
            "appscript",
            "appscript.reference",
            "mac",
            "macurl2path",
            "_scproxy",
            "_osx_support",
        ]
    )
if os.name != "os2":
    DEFAULT_EXCLUDES.update(["os2", "os2emxpath", "_emx_link"])
if os.name != "ce":
    DEFAULT_EXCLUDES.add("ce")
if os.name != "riscos":
    DEFAULT_EXCLUDES.update(
        ["riscos", "riscosenviron", "riscospath", "rourl2path"]
    )
if "__pypy__" not in sys.builtin_module_names:
    DEFAULT_EXCLUDES.add("__pypy__")

# removed in python versions > 3.0
PY_VERSION = sys.version_info[:2]

if PY_VERSION >= (3, 10):
    DEFAULT_EXCLUDES.update(
        [
            # 3.3
            "cElementTree",
            # 3.8
            "macpath",
            # 3.9
            "_dummy_thread",
            "dummy_threading",
            "_dummy_threading",
            # 3.10
            "formatter",
            "parser",
        ]
    )
if PY_VERSION >= (3, 11):
    DEFAULT_EXCLUDES.add("binhex")
if PY_VERSION >= (3, 12):
    DEFAULT_EXCLUDES.update(
        [
            # "asynchat",  # available as pyasynchat
            # "asyncore",  # available as pyasyncore
            "distutils",
            "imp",
            "smtpd",
        ]
    )
if PY_VERSION >= (3, 13):
    DEFAULT_EXCLUDES.update(
        [
            "aifc",
            "audioop",
            "chunk",
            "cgi",
            "cgitb",
            "crypt",
            "_crypt",
            "imghdr",
            "lib2to3",
            "mailcap",
            # "msilib",  # available as python-msilib
            "nis",
            "nntplib",
            "ossaudiodev",
            "pipes",
            "sndhdr",
            "spwd",
            "sunau",
            "telnetlib",
            "uu",
            "xdrlib",
        ]
    )

# remove test modules
DEFAULT_EXCLUDES.update(["test", "test.support"])

# remove modules mapped to internal modules
DEFAULT_EXCLUDES.update(
    [
        "importlib._bootstrap",  # mapped-> _frozen_importlib
        "importlib._bootstrap_external",  # _frozen_importlib_external
    ]
)

DEFAULT_IGNORE_NAMES: set[str] = {
    "__main__",
    "_frozen_importlib",  # internal
    "_frozen_importlib_external",  # internal
    "_manylinux",  # flag
    "_typeshed",
    "_typeshed.dbapi",
    "_typeshed.importlib",
    "_typeshed.wsgi",
    "_typeshed.xml",
    "typeshed",
}

# ignored by platform / os
if not sys.platform.startswith("android"):
    DEFAULT_IGNORE_NAMES.update(["android", "jnius"])
if not sys.platform.startswith("java"):
    DEFAULT_IGNORE_NAMES.update(["java.lang", "jnius", "org.python.core"])
if not sys.platform.startswith("OpenVMS"):
    DEFAULT_IGNORE_NAMES.add("vms_lib")
if os.name != "nt":
    DEFAULT_IGNORE_NAMES.update(
        ["msvcrt", "_overlapped", "_winapi", "winreg", "_wmi"]
    )
else:
    DEFAULT_IGNORE_NAMES.update(
        [
            "fcntl",
            "grp",
            "_posixshmem",
            "_posixsubprocess",
            "pwd",
            "readline",
            "termios",
        ]
    )
if "posix" in sys.builtin_module_names:
    DEFAULT_IGNORE_NAMES.add("nt")  # only windows, not mingw
else:
    DEFAULT_IGNORE_NAMES.add("posix")

# ignore backports
DEFAULT_IGNORE_NAMES.update(
    ["backports.zoneinfo", "importlib_metadata", "importlib_resources"]
)
if PY_VERSION >= (3, 11):
    DEFAULT_IGNORE_NAMES.add("exceptiongroup")
if PY_VERSION >= (3, 12):
    DEFAULT_IGNORE_NAMES.add("backports.tarfile")
if PY_VERSION >= (3, 14):
    DEFAULT_IGNORE_NAMES.add("backports.zstd")

# ignore new libraries in Python 3.10+
if PY_VERSION < (3, 11):
    DEFAULT_IGNORE_NAMES.update(["tomllib", "wsgiref.types"])
if PY_VERSION < (3, 14):
    DEFAULT_IGNORE_NAMES.update(
        [
            "annotationlib",
            "concurrent.interpreters",
            "compression",
            "string.templatelib",
        ]
    )


# ignore all default excludes
DEFAULT_IGNORE_NAMES.update(DEFAULT_EXCLUDES)
