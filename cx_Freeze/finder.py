"""
Base class for finding modules.
"""

import dis
import imp
import logging
import marshal
import opcode
import os
import pkgutil
import re
import sys
import types
import zipfile

import cx_Freeze.hooks

BUILD_LIST = opcode.opmap["BUILD_LIST"]
INPLACE_ADD = opcode.opmap["INPLACE_ADD"]
LOAD_CONST = opcode.opmap["LOAD_CONST"]
IMPORT_NAME = opcode.opmap["IMPORT_NAME"]
IMPORT_FROM = opcode.opmap["IMPORT_FROM"]
IMPORT_STAR = opcode.opmap["IMPORT_STAR"]
STORE_FAST = opcode.opmap["STORE_FAST"]
STORE_NAME = opcode.opmap["STORE_NAME"]
STORE_GLOBAL = opcode.opmap["STORE_GLOBAL"]
STORE_OPS = (STORE_NAME, STORE_GLOBAL)

__all__ = [ "Module", "ModuleFinder" ]

try:
    bytes   # Python >= 2.6
except NameError:
    bytes = str

try:
    source_from_cache = imp.source_from_cache  # Python 3.2 and above
except AttributeError:
    def source_from_cache(path):  # Pre PEP 3147 - cache is just .pyc/.pyo
        assert path.endswith(('.pyc', '.pyo'))
        return path[:-1]

class ZipModulesCache(object):
    """A cache of module and package locations within zip files."""
    def __init__(self):
        # filename -> None (used like a set)
        self.files_seen = {}
        # (path, modulename) -> module_details
        self.loadable_modules = {}
    
    def find(self, path, modulename):
        """Find a module in the given path.
        
        path should be a string referring to a zipfile or a directory in a
        zip file. If it is outside a zip file, it will be ignored.
        
        modulename should be a string, with only the last part of the module
        name, i.e. not containing any dots.
        
        If the module is found, this returns information in the same format
        as :func:`imp.find_module`. Otherwise, it returns None.
        """
        try:
            return self.retrieve_loadable_module(path, modulename)
        except KeyError:
            pass

        if path in self.files_seen:
            return None

        # This is a marker that we've seen it, whether or not it's a zip file.
        self.files_seen[path] = None

        if os.path.isfile(path) and zipfile.is_zipfile(path):
            self.cache_zip_file(path)
            try:
                return self.retrieve_loadable_module(path, modulename)
            except KeyError:
                return None
    
    def retrieve_loadable_module(self, directory, modulename):
        """Retrieve a module from the cache and translate its info into the
        format returned by :func:`imp.find_module`.
        
        Raises KeyError if the module is not present.
        """
        zip, ideal_path, actual_path, ispkg = self.loadable_modules[directory, modulename]
        # zip: zipfile.ZipFile object
        # ideal_path: the path to the pkg directory or module .py file
        # actual path: path to the .pyc file (None for pkg directories)
        # ispkg: bool, True if this entry refers to a package.
        full_path = os.path.join(zip.filename, ideal_path)
        if ispkg:
            return None, full_path, ('', '', imp.PKG_DIRECTORY)
        else:                
            fp = zip.read(actual_path)
            info = (".pyc", "rb", imp.PY_COMPILED)
            return fp, full_path, info
    
    def cache_zip_file(self, zip_path):
        """Read a zip file and cache the modules and packages found inside it.
        """
        zip = zipfile.ZipFile(zip_path)
        for archiveName in zip.namelist():
            baseName, ext = os.path.splitext(archiveName)
            if ext not in ('.pyc', '.pyo'):
                continue
            if '__pycache__' in baseName:
                if sys.version_info[:2] < (3, 2) \
                        or not baseName.endswith(imp.get_tag()):
                    continue
                baseName = os.path.splitext(source_from_cache(archiveName))[0]
            nameparts = baseName.split("/")
            
            if len(nameparts) > 1 and nameparts[-1] == '__init__':
                # dir/__init__.pyc  -> dir is a package
                self.record_loadable_module(nameparts[:-1], None, zip, True)

            self.record_loadable_module(nameparts, archiveName, zip, False)

    def record_loadable_module(self, nameparts, actual_path, zip, ispkg=False):
        """Cache one module found in the zip file."""
        parent_dir = os.path.normpath(os.path.join(zip.filename, "/".join(nameparts[:-1])))
        modulename = nameparts[-1]
        ideal_path = "/".join(nameparts) + ("" if ispkg else ".py")
        if (parent_dir, modulename) not in self.loadable_modules:
            self.loadable_modules[parent_dir, modulename] = (zip, ideal_path, actual_path, ispkg)

class ModuleFinder(object):

    def __init__(self, includeFiles = None, excludes = [], path = None,
            replacePaths = None):
        self.includeFiles = includeFiles
        if includeFiles is None:
            self.includeFiles = []
        self.excludeDependentFiles = {}
        self.excludes = dict.fromkeys(excludes)
        self.replacePaths = replacePaths
        if replacePaths is None:
            self.replacePaths = []
        self.path = path or sys.path
        self.modules = []
        self.aliases = {}
        self._modules = dict.fromkeys(excludes)
        self._builtinModules = dict.fromkeys(sys.builtin_module_names)
        self._badModules = {}
        self._zip_modules_cache = ZipModulesCache()
        cx_Freeze.hooks.initialize(self)
        initialExcludedModules = self.excludes.copy()
        self._AddBaseModules()

    def _AddBaseModules(self):
        """Add the base modules to the finder. These are the modules that
           Python imports itself during initialization and, if not found,
           can result in behavior that differs from running from source;
           also include modules used within the bootstrap code.

           When cx_Freeze is built, these modules (and modules they load) are
           included in the startup zip file.
           """
        self.IncludeModule("traceback")
        self.IncludeModule("warnings")
        self.IncludePackage("encodings")
        if sys.version_info[0] >= 3:
            self.IncludeModule("io")
        self.IncludeModule("os")
        self.IncludeModule("sys")
        self.IncludeModule("zlib")
        if sys.version_info[:2] >= (3, 4):
            # We need this, because collections gets loaded (via traceback),
            # and a partially frozen package causes problems.
            self.IncludeModule("collections.abc")
        if sys.version_info[:2] >= (3,5):
            self.IncludeModule("importlib.abc")

    def _AddModule(self, name):
        """Add a module to the list of modules but if one is already found,
           then return it instead; this is done so that packages can be
           handled properly."""
        module = self._modules.get(name)
        if module is None:
            module = self._modules[name] = Module(name)
            self.modules.append(module)
            if name in self._badModules:
                logging.debug("Removing module [%s] from list of bad modules",
                        name)
                del self._badModules[name]
        return module

    def _DetermineParent(self, caller):
        """Determine the parent to use when searching packages."""
        if caller is not None:
            if caller.path is not None:
                return caller
            return self._GetParentByName(caller.name)

    def _EnsureFromList(self, caller, packageModule, fromList,
            deferredImports):
        """Ensure that the from list is satisfied. This is only necessary for
           package modules. If the package module has not been completely
           imported yet, defer the import until it has been completely imported
           in order to avoid spurious errors about missing modules."""
        if packageModule.inImport and caller is not packageModule:
            deferredImports.append((caller, packageModule, fromList))
        else:
            for name in fromList:
                if name in packageModule.globalNames:
                    continue
                subModuleName = "%s.%s" % (packageModule.name, name)
                self._ImportModule(subModuleName, deferredImports, caller)

    def _FindModule(self, name, path, namespace):
        try:
            # imp loads normal modules from the filesystem
            return imp.find_module(name, path)
        except ImportError:
            if namespace and name in sys.modules:
                # Namespace package (?)
                module = sys.modules[name]
                info = ("", "", imp.PKG_DIRECTORY)
                return None, list(module.__path__)[0], info

            # Check for modules in zip files.
            # If a path is a subdirectory within a zip file, we must have
            # already cached the contents of the zip file to find modules in it.
            if path is None:
                path = []
            for location in path:
                res = self._zip_modules_cache.find(location, name)
                if res is not None:
                    return res
            raise

    def _GetParentByName(self, name):
        """Return the parent module given the name of a module."""
        pos = name.rfind(".")
        if pos > 0:
            parentName = name[:pos]
            return self._modules[parentName]

    def _ImportAllSubModules(self, module, deferredImports, recursive = True):
        """Import all sub modules to the given package."""
        suffixes = [s[0] for s in imp.get_suffixes()]

        for path in module.path:
            try:
                fileNames = os.listdir(path)
            except os.error:
                continue

            for fileName in fileNames:
                fullName = os.path.join(path, fileName)
                if os.path.isdir(fullName):
                    initFile = os.path.join(fullName, "__init__.py")
                    if not os.path.exists(initFile):
                        continue
                    name = fileName
                else:
                    # We need to run through these in order to correctly pick
                    # up PEP 3149 library names (e.g. .cpython-32mu.so).
                    for suffix in suffixes:
                        if fileName.endswith(suffix):
                            name = fileName[:-len(suffix)]

                            # Skip modules whose names appear to contain '.',
                            # as we may be using the wrong suffix, and even if
                            # we're not, such module names will break the import
                            # code.
                            if "." not in name:
                                break

                    else:
                        continue
                    if name == "__init__":
                        continue

                subModuleName = "%s.%s" % (module.name, name)
                subModule = self._InternalImportModule(subModuleName,
                                deferredImports)
                if subModule is None:
                    if subModuleName not in self.excludes:
                        raise ImportError("No module named %r" % subModuleName)
                else:
                    module.globalNames[name] = None
                    if subModule.path and recursive:
                        self._ImportAllSubModules(subModule, deferredImports,
                                recursive)

    def _ImportDeferredImports(self, deferredImports, skipInImport = False):
        """Import any sub modules that were deferred, if applicable."""
        while deferredImports:
            newDeferredImports = []
            for caller, packageModule, subModuleNames in deferredImports:
                if packageModule.inImport and skipInImport:
                    continue
                self._EnsureFromList(caller, packageModule, subModuleNames,
                        newDeferredImports)
            deferredImports = newDeferredImports
            skipInImport = True

    def _ImportModule(self, name, deferredImports, caller = None,
            relativeImportIndex = 0, namespace = False):
        """Attempt to find the named module and return it or None if no module
           by that name could be found."""

        # absolute import (available in Python 2.5 and up)
        # the name given is the only name that will be searched
        if relativeImportIndex == 0:
            module = self._InternalImportModule(name,
                    deferredImports, namespace = namespace)

        # old style relative import (regular 'import foo' in Python 2)
        # the name given is tried in the current package, and if
        # no match is found, sys.path is searched for a top-level module/pockage
        elif relativeImportIndex < 0:
            parent = self._DetermineParent(caller)
            if parent is not None:
                fullName = "%s.%s" % (parent.name, name)
                module = self._InternalImportModule(fullName,
                        deferredImports, namespace = namespace)
                if module is not None:
                    parent.globalNames[name] = None
                    return module

            module = self._InternalImportModule(name,
                    deferredImports, namespace = namespace)

        # new style relative import (available in Python 2.5 and up)
        # the index indicates how many levels to traverse and only that level
        # is searched for the named module
        elif relativeImportIndex > 0:
            parent = caller
            if parent.path is not None:
                relativeImportIndex -= 1
            while parent is not None and relativeImportIndex > 0:
                parent = self._GetParentByName(parent.name)
                relativeImportIndex -= 1
            if parent is None:
                module = None
            elif not name:
                module = parent
            else:
                name = "%s.%s" % (parent.name, name)
                module = self._InternalImportModule(name,
                        deferredImports, namespace = namespace)

        # if module not found, track that fact
        if module is None:
            if caller is None:
                raise ImportError("No module named %r" % name)
            self._RunHook("missing", name, caller)
            if name not in caller.ignoreNames:
                callers = self._badModules.setdefault(name, {})
                callers[caller.name] = None

        return module

    def _InternalImportModule(self, name, deferredImports, namespace = False):
        """Internal method used for importing a module which assumes that the
           name given is an absolute name. None is returned if the module
           cannot be found."""
        try:
            # Check in module cache before trying to import it again.
            return self._modules[name]
        except KeyError:
            pass

        if name in self._builtinModules:
            module = self._AddModule(name)
            logging.debug("Adding module [%s] [C_BUILTIN]", name)
            self._RunHook("load", module.name, module)
            module.inImport = False
            return module

        pos = name.rfind(".")
        if pos < 0:  # Top-level module
            path = self.path
            searchName = name
            parentModule = None
        else:        # Dotted module name - look up the parent module
            parentName = name[:pos]
            parentModule = \
                    self._InternalImportModule(parentName, deferredImports,
                            namespace = namespace)
            if parentModule is None:
                return None
            if namespace:
                parentModule.ExtendPath()
            path = parentModule.path
            searchName = name[pos + 1:]

        if name in self.aliases:
            actualName = self.aliases[name]
            module = self._InternalImportModule(actualName, deferredImports)
            self._modules[name] = module
            return module

        try:
            fp, path, info = self._FindModule(searchName, path, namespace)
            if info[-1] == imp.C_BUILTIN and parentModule is not None:
                return None
            module = self._LoadModule(name, fp, path, info, deferredImports,
                    parentModule, namespace)
        except ImportError:
            logging.debug("Module [%s] cannot be imported", name)
            self._modules[name] = None
            return None
        return module

    def _LoadModule(self, name, fp, path, info, deferredImports,
            parent = None, namespace = False):
        """Load the module, given the information acquired by the finder."""
        suffix, mode, type = info
        if type == imp.PKG_DIRECTORY:
            return self._LoadPackage(name, path, parent, deferredImports,
                    namespace)
        module = self._AddModule(name)
        module.file = path
        module.parent = parent

        if type == imp.PY_SOURCE:
            logging.debug("Adding module [%s] [PY_SOURCE]", name)
            # Load & compile Python source code
            if sys.version_info[0] >= 3:
                # For Python 3, read the file with the correct encoding
                import tokenize
                fp = open(path, "rb")
                encoding, lines = tokenize.detect_encoding(fp.readline)
                fp = open(path, "U", encoding = encoding)
            codeString = fp.read()
            if codeString and codeString[-1] != "\n":
                codeString = codeString + "\n"
            try:
                module.code = compile(codeString, path, "exec")
            except SyntaxError:
                raise ImportError("Invalid syntax in %s" % path)
        
        elif type == imp.PY_COMPILED:
            logging.debug("Adding module [%s] [PY_COMPILED]", name)
            # Load Python bytecode
            if isinstance(fp, bytes):
                magic = fp[:4]
            else:
                magic = fp.read(4)
            if magic != imp.get_magic():
                raise ImportError("Bad magic number in %s" % path)
            skip_bytes = 8 if (sys.version_info[:2] >= (3,3)) else 4
            if isinstance(fp, bytes):
                module.code = marshal.loads(fp[skip_bytes+4:])
                module.inZipFile = True
            else:
                fp.read(skip_bytes)
                module.code = marshal.load(fp)
        
        elif type == imp.C_EXTENSION:
            logging.debug("Adding module [%s] [C_EXTENSION]", name)
            if parent is None:
                # Our extension loader (see the freezer module) uses imp to
                # load compiled extensions.
                self.IncludeModule("imp")

        # If there's a custom hook for this module, run it.
        self._RunHook("load", module.name, module)
        
        if module.code is not None:
            if self.replacePaths:
                topLevelModule = module
                while topLevelModule.parent is not None:
                    topLevelModule = topLevelModule.parent
                module.code = self._ReplacePathsInCode(topLevelModule,
                        module.code)
            
            # Scan the module code for import statements
            self._ScanCode(module.code, module, deferredImports)
        
        module.inImport = False
        return module

    def _LoadPackage(self, name, path, parent, deferredImports, namespace):
        """Load the package, given its name and path."""
        module = self._AddModule(name)
        module.path = [path]
        try:
            fp, path, info = self._FindModule("__init__", module.path, False)
            self._LoadModule(name, fp, path, info, deferredImports, parent)
            logging.debug("Adding module [%s] [PKG_DIRECTORY]", name)
        except ImportError:
            if not namespace:
                raise
            fileName = os.path.join(path, "__init__.py")
            module.code = compile("", fileName, "exec")
            logging.debug("Adding module [%s] [PKG_NAMESPACE_DIRECTORY]", name)
        return module

    def _ReplacePathsInCode(self, topLevelModule, co):
        """Replace paths in the code as directed, returning a new code object
           with the modified paths in place."""
        # Prepare the new filename.
        origFileName = newFileName = os.path.normpath(co.co_filename)
        for searchValue, replaceValue in self.replacePaths:
            if searchValue == "*":
                searchValue = os.path.dirname(topLevelModule.file)
                if topLevelModule.path:
                    searchValue = os.path.dirname(searchValue)
                if searchValue:
                    searchValue = searchValue + os.path.sep
            if not origFileName.startswith(searchValue):
                continue
            newFileName = replaceValue + origFileName[len(searchValue):]
            break
        
        # Run on subordinate code objects from function & class definitions.
        constants = list(co.co_consts)
        for i, value in enumerate(constants):
            if isinstance(value, type(co)):
                constants[i] = self._ReplacePathsInCode(topLevelModule, value)
        
        # Build the new code object.
        if sys.version_info[0] < 3:
            return types.CodeType(co.co_argcount, co.co_nlocals,
                    co.co_stacksize, co.co_flags, co.co_code, tuple(constants),
                    co.co_names, co.co_varnames, newFileName, co.co_name,
                    co.co_firstlineno, co.co_lnotab, co.co_freevars,
                    co.co_cellvars)
        return types.CodeType(co.co_argcount, co.co_kwonlyargcount,
                co.co_nlocals, co.co_stacksize, co.co_flags, co.co_code,
                tuple(constants), co.co_names, co.co_varnames, newFileName,
                co.co_name, co.co_firstlineno, co.co_lnotab, co.co_freevars,
                co.co_cellvars)

    def _RunHook(self, hookName, moduleName, *args):
        """Run hook for the given module if one is present."""
        name = "%s_%s" % (hookName, moduleName.replace(".", "_"))
        method = getattr(cx_Freeze.hooks, name, None)
        if method is not None:
            method(self, *args)

    def _ScanCode(self, co, module, deferredImports, topLevel = True):
        """Scan code, looking for imported modules and keeping track of the
           constants that have been created in order to better tell which
           modules are truly missing."""
        arguments = []
        importedModule = None
        method = dis._unpack_opargs if sys.version_info[:3] >= (3, 5, 2) \
                else self._UnpackOpArgs
        for opIndex, op, opArg in method(co.co_code):

            # keep track of constants (these are used for importing)
            # immediately restart loop so arguments are retained
            if op == LOAD_CONST:
                arguments.append(co.co_consts[opArg])
                continue

            # import statement: attempt to import module
            elif op == IMPORT_NAME:
                name = co.co_names[opArg]
                if len(arguments) >= 2:
                    relativeImportIndex, fromList = arguments[-2:]
                else:
                    relativeImportIndex = -1
                    fromList = arguments[0] if arguments else []
                if name not in module.excludeNames:
                    importedModule = self._ImportModule(name, deferredImports,
                            module, relativeImportIndex)
                    if importedModule is not None:
                        if fromList and fromList != ("*",) \
                                and importedModule.path is not None:
                            self._EnsureFromList(module, importedModule,
                                    fromList, deferredImports)

            # import * statement: copy all global names
            elif op == IMPORT_STAR and topLevel and importedModule is not None:
                module.globalNames.update(importedModule.globalNames)

            # store operation: track only top level
            elif topLevel and op in STORE_OPS:
                name = co.co_names[opArg]
                module.globalNames[name] = None

            # reset arguments; these are only needed for import statements so
            # ignore them in all other cases!
            arguments = []

        # Scan the code objects from function & class definitions
        for constant in co.co_consts:
            if isinstance(constant, type(co)):
                self._ScanCode(constant, module, deferredImports,
                        topLevel = False)

    def _UnpackOpArgs(self, code):
        """Unpack the operations and arguments from the byte code. From Python
           3.5 onwards this is found in the private method _unpack_opargs
           but for earlier releases this wasn't available as a separate
           method."""
        opIndex = 0
        numOps = len(code)
        is3 = sys.version_info[0] >= 3
        while opIndex < numOps:
            offset = opIndex
            if is3:
                op = code[opIndex]
            else:
                op = ord(code[opIndex])
            opIndex += 1
            arg = None
            if op >= dis.HAVE_ARGUMENT:
                if is3:
                    arg = code[opIndex] + code[opIndex + 1] * 256
                else:
                    arg = ord(code[opIndex]) + ord(code[opIndex + 1]) * 256
                opIndex += 2
            yield (offset, op, arg)

    def AddAlias(self, name, aliasFor):
        """Add an alias for a particular module; when an attempt is made to
           import a module using the alias name, import the actual name
           instead."""
        self.aliases[name] = aliasFor

    def ExcludeDependentFiles(self, fileName):
        self.excludeDependentFiles[fileName] = None

    def ExcludeModule(self, name):
        """Exclude the named module from the resulting frozen executable."""
        self.excludes[name] = None
        self._modules[name] = None

    def IncludeFile(self, path, moduleName = None):
        """Include the named file as a module in the frozen executable."""
        name, ext = os.path.splitext(os.path.basename(path))
        if moduleName is None:
            moduleName = name
        info = (ext, "r", imp.PY_SOURCE)
        deferredImports = []
        module = self._LoadModule(moduleName, open(path, "U"), path, info,
                deferredImports)
        self._ImportDeferredImports(deferredImports)
        return module

    def IncludeFiles(self, sourcePath, targetPath, copyDependentFiles = True):
        """Include the files in the given directory in the target build."""
        self.includeFiles.append((sourcePath, targetPath))
        if not copyDependentFiles:
            self.ExcludeDependentFiles(sourcePath)

    def IncludeModule(self, name, namespace = False):
        """Include the named module in the frozen executable."""
        deferredImports = []
        module = self._ImportModule(name, deferredImports,
                namespace = namespace)
        self._ImportDeferredImports(deferredImports, skipInImport = True)
        return module

    def IncludePackage(self, name):
        """Include the named package and any submodules in the frozen
           executable."""
        deferredImports = []
        module = self._ImportModule(name, deferredImports)
        if module.path:
            self._ImportAllSubModules(module, deferredImports)
        self._ImportDeferredImports(deferredImports, skipInImport = True)
        return module

    def ReportMissingModules(self):
        """Display a list of modules that weren't found."""
        if self._badModules:
            sys.stdout.write("Missing modules:\n")
            names = list(self._badModules.keys())
            names.sort()
            for name in names:
                callers = list(self._badModules[name].keys())
                callers.sort()
                sys.stdout.write("? %s imported from %s\n" % \
                        (name, ", ".join(callers)))
            sys.stdout.write("This is not necessarily a problem - the modules "
                             "may not be needed on this platform.\n")
            sys.stdout.write("\n")


class Module(object):

    def __init__(self, name):
        self.name = name
        self.file = None
        self.path = None
        self.code = None
        self.parent = None
        self.globalNames = {}
        self.excludeNames = {}
        self.ignoreNames = {}
        self.inZipFile = False
        self.inImport = True

    def __repr__(self):
        parts = ["name=%s" % repr(self.name)]
        if self.file is not None:
            parts.append("file=%s" % repr(self.file))
        if self.path is not None:
            parts.append("path=%s" % repr(self.path))
        return "<Module %s>" % ", ".join(parts)

    def AddGlobalName(self, name):
        self.globalNames[name] = None

    def ExcludeName(self, name):
        self.excludeNames[name] = None

    def ExtendPath(self):
        self.path = pkgutil.extend_path(self.path, self.name)
        if self.parent is not None:
            self.parent.ExtendPath()

    def IgnoreName(self, name):
        self.ignoreNames[name] = None

