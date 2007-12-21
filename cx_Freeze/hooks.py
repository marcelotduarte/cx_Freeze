import os
import sys

def initialize(finder):
    """upon initialization of the finder, this routine is called to set up some
       automatic exclusions for various platforms."""
    finder.ExcludeModule("os.path")
    if os.name == "nt":
        finder.ExcludeModule("fcntl")
        finder.ExcludeModule("grp")
        finder.ExcludeModule("pwd")
        finder.ExcludeModule("termios")
    else:
        finder.ExcludeModule("_winreg")
        finder.ExcludeModule("msilib")
        finder.ExcludeModule("msvcrt")
        finder.ExcludeModule("nt")
        if os.name not in ("os2", "ce"):
            finder.ExcludeModule("ntpath")
        finder.ExcludeModule("nturl2path")
        finder.ExcludeModule("pythoncom")
        finder.ExcludeModule("pywintypes")
        finder.ExcludeModule("winerror")
        finder.ExcludeModule("winsound")
        finder.ExcludeModule("win32con")
        finder.ExcludeModule("win32service")
    if os.name != "posix":
        finder.ExcludeModule("posix")
    if os.name != "mac":
        finder.ExcludeModule("Carbon")
        finder.ExcludeModule("ic")
        finder.ExcludeModule("mac")
        finder.ExcludeModule("MacOS")
        finder.ExcludeModule("macpath")
        finder.ExcludeModule("macurl2path")
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
    if sys.platform[:4] != "java":
        finder.ExcludeModule("java.lang")
        finder.ExcludeModule("org.python.core")


def load_ceODBC(finder, module):
    """the ceODBC module implicitly imports both datetime and decimal; make
       sure this happens."""
    finder.IncludeModule("datetime")
    finder.IncludeModule("decimal")


def load_cx_Oracle(finder, module):
    """the cx_Oracle module implicitly imports datetime; make sure this
       happens."""
    finder.IncludeModule("datetime")


def load_docutils_frontend(finder, module):
    """The optik module is the old name for the optparse module; ignore the
       module if it cannot be found."""
    module.IgnoreName("optik")


def load_dummy_threading(finder, module):
    """the dummy_threading module plays games with the name of the threading
       module for its own purposes; ignore that here"""
    finder.ExcludeModule("_dummy_threading")


def load_email(finder, module):
    """the email package has a bunch of aliases as the submodule names were
       all changed to lowercase in Python 2.5; mimic that here."""
    if sys.version_info[:2] >= (2, 5):
        for name in ("Charset", "Encoders", "Errors", "FeedParser",
                "Generator", "Header", "Iterators", "Message", "Parser",
                "Utils", "base64MIME", "quopriMIME"):
            finder.AddAlias("email.%s" % name, "email.%s" % name.lower())


def load_ftplib(finder, module):
    """the ftplib module attempts to import the SOCKS module; ignore this
       module if it cannot be found"""
    module.IgnoreName("SOCKS")


def load_pythoncom(finder, module):
    """the pythoncom module is actually contained in a DLL but since those
       cannot be loaded directly in Python 2.5 and higher a special module is
       used to perform that task; simply use that technique directly to
       determine the name of the DLL and ensure it is included as a normal
       extension; also load the pywintypes module which is implicitly
       loaded."""
    import pythoncom
    module.file = pythoncom.__file__
    module.code = None
    finder.IncludeModule("pywintypes")


def load_pywintypes(finder, module):
    """the pywintypes module is actually contained in a DLL but since those
       cannot be loaded directly in Python 2.5 and higher a special module is
       used to perform that task; simply use that technique directly to
       determine the name of the DLL and ensure it is included as a normal
       extension."""
    import pywintypes
    module.file = pywintypes.__file__
    module.code = None


def load_PyQt4_Qt(finder, module):
    """the PyQt4.Qt module is an extension module which imports a number of
       other modules and injects their namespace into its own. It seems a
       foolish way of doing things but perhaps there is some hidden advantage
       to this technique over pure Python."""
    finder.IncludeModule("PyQt4._qt")
    finder.IncludeModule("PyQt4.QtCore")
    finder.IncludeModule("PyQt4.QtGui")
    finder.IncludeModule("PyQt4.QtSvg")
    finder.IncludeModule("PyQt4.Qsci")
    finder.IncludeModule("PyQt4.QtAssistant")
    finder.IncludeModule("PyQt4.QtNetwork")
    finder.IncludeModule("PyQt4.QtOpenGL")
    finder.IncludeModule("PyQt4.QtScript")
    finder.IncludeModule("PyQt4.QtSql")
    finder.IncludeModule("PyQt4.QtSvg")
    finder.IncludeModule("PyQt4.QtTest")
    finder.IncludeModule("PyQt4.QtXml")
    finder.IncludeModule("sip")


def load_tempfile(finder, module):
    """the tempfile module attempts to load the fcntl and thread modules but
       continues if these modules cannot be found; ignore these modules if they
       cannot be found."""
    module.IgnoreName("fcntl")
    module.IgnoreName("thread")


def load_time(finder, module):
    """the time module implicitly loads _strptime; make sure this happens."""
    finder.IncludeModule("_strptime")


def load_win32api(finder, module):
    """the win32api module implicitly loads the pywintypes module; make sure
       this happens."""
    finder.IncludeModule("pywintypes")


def load_win32com(finder, module):
    """the win32com package manipulates its search path at runtime to include
       the sibling directory called win32comext; simulate that by changing the
       search path in a similar fashion here."""
    baseDir = os.path.dirname(os.path.dirname(module.file))
    module.path.append(os.path.join(baseDir, "win32comext"))


def load_xml(finder, module):
    """the builtin xml package attempts to load the _xmlplus module to see if
       that module should take its role instead; ignore the failure to find
       this module, though."""
    module.IgnoreName("_xmlplus")


def missing_EasyDialogs(finder, caller):
    """the EasyDialogs module is not normally present on Windows but it also
       may be so instead of excluding it completely, ignore it if it can't be
       found"""
    if sys.platform == "win32":
        caller.IgnoreName("EasyDialogs")


def missing_readline(finder, caller):
    """the readline module is not normally present on Windows but it also may
       be so instead of excluding it completely, ignore it if it can't be
       found"""
    if sys.platform == "win32":
        caller.IgnoreName("readline")

