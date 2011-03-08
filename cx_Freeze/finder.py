"""
Base class for finding modules.
"""

import dis
import imp
import marshal
import opcode
import os
import pkgutil
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

class ModuleFinder(object):

    def __init__(self, includeFiles = None, excludes = [], path = None,
            replacePaths = None, copyDependentFiles = True, bootstrap = False,
            compress = True):
        self.includeFiles = includeFiles
        if includeFiles is None:
            self.includeFiles = []
        self.excludes = dict.fromkeys(excludes)
        self.replacePaths = replacePaths
        if replacePaths is None:
            self.replacePaths = []
        self.copyDependentFiles = copyDependentFiles
        self.compress = compress
        self.path = path or sys.path
        self.modules = []
        self.aliases = {}
        self._modules = dict.fromkeys(excludes)
        self._builtinModules = dict.fromkeys(sys.builtin_module_names)
        self._badModules = {}
        self._zipFileEntries = {}
        self._zipFiles = {}
        cx_Freeze.hooks.initialize(self)
        initialExcludedModules = self.excludes.copy()
        self._AddBaseModules()
        if not bootstrap:
            self._ClearBaseModuleCode(initialExcludedModules)

    def _AddBaseModules(self):
        """Add the base modules to the finder. These are the modules that
           Python imports itself during initialization and, if not found,
           can result in behavior that differs from running from source;
           also include modules used within the bootstrap code"""
        self.ExcludeModule("cStringIO")
        self.ExcludeModule("doctest")
        self.ExcludeModule("getopt")
        self.ExcludeModule("logging")
        self.ExcludeModule("re")
        self.ExcludeModule("subprocess")
        self.IncludeModule("traceback")
        self.IncludeModule("warnings")
        self.IncludePackage("encodings")
        if sys.version_info[0] >= 3:
            self.IncludeModule("io")
        if self.copyDependentFiles:
            self.IncludeModule("imp")
            self.IncludeModule("os")
            self.IncludeModule("sys")
            self.IncludeModule("zlib")

    def _AddModule(self, name):
        """Add a module to the list of modules but if one is already found,
           then return it instead; this is done so that packages can be
           handled properly."""
        module = self._modules.get(name)
        if module is None:
            module = self._modules[name] = Module(name)
            self.modules.append(module)
            if name in self._badModules:
                del self._badModules[name]
        return module

    def _ClearBaseModuleCode(self, initialExcludedModules):
        """Clear the code for all of the base modules. This is done when not in
           bootstrap mode so that the base modules are not included in the
           zip file."""
        for name in self.excludes:
            if name in initialExcludedModules:
                continue
            del self._modules[name]
        self.excludes = initialExcludedModules
        for module in self._modules.values():
            if module is None:
                continue
            if module.code is not None:
                module.code = None
                module.file = None

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
            return imp.find_module(name, path)
        except ImportError:
            if namespace and name in sys.modules:
                module = sys.modules[name]
                info = ("", "", imp.PKG_DIRECTORY)
                return None, module.__path__[0], info
            if path is None:
                path = []
            for location in path:
                if name in self._zipFileEntries:
                    break
                if location in self._zipFiles:
                    continue
                if os.path.isdir(location) or not zipfile.is_zipfile(location):
                    self._zipFiles[location] = None
                    continue
                zip = zipfile.ZipFile(location)
                for archiveName in zip.namelist():
                    baseName, ext = os.path.splitext(archiveName)
                    if ext not in ('.pyc', '.pyo'):
                        continue
                    moduleName = ".".join(baseName.split("/"))
                    if moduleName in self._zipFileEntries:
                        continue
                    self._zipFileEntries[moduleName] = (zip, archiveName)
                self._zipFiles[location] = None
            info = self._zipFileEntries.get(name)
            if info is not None:
                zip, archiveName = info
                fp = zip.read(archiveName)
                info = (".pyc", "rb", imp.PY_COMPILED)
                return fp, os.path.join(zip.filename, archiveName), info
            raise

    def _GetParentByName(self, name):
        """Return the parent module given the name of a module."""
        pos = name.rfind(".")
        if pos > 0:
            parentName = name[:pos]
            return self._modules[parentName]

    def _ImportAllSubModules(self, module, deferredImports, recursive = True):
        """Import all sub modules to the given package."""
        suffixes = dict.fromkeys([s[0] for s in imp.get_suffixes()])
        for dir in module.path:
            try:
                fileNames = os.listdir(dir)
            except os.error:
                continue
            for fileName in fileNames:
                name, ext = os.path.splitext(fileName)
                if ext not in suffixes:
                    continue
                if name == "__init__":
                    continue
                subModuleName = "%s.%s" % (module.name, name)
                subModule, returnError = \
                        self._InternalImportModule(subModuleName,
                                deferredImports)
                if returnError and subModule is None:
                    raise ImportError("No module named %r" % subModuleName)
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

    def _ImportModule(self, name, deferredImports, caller = None,
            relativeImportIndex = 0, namespace = False):
        """Attempt to find the named module and return it or None if no module
           by that name could be found."""

        # absolute import (available in Python 2.5 and up)
        # the name given is the only name that will be searched
        if relativeImportIndex == 0:
            module, returnError = self._InternalImportModule(name,
                    deferredImports, namespace = namespace)

        # old style relative import (only possibility in Python 2.4 and prior)
        # the name given is tried in all parents until a match is found and if
        # no match is found, the global namespace is searched
        elif relativeImportIndex < 0:
            parent = self._DetermineParent(caller)
            while parent is not None:
                fullName = "%s.%s" % (parent.name, name)
                module, returnError = self._InternalImportModule(fullName,
                        deferredImports, namespace = namespace)
                if module is not None:
                    parent.globalNames[name] = None
                    return module
                parent = self._GetParentByName(parent.name)
            module, returnError = self._InternalImportModule(name,
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
                returnError = True
            elif not name:
                module = parent
            else:
                name = "%s.%s" % (parent.name, name)
                module, returnError = self._InternalImportModule(name,
                        deferredImports, namespace = namespace)

        # if module not found, track that fact
        if module is None:
            if caller is None:
                raise ImportError("No module named %r" % name)
            self._RunHook("missing", name, caller)
            if returnError and name not in caller.ignoreNames:
                callers = self._badModules.setdefault(name, {})
                callers[caller.name] = None

        return module

    def _InternalImportModule(self, name, deferredImports, namespace = False):
        """Internal method used for importing a module which assumes that the
           name given is an absolute name. None is returned if the module
           cannot be found."""
        try:
            return self._modules[name], False
        except KeyError:
            pass
        if name in self._builtinModules:
            module = self._AddModule(name)
            self._RunHook("load", module.name, module)
            module.inImport = False
            return module, False
        pos = name.rfind(".")
        if pos < 0:
            path = self.path
            searchName = name
            parentModule = None
        else:
            parentName = name[:pos]
            parentModule, returnError = \
                    self._InternalImportModule(parentName, deferredImports,
                            namespace = namespace)
            if parentModule is None:
                return None, returnError
            if namespace:
                parentModule.ExtendPath()
            path = parentModule.path
            searchName = name[pos + 1:]
        if name in self.aliases:
            actualName = self.aliases[name]
            module, returnError = \
                    self._InternalImportModule(actualName, deferredImports)
            self._modules[name] = module
            return module, returnError
        try:
            fp, path, info = self._FindModule(searchName, path, namespace)
            module = self._LoadModule(name, fp, path, info, deferredImports,
                    parentModule, namespace)
        except ImportError:
            self._modules[name] = None
            return None, True
        return module, False

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
            if sys.version_info[0] >= 3:
                import tokenize
                fp = open(path, "rb")
                encoding, lines = tokenize.detect_encoding(fp.readline)
                fp = open(path, "U", encoding = encoding)
            codeString = fp.read()
            if codeString and codeString[-1] != "\n":
                codeString = codeString + "\n"
            module.code = compile(codeString, path, "exec")
        elif type == imp.PY_COMPILED:
            if isinstance(fp, str):
                magic = fp[:4]
            else:
                magic = fp.read(4)
            if magic != imp.get_magic():
                raise ImportError("Bad magic number in %s" % path)
            if isinstance(fp, str):
                module.code = marshal.loads(fp[8:])
                module.inZipFile = True
            else:
                fp.read(4)
                module.code = marshal.load(fp)
        self._RunHook("load", module.name, module)
        if module.code is not None:
            if self.replacePaths:
                topLevelModule = module
                while topLevelModule.parent is not None:
                    topLevelModule = topLevelModule.parent
                module.code = self._ReplacePathsInCode(topLevelModule,
                        module.code)
            self._ScanCode(module.code, module, deferredImports)
        module.inImport = False
        return module

    def _LoadPackage(self, name, path, parent, deferredImports, namespace):
        """Load the package, given its name and path."""
        module = self._AddModule(name)
        module.path = [path]
        try:
            fp, path, info = imp.find_module("__init__", module.path)
            self._LoadModule(name, fp, path, info, deferredImports, parent)
        except ImportError:
            if not namespace:
                raise
            fileName = os.path.join(path, "__init__.py")
            module.code = compile("", fileName, "exec")
        return module

    def _ReplacePathsInCode(self, topLevelModule, co):
        """Replace paths in the code as directed, returning a new code object
           with the modified paths in place."""
        origFileName = newFileName = os.path.normpath(co.co_filename)
        for searchValue, replaceValue in self.replacePaths:
            if searchValue == "*":
                searchValue = os.path.dirname(topLevelModule.file)
                if topLevelModule.path:
                    searchValue = os.path.dirname(searchValue)
                if searchValue:
                    searchValue = searchValue + os.pathsep
            elif not origFileName.startswith(searchValue):
                continue
            newFileName = replaceValue + origFileName[len(searchValue):]
            break
        constants = list(co.co_consts)
        for i, value in enumerate(constants):
            if isinstance(value, type(co)):
                constants[i] = self._ReplacePathsInCode(topLevelModule, value)
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
        opIndex = 0
        arguments = []
        code = co.co_code
        numOps = len(code)
        is3 = sys.version_info[0] >= 3
        while opIndex < numOps:
            if is3:
                op = code[opIndex]
            else:
                op = ord(code[opIndex])
            opIndex += 1
            if op >= dis.HAVE_ARGUMENT:
                if is3:
                    opArg = code[opIndex] + code[opIndex + 1] * 256
                else:
                    opArg = ord(code[opIndex]) + ord(code[opIndex + 1]) * 256
                opIndex += 2
            if op == LOAD_CONST:
                arguments.append(co.co_consts[opArg])
            elif op == IMPORT_NAME:
                name = co.co_names[opArg]
                if len(arguments) == 2:
                    relativeImportIndex, fromList = arguments
                else:
                    relativeImportIndex = -1
                    fromList, = arguments
                if name not in module.excludeNames:
                    importedModule = self._ImportModule(name, deferredImports,
                            module, relativeImportIndex)
                    if importedModule is not None:
                        if fromList and fromList != ("*",) \
                                and importedModule.path is not None:
                            self._EnsureFromList(module, importedModule,
                                    fromList, deferredImports)
            elif op == IMPORT_FROM and topLevel:
                if is3:
                    op = code[opIndex]
                    opArg = code[opIndex + 1] + code[opIndex + 2] * 256
                else:
                    op = ord(code[opIndex])
                    opArg = ord(code[opIndex + 1]) + \
                            ord(code[opIndex + 2]) * 256
                opIndex += 3
                if op == STORE_FAST:
                    name = co.co_varnames[opArg]
                else:
                    name = co.co_names[opArg]
                module.globalNames[name] = None
            elif op == IMPORT_STAR and topLevel and importedModule is not None:
                module.globalNames.update(importedModule.globalNames)
                arguments = []
            elif op not in (BUILD_LIST, INPLACE_ADD):
                if topLevel and op in STORE_OPS:
                    name = co.co_names[opArg]
                    module.globalNames[name] = None
                arguments = []
        for constant in co.co_consts:
            if isinstance(constant, type(co)):
                self._ScanCode(constant, module, deferredImports,
                        topLevel = False)

    def AddAlias(self, name, aliasFor):
        """Add an alias for a particular module; when an attempt is made to
           import a module using the alias name, import the actual name
           instead."""
        self.aliases[name] = aliasFor

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

    def IncludeFiles(self, sourcePath, targetPath):
        """Include the files in the given directory in the target build."""
        if self.copyDependentFiles:
            self.includeFiles.append((sourcePath, targetPath))

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
        if self._badModules:
            sys.stdout.write("Missing modules:\n")
            names = list(self._badModules.keys())
            names.sort()
            for name in names:
                callers = list(self._badModules[name].keys())
                callers.sort()
                sys.stdout.write("? %s imported from %s\n" % \
                        (name, ", ".join(callers)))
            sys.stdout.write("\n")

    def WriteSourceFile(self, fileName):
        dirName = os.path.dirname(fileName)
        if not os.path.isdir(dirName):
            os.makedirs(dirName)
        outfp = open(fileName, "w")
        names = list(self._modules.keys())
        names.sort()
        modulesWritten = []
        for name in names:
            module = self._modules[name]
            if module is None or module.code is None:
                continue
            mangledName = "__".join(name.split("."))
            sys.stdout.write("adding base module named %s\n" % name)
            code = marshal.dumps(module.code)
            size = len(code)
            if module.path:
                size = -size
            modulesWritten.append((name, mangledName, size))
            outfp.write("unsigned char M_%s[] = {" % mangledName)
            for i in range(0, len(code), 16):
                outfp.write("\n\t")
                for op in code[i:i + 16]:
                    if not isinstance(op, int):
                        op = ord(op)
                    outfp.write("%d," % op)
            outfp.write("\n};\n\n");
        outfp.write("static struct _frozen gFrozenModules[] = {\n")
        for name, mangledName, size in modulesWritten:
            outfp.write('    {"%s", M_%s, %d},\n' % (name, mangledName, size))
        outfp.write("    {0, 0, 0}\n};\n")


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

