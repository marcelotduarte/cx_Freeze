"""Utility module for freezing Python modules to a base binary."""

import imp
import marshal
import os
import sys
import struct
import time
import zipfile

# NOTE: the try: except: block in this code is not necessary under Python 2.4
# and higher and can be removed once support for Python 2.3 is no longer needed
EXTENSION_LOADER_SOURCE = \
"""
import imp, os, sys

found = False
for p in sys.path:
    if not os.path.isdir(p):
        continue
    f = os.path.join(p, "%s")
    if not os.path.exists(f):
        continue
    try:
        m = imp.load_dynamic(__name__, f)
    except ImportError:
        del sys.modules[__name__]
        raise
    sys.modules[__name__] = m
    found = True
    break
if not found:
    del sys.modules[__name__]
    raise ImportError, "No module named %%s" %% __name__
"""


def CreateExtensionLoaders(moduleFinder):
    """Create extension loaders for all modules which are extensions which
       would not be found using the normal import mechanism; these include such
       things as extensions found within packages and modules which have names
       that don't correspond to the file name in which they are found."""
    for name, module in moduleFinder.modules.items():
        if module.__code__ is not None or module.__file__ is None:
            continue
        fileName = os.path.basename(module.__file__)
        baseFileName, ext = os.path.splitext(fileName)
        if baseFileName != name and name != "zlib":
            if "." in name:
                fileName = name + ext
            generatedFileName = "ExtensionLoader_%s.py" % \
                    name.replace(".", "_")
            module.__code__ = compile(EXTENSION_LOADER_SOURCE % fileName,
                    generatedFileName, "exec")
            moduleFinder.scan_code(module.__code__, module)
        moduleFinder.AddDependentFile(module.__file__, fileName)


def FullFileName(subDir, name, defaultName):
    """Return the full name of the file to use."""
    if name is None:
        name = defaultName
    defaultBaseName, defaultExt = \
            os.path.splitext(os.path.normcase(defaultName))
    name, ext = os.path.splitext(os.path.normcase(name))
    if not ext:
        ext = defaultExt
    if os.path.isfile(sys.path[0]):
        baseDir = os.path.dirname(sys.path[0])
    else:
        baseDir = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(baseDir, subDir, name + ext)


def Freeze(targetFileName, moduleFinder, zipIncludes, compress):
    """Freeze the modules found by the finder to the end of the file."""
    outFile = zipfile.PyZipFile(targetFileName, "a", zipfile.ZIP_DEFLATED)
    for name, module in moduleFinder.modules.iteritems():
        if module.__code__ is None:
            continue
        fileName = "/".join(name.split("."))
        if module.__path__:
            fileName += "/__init__"
        if os.path.exists(module.__file__):
            mtime = os.stat(module.__file__).st_mtime
        else:
            mtime = time.time()
        zipTime = time.localtime(mtime)[:6]
        data = imp.get_magic() + struct.pack("<i", mtime) + \
                marshal.dumps(module.__code__)
        zinfo = zipfile.ZipInfo(fileName + ".pyc", zipTime)
        if compress:
            zinfo.compress_type = zipfile.ZIP_DEFLATED
        outFile.writestr(zinfo, data)
    for spec in zipIncludes:
        if '=' in spec:
            fileName, archiveName = spec.split('=', 1)
        else:
            fileName = archiveName = spec
        outFile.write(fileName, archiveName)

