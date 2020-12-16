"""
Base class for finding modules.
"""

import dis
import importlib.machinery
import logging
import os
import sys
import opcode
from typing import Dict, List, Optional, Union
from importlib.abc import ExecutionLoader

import importlib_metadata
from cx_Freeze.common import rebuild_code_object
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

__all__ = ["Module", "ModuleFinder"]


class ModuleFinder:
    def __init__(
        self,
        include_files=None,
        excludes=None,
        path=None,
        replace_paths=None,
        zip_include_all_packages=False,
        zip_exclude_packages=None,
        zip_include_packages=None,
        constants_module=None,
        zip_includes=None,
    ):
        self.include_files = include_files or []
        self.excludes = dict.fromkeys(excludes or [])
        self.optimizeFlag = 0
        self.path = path or sys.path
        self.replace_paths = replace_paths or []
        self.zip_include_all_packages = zip_include_all_packages
        self.zip_exclude_packages = zip_exclude_packages or []
        self.zip_include_packages = zip_include_packages or []
        self.constants_module = constants_module
        self.zip_includes = zip_includes or []
        self.modules = []
        self.aliases = {}
        self.exclude_dependent_files = {}
        self._modules = dict.fromkeys(
            excludes or []
        )  # type: Dict[str, Optional[Module]]
        self._builtin_modules = dict.fromkeys(sys.builtin_module_names)
        self._bad_modules = {}
        cx_Freeze.hooks.initialize(self)
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
        self.IncludeModule("unicodedata")
        self.IncludePackage("encodings")
        self.IncludeModule("io")
        self.IncludeModule("os")
        self.IncludeModule("sys")
        self.IncludeModule("zlib")
        self.IncludeModule("collections.abc")
        self.IncludeModule("importlib.abc")

    def _AddModule(self, name, path=None, file_name=None, parent=None):
        """Add a module to the list of modules but if one is already found,
        then return it instead; this is done so that packages can be
        handled properly."""
        module = self._modules.get(name)
        if module is None:
            module = Module(name, path, file_name, parent)
            self._modules[name] = module
            self.modules.append(module)
            if name in self._bad_modules:
                logging.debug(
                    "Removing module [%s] from list of bad modules", name
                )
                del self._bad_modules[name]
            if (
                self.zip_include_all_packages
                and module.name not in self.zip_exclude_packages
                or module.name in self.zip_include_packages
            ):
                module.store_in_file_system = False
        if module.path is None and path is not None:
            module.path = path
        if module.file is None and file_name is not None:
            module.file = file_name
        return module

    def _DetermineParent(self, caller):
        """Determine the parent to use when searching packages."""
        if caller is not None:
            if caller.path is not None:
                return caller
            return self._GetParentByName(caller.name)
        return None

    def _EnsureFromList(
        self, caller, packageModule, fromList, deferredImports
    ):
        """Ensure that the from list is satisfied. This is only necessary for
        package modules. If the package module has not been completely
        imported yet, defer the import until it has been completely imported
        in order to avoid spurious errors about missing modules."""
        if packageModule.in_import and caller is not packageModule:
            deferredImports.append((caller, packageModule, fromList))
        else:
            for name in fromList:
                if name in packageModule.global_names:
                    continue
                subModuleName = f"{packageModule.name}.{name}"
                self._ImportModule(subModuleName, deferredImports, caller)

    def _GetParentByName(self, name):
        """Return the parent module given the name of a module."""
        pos = name.rfind(".")
        if pos > 0:
            parentName = name[:pos]
            return self._modules[parentName]
        return None

    def _ImportAllSubModules(self, module, deferredImports, recursive=True):
        """Import all sub modules to the given package."""
        suffixes = importlib.machinery.all_suffixes()

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
                            name = fileName[: -len(suffix)]

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

                subModuleName = f"{module.name}.{name}"
                subModule = self._InternalImportModule(
                    subModuleName, deferredImports
                )
                if subModule is None:
                    if subModuleName not in self.excludes:
                        raise ImportError(f"No module named {subModuleName!r}")
                else:
                    module.global_names.add(name)
                    if subModule.path and recursive:
                        self._ImportAllSubModules(
                            subModule, deferredImports, recursive
                        )

    def _ImportDeferredImports(self, deferredImports, skipInImport=False):
        """Import any sub modules that were deferred, if applicable."""
        while deferredImports:
            newDeferredImports = []
            for caller, packageModule, subModuleNames in deferredImports:
                if packageModule.in_import and skipInImport:
                    continue
                self._EnsureFromList(
                    caller, packageModule, subModuleNames, newDeferredImports
                )
            deferredImports = newDeferredImports
            skipInImport = True

    def _ImportModule(
        self, name, deferredImports, caller=None, relativeImportIndex=0
    ):
        """Attempt to find the named module and return it or None if no module
        by that name could be found."""

        # absolute import (available in Python 2.5 and up)
        # the name given is the only name that will be searched
        if relativeImportIndex == 0:
            module = self._InternalImportModule(name, deferredImports)

        # old style relative import (regular 'import foo' in Python 2)
        # the name given is tried in the current package, and if
        # no match is found, sys.path is searched for a top-level module/pockage
        elif relativeImportIndex < 0:
            parent = self._DetermineParent(caller)
            if parent is not None:
                fullName = f"{parent.name}.{name}"
                module = self._InternalImportModule(fullName, deferredImports)
                if module is not None:
                    parent.global_names.add(name)
                    return module

            module = self._InternalImportModule(name, deferredImports)

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
                name = f"{parent.name}.{name}"
                module = self._InternalImportModule(name, deferredImports)

        # if module not found, track that fact
        if module is None:
            if caller is None:
                raise ImportError(f"No module named {name!r}")
            self._RunHook("missing", name, caller)
            if name not in caller.ignore_names:
                callers = self._bad_modules.setdefault(name, {})
                callers[caller.name] = None

        return module

    def _InternalImportModule(self, name, deferredImports):
        """Internal method used for importing a module which assumes that the
        name given is an absolute name. None is returned if the module
        cannot be found."""
        try:
            # Check in module cache before trying to import it again.
            return self._modules[name]
        except KeyError:
            pass

        if name in self._builtin_modules:
            module = self._AddModule(name)
            logging.debug("Adding module [%s] [C_BUILTIN]", name)
            self._RunHook("load", module.name, module)
            module.in_import = False
            return module

        pos = name.rfind(".")
        if pos < 0:  # Top-level module
            path = self.path
            parentModule = None
        else:  # Dotted module name - look up the parent module
            parentName = name[:pos]
            parentModule = self._InternalImportModule(
                parentName, deferredImports
            )
            if parentModule is None:
                return None
            path = parentModule.path

        if name in self.aliases:
            actualName = self.aliases[name]
            module = self._InternalImportModule(actualName, deferredImports)
            self._modules[name] = module
            return module

        try:
            module = self._load_module(
                name, path, deferredImports, parentModule
            )
        except ImportError:
            logging.debug("Module [%s] cannot be imported", name)
            self._modules[name] = None
            return None
        return module

    def _load_module(
        self,
        name: str,
        path: Union[str, List[str]],
        deferredImports: List[str],
        parent: Optional["Module"] = None,
    ) -> Optional["Module"]:
        """Load the module, searching the module spec."""
        spec: Optional[importlib.machinery.ModuleSpec]
        loader: ExecutionLoader
        module: "Module"

        if isinstance(path, str):
            # Include file as module
            module = self._AddModule(name, file_name=path, parent=parent)
            ext = os.path.splitext(os.path.basename(path))[1]
            if ext in importlib.machinery.SOURCE_SUFFIXES:
                loader = importlib.machinery.SourceFileLoader(name, path)
            elif ext in importlib.machinery.BYTECODE_SUFFIXES:
                loader = importlib.machinery.SourcelessFileLoader(name, path)
            else:
                raise ImportError(f"No module named {name!r}", name=name)
        else:
            # Find modules to load
            try:
                # It's recommended to clear the caches first.
                importlib.machinery.PathFinder.invalidate_caches()
                spec = importlib.machinery.PathFinder.find_spec(name, path)
            except Exception:
                spec = None
            if spec is None:
                return None
            # Handle special cases
            loader = spec.loader
            if loader is importlib.machinery.BuiltinImporter:
                return None
            if loader is importlib.machinery.FrozenImporter:
                return None
            # Load package or namespae package
            if spec.submodule_search_locations:
                path_list = list(spec.submodule_search_locations)
                module = self._AddModule(name, path=path_list, parent=parent)
                if spec.origin in (None, "namespace"):
                    logging.debug("Adding module [%s] [NAMESPACE]", name)
                    path = os.path.join(path_list[0], "__init__.py")
                    module.code = compile("", path, "exec")
                    return module
                else:
                    logging.debug("Adding module [%s] [PACKAGE]", name)
                    path = spec.origin  # path of __init__
                    module.file = path
            else:
                path = spec.origin
                module = self._AddModule(name, file_name=path, parent=parent)

        if isinstance(loader, importlib.machinery.SourceFileLoader):
            logging.debug("Adding module [%s] [SOURCE]", name)
            # Load & compile Python source code
            source_bytes = loader.get_data(path)
            try:
                module.code = loader.source_to_code(
                    source_bytes, path, _optimize=self.optimizeFlag
                )
            except SyntaxError:
                logging.debug("Invalid syntax in [%s]", name)
                raise ImportError(f"Invalid syntax in {path}", name=name)
        elif isinstance(loader, importlib.machinery.SourcelessFileLoader):
            logging.debug("Adding module [%s] [BYTECODE]", name)
            # Load Python bytecode
            module.code = loader.get_code(name)
            if module.code is None:
                raise ImportError(f"Bad magic number in {path}", name=name)
        elif isinstance(loader, importlib.machinery.ExtensionFileLoader):
            logging.debug("Adding module [%s] [EXTENSION]", name)
        else:
            raise ImportError(f"Unknown module loader in {path}", name=name)

        # If there's a custom hook for this module, run it.
        self._RunHook("load", module.name, module)

        if module.code is not None:
            if self.replace_paths:
                topLevelModule = module
                while topLevelModule.parent is not None:
                    topLevelModule = topLevelModule.parent
                module.code = self._ReplacePathsInCode(
                    topLevelModule, module.code
                )

            # Scan the module code for import statements
            self._ScanCode(module.code, module, deferredImports)

            # Verify __package__ in use
            self._ReplacePackageInCode(module)

        module.in_import = False
        return module

    def _ReplacePackageInCode(self, module):
        """Replace the value of __package__ directly in the code,
        only in zipped modules."""
        co = module.code
        if (
            co is None
            or module.parent is None
            or module.in_file_system
            or "__package__" in module.global_names
        ):
            # In some modules, like 'six' the variable is defined, so...
            return
        # Only if the code references it.
        if "__package__" in co.co_names:
            # Insert a bytecode to represent the code:
            # __package__ = module.parent.name
            constants = list(co.co_consts)
            pkg_const_index = len(constants)
            pkg_name_index = co.co_names.index("__package__")
            if pkg_const_index > 255 or pkg_name_index > 255:
                # Don't touch modules with many constants or names;
                # This is good for now.
                return
            # The bytecode/wordcode
            codes = [LOAD_CONST, pkg_const_index, STORE_NAME, pkg_name_index]
            codestring = bytes(codes) + co.co_code
            constants.append(module.parent.name)
            code = rebuild_code_object(
                co, codestring=codestring, constants=constants
            )
            module.code = code

    def _ReplacePathsInCode(self, topLevelModule, co):
        """Replace paths in the code as directed, returning a new code object
        with the modified paths in place."""
        # Prepare the new filename.
        origFileName = newFileName = os.path.normpath(co.co_filename)
        for searchValue, replaceValue in self.replace_paths:
            if searchValue == "*":
                if topLevelModule.file is None:
                    continue
                searchValue = os.path.dirname(topLevelModule.file)
                if topLevelModule.path:
                    searchValue = os.path.dirname(searchValue)
                if searchValue:
                    searchValue = searchValue + os.path.sep
            if not origFileName.startswith(searchValue):
                continue
            newFileName = replaceValue + origFileName[len(searchValue) :]
            break

        # Run on subordinate code objects from function & class definitions.
        constants = list(co.co_consts)
        for i, value in enumerate(constants):
            if isinstance(value, type(co)):
                constants[i] = self._ReplacePathsInCode(topLevelModule, value)

        return rebuild_code_object(
            co, constants=constants, filename=newFileName
        )

    def _RunHook(self, hookName, moduleName, *args):
        """Run hook for the given module if one is present."""
        name = "{}_{}".format(hookName, moduleName.replace(".", "_"))
        method = getattr(cx_Freeze.hooks, name, None)
        if method is not None:
            method(self, *args)

    def _ScanCode(self, co, module: "Module", deferredImports, topLevel=True):
        """Scan code, looking for imported modules and keeping track of the
        constants that have been created in order to better tell which
        modules are truly missing."""
        arguments = []
        importedModule = None
        for opIndex, op, opArg in dis._unpack_opargs(co.co_code):

            # keep track of constants (these are used for importing)
            # immediately restart loop so arguments are retained
            if op == LOAD_CONST:
                arguments.append(co.co_consts[opArg])
                continue

            # import statement: attempt to import module
            if op == IMPORT_NAME:
                name = co.co_names[opArg]
                if len(arguments) >= 2:
                    relativeImportIndex, fromList = arguments[-2:]
                else:
                    relativeImportIndex = -1
                    fromList = arguments[0] if arguments else []
                if name not in module.exclude_names:
                    importedModule = self._ImportModule(
                        name, deferredImports, module, relativeImportIndex
                    )
                    if importedModule is not None:
                        if (
                            fromList
                            and fromList != ("*",)
                            and importedModule.path is not None
                        ):
                            self._EnsureFromList(
                                module,
                                importedModule,
                                fromList,
                                deferredImports,
                            )

            # import * statement: copy all global names
            elif op == IMPORT_STAR and topLevel and importedModule is not None:
                module.global_names.update(importedModule.global_names)

            # store operation: track only top level
            elif topLevel and op in STORE_OPS:
                name = co.co_names[opArg]
                module.global_names.add(name)

            # reset arguments; these are only needed for import statements so
            # ignore them in all other cases!
            arguments = []

        # Scan the code objects from function & class definitions
        for constant in co.co_consts:
            if isinstance(constant, type(co)):
                self._ScanCode(
                    constant, module, deferredImports, topLevel=False
                )

    def AddAlias(self, name, aliasFor):
        """Add an alias for a particular module; when an attempt is made to
        import a module using the alias name, import the actual name
        instead."""
        self.aliases[name] = aliasFor

    def AddConstant(self, name, value):
        self.constants_module.values[name] = value

    def ExcludeDependentFiles(self, fileName):
        self.exclude_dependent_files[fileName] = None

    def ExcludeModule(self, name):
        """Exclude the named module from the resulting frozen executable."""
        self.excludes[name] = None
        self._modules[name] = None

    def IncludeFile(self, path: str, name: Optional[str] = None) -> "Module":
        """Include the named file as a module in the frozen executable."""
        if name is None:
            name = os.path.splitext(os.path.basename(path))[0]
        deferredImports = []
        module = self._load_module(name, path, deferredImports)
        self._ImportDeferredImports(deferredImports)
        return module

    def IncludeFiles(self, sourcePath, targetPath, copyDependentFiles=True):
        """Include the files in the given directory in the target build."""
        self.include_files.append((sourcePath, targetPath))
        if not copyDependentFiles:
            self.ExcludeDependentFiles(sourcePath)

    def IncludeModule(self, name):
        """Include the named module in the frozen executable."""
        deferredImports = []
        module = self._ImportModule(name, deferredImports)
        self._ImportDeferredImports(deferredImports, skipInImport=True)
        return module

    def IncludePackage(self, name):
        """Include the named package and any submodules in the frozen
        executable."""
        deferredImports = []
        module = self._ImportModule(name, deferredImports)
        if module.path:
            self._ImportAllSubModules(module, deferredImports)
        self._ImportDeferredImports(deferredImports, skipInImport=True)
        return module

    def ReportMissingModules(self):
        """Display a list of modules that weren't found."""
        if self._bad_modules:
            print("Missing modules:")
            names = list(self._bad_modules.keys())
            names.sort()
            for name in names:
                callers = list(self._bad_modules[name].keys())
                callers.sort()
                print("? {} imported from {}".format(name, ", ".join(callers)))
            print(
                "This is not necessarily a problem - the modules "
                "may not be needed on this platform.\n"
            )

    def SetOptimizeFlag(self, optimizeFlag):
        """Set a new value of optimize flag and returns the previous value."""
        previous = self.optimizeFlag
        # The value of optimizeFlag is propagated according to the user's
        # choice and checked in dist.py or main,py. This value is unlikely
        # to be wrong, yet we check and ignore any divergent value.
        if -1 <= optimizeFlag <= 2:
            self.optimizeFlag = optimizeFlag
        return previous

    def ZipIncludeFiles(self, sourcePath, targetPath):
        """Include the file(s) in the library.zip"""
        self.zip_includes.append((sourcePath, targetPath))


class Module:
    def __init__(self, name, path=None, file_name=None, parent=None):
        self.name = name
        self.file = file_name
        self.path = path
        self.code = None
        self.parent = parent
        self.global_names = set()
        self.exclude_names = set()
        self.ignore_names = set()
        self.source_is_zip_file = False
        self.in_import = True
        self.store_in_file_system = True
        # distribution files (metadata)
        dist_files = []
        packages = [name]
        try:
            requires = importlib_metadata.requires(packages[0])
        except importlib_metadata.PackageNotFoundError:
            requires = None
        if requires is not None:
            packages += [req.partition(" ")[0] for req in requires]
        for package_name in packages:
            try:
                files = importlib_metadata.files(package_name)
            except importlib_metadata.PackageNotFoundError:
                files = None
            if files is not None:
                # cache file names to use in write modules
                for file in files:
                    if not file.match("*.dist-info/*"):
                        continue
                    dist_path = str(file.locate())
                    arc_path = file.as_posix()
                    dist_files.append((dist_path, arc_path))
        self.dist_files = dist_files

    def __repr__(self):
        parts = ["name=%s" % repr(self.name)]
        if self.file is not None:
            parts.append("file=%s" % repr(self.file))
        if self.path is not None:
            parts.append("path=%s" % repr(self.path))
        return "<Module %s>" % ", ".join(parts)

    def AddGlobalName(self, name):
        self.global_names.add(name)

    def ExcludeName(self, name):
        self.exclude_names.add(name)

    def IgnoreName(self, name):
        self.ignore_names.add(name)

    @property
    def in_file_system(self):
        if self.parent is not None:
            return self.parent.in_file_system
        if self.path is None or self.file is None:
            return False
        return self.store_in_file_system
