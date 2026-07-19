"""Set of unused modules, named default excludes and default ignore names.

On various platforms and python versions.
"""

from __future__ import annotations

import collections.abc
import os
import sys

__all__ = ("DEFAULT_EXCLUDES", "DEFAULT_IGNORE_NAMES")

# EXCLUDES - modules that exists in the current supported Python version or
# platforms and shouldn't included in the frozen executable.
DEFAULT_EXCLUDES: set[str] = {
    "ensurepip",
    "idlelib",
    "pip",
    "pydoc",
    "pydoc_data",
    "sitecustomize",
    "test",
    "test.support",
    "this",
    "unittest",
    "usercustomize",
    "venv",
    "zipapp",
}

# Excludes modules for platforms other than the current one.
if sys.platform != "aix":
    DEFAULT_EXCLUDES.add("_aix_support")
if sys.platform != "android":
    DEFAULT_EXCLUDES.add("_android_support")
if sys.platform != "darwin":
    DEFAULT_EXCLUDES |= {
        "_apple_support",
        "_scproxy",
        "_osx_support",
    }
if sys.platform != "ios":
    DEFAULT_EXCLUDES.add("_ios_support")
if os.name != "nt":
    DEFAULT_EXCLUDES |= {
        "nturl2path",
    }
if "__pypy__" not in sys.builtin_module_names:
    DEFAULT_EXCLUDES.add("__pypy__")

# IGNORE - optional modules that may be referenced but no longer exist
# (legacy code) or were not installed, and will not cause problems.
DEFAULT_IGNORE_NAMES: set[str] = {
    # Ignore py2 modules that have been removed or renamed in py3.
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
    # OpenVMS
    "vms_lib",
}
# Ignore old names of collections modules.
DEFAULT_IGNORE_NAMES |= {
    f"collections.{name}" for name in collections.abc.__all__
}

# Ignores modules for platforms other than the current one.
if sys.platform != "darwin":
    DEFAULT_IGNORE_NAMES |= {
        "appscript",
        "appscript.reference",
        "mac",
        "macurl2path",
    }
if os.name != "nt":
    DEFAULT_IGNORE_NAMES |= {
        "msilib",
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
    }

# Ignore modules removed in python versions > 3.0.
PY_VERSION = sys.version_info[:2]

if PY_VERSION >= (3, 10):
    DEFAULT_IGNORE_NAMES |= {
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
    }
if PY_VERSION >= (3, 11):
    DEFAULT_IGNORE_NAMES.add("binhex")
if PY_VERSION >= (3, 12):
    DEFAULT_IGNORE_NAMES |= {
        "asynchat",  # available as pyasynchat
        "asyncore",  # available as pyasyncore
        "distutils",  # available w/ setuptools
        "imp",
        "smtpd",
    }
if PY_VERSION >= (3, 13):
    DEFAULT_IGNORE_NAMES |= {
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
        "msilib",  # available as python-msilib
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
    }

DEFAULT_IGNORE_NAMES |= {
    "__main__",
    "_manylinux",  # flag
    "_typeshed",
    "_typeshed.dbapi",
    "_typeshed.importlib",
    "_typeshed.wsgi",
    "_typeshed.xml",
    "typeshed",
}

# Ignore modules for platforms other than the current one.
if sys.platform != "android":
    DEFAULT_IGNORE_NAMES |= {
        "android",
        "jnius",
    }
if os.name != "java":
    DEFAULT_IGNORE_NAMES |= {
        "java.lang",
        "jnius",
        "org.python.core",
    }
if os.name != "nt":
    DEFAULT_IGNORE_NAMES |= {
        "msvcrt",
        "_overlapped",
        "_winapi",
        "winreg",
        "_wmi",
    }
else:
    DEFAULT_IGNORE_NAMES |= {
        "fcntl",
        "grp",
        "_posixshmem",
        "_posixsubprocess",
        "pwd",
        "readline",
        "termios",
    }
if "posix" in sys.builtin_module_names:
    DEFAULT_IGNORE_NAMES.add("nt")  # only windows, not mingw
else:
    DEFAULT_IGNORE_NAMES.add("posix")

# Ignore backports.
DEFAULT_IGNORE_NAMES |= {
    "backports",
    "backports.zoneinfo",
    "importlib_metadata",
    "importlib_resources",
}
if PY_VERSION >= (3, 11):
    DEFAULT_IGNORE_NAMES.add("exceptiongroup")
if PY_VERSION >= (3, 12):
    DEFAULT_IGNORE_NAMES.add("backports.tarfile")
if PY_VERSION >= (3, 14):
    DEFAULT_IGNORE_NAMES.add("backports.zstd")

# Ignore new libraries in Python 3.10+.
if PY_VERSION < (3, 11):
    DEFAULT_IGNORE_NAMES |= {
        "tomllib",
        "wsgiref.types",
    }
if PY_VERSION < (3, 14):
    DEFAULT_IGNORE_NAMES |= {
        "annotationlib",
        "concurrent.interpreters",
        "compression",
        "string.templatelib",
    }

# Ignore all default excludes.
DEFAULT_IGNORE_NAMES.update(DEFAULT_EXCLUDES)
