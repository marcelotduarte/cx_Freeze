import os
import sys

def initialize(finder):
    """upon initialization of the finder, this routine is called to set up some
       automatic exclusions for various platforms."""
    finder.ExcludeModule("FCNTL")
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
        finder.ExcludeModule("win32api")
        finder.ExcludeModule("win32con")
        finder.ExcludeModule("win32event")
        finder.ExcludeModule("win32file")
        finder.ExcludeModule("win32pdh")
        finder.ExcludeModule("win32pipe")
        finder.ExcludeModule("win32process")
        finder.ExcludeModule("win32security")
        finder.ExcludeModule("win32service")
        finder.ExcludeModule("wx.activex")
    if os.name != "posix":
        finder.ExcludeModule("posix")
    if os.name != "mac":
        finder.ExcludeModule("Carbon")
        finder.ExcludeModule("gestalt")
        finder.ExcludeModule("ic")
        finder.ExcludeModule("mac")
        finder.ExcludeModule("MacOS")
        finder.ExcludeModule("macpath")
        finder.ExcludeModule("macurl2path")
        if os.name != "nt":
            finder.ExcludeModule("EasyDialogs")
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


def load_cElementTree(finder, module):
    """the cElementTree module implicitly loads the elementtree.ElementTree
       module; make sure this happens."""
    finder.IncludeModule("elementtree.ElementTree")


def load_ceODBC(finder, module):
    """the ceODBC module implicitly imports both datetime and decimal; make
       sure this happens."""
    finder.IncludeModule("datetime")
    finder.IncludeModule("decimal")


def load_cx_Oracle(finder, module):
    """the cx_Oracle module implicitly imports datetime; make sure this
       happens."""
    finder.IncludeModule("datetime")
    try:
        finder.IncludeModule("decimal")
    except ImportError:
        pass


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


def load_glib(finder, module):
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


def load_gtk__gtk(finder, module):
    """the gtk._gtk module has a number of implicit imports"""
    finder.IncludeModule("atk")
    finder.IncludeModule("cairo")
    finder.IncludeModule("gio")
    finder.IncludeModule("pango")
    finder.IncludeModule("pangocairo")


def load_matplotlib(finder, module):
    """the matplotlib module requires data to be found in mpl-data in the
       same directory as the frozen executable so oblige it"""
    dir = os.path.join(module.path[0], "mpl-data")
    finder.IncludeFiles(dir, "mpl-data")


def load_matplotlib_numerix(finder, module):
    """the numpy.numerix module loads a number of modules dynamically"""
    for name in ("ma", "fft", "linear_algebra", "random_array", "mlab"):
        finder.IncludeModule("%s.%s" % (module.name, name))


def load_numpy_linalg(finder, module):
    """the numpy.linalg module implicitly loads the lapack_lite module; make
       sure this happens"""
    finder.IncludeModule("numpy.linalg.lapack_lite")


def load_pty(finder, module):
    """The sgi module is not needed for this module to function."""
    module.IgnoreName("sgi")


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


def load_PyQt4_QtCore(finder, module):
    """the PyQt4.QtCore module implicitly imports the sip module."""
    finder.IncludeModule("sip")


def load_PyQt4_Qt(finder, module):
    """the PyQt4.Qt module is an extension module which imports a number of
       other modules and injects their namespace into its own. It seems a
       foolish way of doing things but perhaps there is some hidden advantage
       to this technique over pure Python; ignore the absence of some of
       the modules since not every installation includes all of them."""
    finder.IncludeModule("PyQt4.QtCore")
    finder.IncludeModule("PyQt4.QtGui")
    for name in ("PyQt4._qt", "PyQt4.QtSvg", "PyQt4.Qsci", "PyQt4.QtAssistant",
            "PyQt4.QtNetwork", "PyQt4.QtOpenGL", "PyQt4.QtScript",
            "PyQt4.QtSql", "PyQt4.QtSvg", "PyQt4.QtTest", "PyQt4.QtXml"):
        try:
            finder.IncludeModule(name)
        except ImportError:
            pass


def load_Tkinter(finder, module):
    """the Tkinter module has data files that are required to be loaded so
       ensure that they are copied into the directory that is expected at
       runtime."""
    import Tkinter
    import _tkinter
    tk = _tkinter.create()
    tclDir = os.path.dirname(tk.call("info", "library"))
    tclSourceDir = os.path.join(tclDir, "tcl%s" % _tkinter.TCL_VERSION)
    tkSourceDir = os.path.join(tclDir, "tk%s" % _tkinter.TK_VERSION)
    finder.IncludeFiles(tclSourceDir, "tcl")
    finder.IncludeFiles(tkSourceDir, "tk")


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


def load_win32file(finder, module):
    """the win32api module implicitly loads the pywintypes module; make sure
       this happens."""
    finder.IncludeModule("pywintypes")


def load_xml(finder, module):
    """the builtin xml package attempts to load the _xmlplus module to see if
       that module should take its role instead; ignore the failure to find
       this module, though."""
    module.IgnoreName("_xmlplus")


def load_xml_etree_cElementTree(finder, module):
    """the xml.etree.cElementTree module implicitly loads the
       xml.etree.ElementTree module; make sure this happens."""
    finder.IncludeModule("xml.etree.ElementTree")


def missing_cElementTree(finder, caller):
    """the cElementTree has been incorporated into the standard library in
       Python 2.5 so ignore its absence if it cannot found."""
    if sys.version_info[:2] >= (2, 5):
        caller.IgnoreName("cElementTree")


def missing_EasyDialogs(finder, caller):
    """the EasyDialogs module is not normally present on Windows but it also
       may be so instead of excluding it completely, ignore it if it can't be
       found"""
    if sys.platform == "win32":
        caller.IgnoreName("EasyDialogs")


def missing_gdk(finder, caller):
    """the gdk module is buried inside gtk so there is no need to concern
       ourselves with an error saying that it cannot be found"""
    caller.IgnoreName("gdk")


def missing_ltihooks(finder, caller):
    """this module is not necessairly present so ignore it when it cannot be
       found"""
    caller.IgnoreName("ltihooks")


def missing_readline(finder, caller):
    """the readline module is not normally present on Windows but it also may
       be so instead of excluding it completely, ignore it if it can't be
       found"""
    if sys.platform == "win32":
        caller.IgnoreName("readline")


def missing_xml_etree(finder, caller):
    """the xml.etree package is new for Python 2.5 but it is common practice
       to use a try..except.. block in order to support versions earlier than
       Python 2.5 transparently; ignore the absence of the package in this
       situation."""
    if sys.version_info[:2] < (2, 5):
        caller.IgnoreName("xml.etree")

