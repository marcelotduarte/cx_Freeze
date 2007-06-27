"""Wrapper for the standard library Python module modulefinder which manages
   a few of the things that the standard module does not manage."""

import glob
import imp
import modulefinder
import os
import shutil
import sys

# ensure that PyXML is handled properly if found
modulefinder.ReplacePackage("_xmlplus", "xml")

class ModuleFinder(modulefinder.ModuleFinder):
    """Subclass of modulefinder which handles a few situations that the
       base class does not handle very well."""

    def __init__(self, excludes, replacePaths):
        modulefinder.ModuleFinder.__init__(self, excludes = excludes,
                replace_paths = replacePaths.items())
        self.dependentFiles = {}

    def AddDependentFile(self, sourceName, targetName = None):
        """Add a dependent file to the list of dependent files."""
        if targetName is None:
            targetName = os.path.basename(sourceName)
        self.dependentFiles[targetName] = sourceName

    def CopyDependentFiles(self, dir, listFileName = None):
        """Copy the required files to the directory and optionally include the
           list of files in the file specified."""
        for targetName, sourceName in self.dependentFiles.iteritems():
            sourceName = os.path.abspath(sourceName)
            targetName = os.path.join(dir, targetName)
            if targetName == sourceName:
                print "Skipping", sourceName
                continue
            print "Copying", sourceName
            if os.path.exists(targetName):
                os.chmod(targetName, 0777)
                os.remove(targetName)
            shutil.copy2(sourceName, targetName)
        if listFileName is not None:
            fileNames = [os.path.join(dir, n) for n in self.dependentFiles]
            fileNames.sort()
            print >> file(listFileName, "w"), "\n".join(fileNames)

    def find_module(self, name, path, parent = None):
        """Find the module and return a reference to it."""
        if path is None and name in ("pythoncom", "pywintypes"):
            try:
                module = __import__(name)
                return None, module.__file__, (".dll", "rb", imp.C_EXTENSION)
            except ImportError:
                pass
        fp, modulePath, stuff = modulefinder.ModuleFinder.find_module(self,
                name, path, parent)
        if name == "win32com":
            modulefinder.AddPackagePath(name,
                    os.path.join(os.path.dirname(modulePath), "win32comext"))
        return fp, modulePath, stuff

    def load_module(self, fqname, fp, path, stuff):
        """Load the module and return a reference to it."""
        try:
            module = modulefinder.ModuleFinder.load_module(self, fqname, fp,
                    path, stuff)
        except SyntaxError, value:
            raise "Module %s from file %s has %s." % (fqname, path, value)
        suffix, mode, type = stuff
        if type == imp.C_EXTENSION \
                and (fqname.startswith("wxPython.") \
                or fqname.startswith("wx.")):
            if sys.platform == "win32":
                dir = os.path.dirname(module.__file__)
                for dll in glob.glob(os.path.join(dir, "wx*.dll")):
                    self.AddDependentFile(dll)
            else:
                for line in os.popen("ldd %s" % module.__file__).readlines():
                    line = line.strip()
                    if not line.startswith("libwx"):
                        continue
                    libName, libLocation = line.split(" => ")
                    if libLocation == "not found":
                        raise "Library %s not found." % libName
                    self.AddDependentFile(libLocation.split()[0])
        return module

    def load_file(self, pathname, moduleName):
        """Load a module from a given file."""
        fp = file(pathname, "r")
        name, ext = os.path.splitext(pathname)
        stuff = (ext, "r", imp.PY_SOURCE)
        self.load_module(moduleName, fp, pathname, stuff)

