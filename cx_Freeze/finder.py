"""Module Finder - discovers what modules are required by the code."""

import importlib.machinery
import logging
import os
import sys
from contextlib import suppress
from importlib.abc import ExecutionLoader
from pathlib import Path, PurePath
from sysconfig import get_config_var
from types import CodeType
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

import opcode

from ._compat import cached_property
from .common import (
    IncludesList,
    InternalIncludesList,
    code_object_replace,
    get_resource_file_path,
    process_path_specs,
)
from .module import ConstantsModule, Module

BUILD_LIST = opcode.opmap["BUILD_LIST"]
EXTENDED_ARG = opcode.opmap["EXTENDED_ARG"]
LOAD_CONST = opcode.opmap["LOAD_CONST"]
IMPORT_NAME = opcode.opmap["IMPORT_NAME"]
IMPORT_FROM = opcode.opmap["IMPORT_FROM"]
IMPORT_STAR = opcode.opmap["IMPORT_STAR"]
STORE_FAST = opcode.opmap["STORE_FAST"]
STORE_NAME = opcode.opmap["STORE_NAME"]
STORE_GLOBAL = opcode.opmap["STORE_GLOBAL"]
STORE_OPS = (STORE_NAME, STORE_GLOBAL)
HAVE_ARGUMENT = opcode.HAVE_ARGUMENT


DeferredList = List[Tuple[Module, Module, List[str]]]

__all__ = ["Module", "ModuleFinder"]


class ModuleFinder:
    """ModuleFinder base class."""

    def __init__(
        self,
        include_files: Optional[IncludesList] = None,
        excludes: Optional[List[str]] = None,
        path: Optional[List[str]] = None,
        replace_paths: Optional[List[Tuple[str, str]]] = None,
        zip_include_all_packages: bool = False,
        zip_exclude_packages: Optional[List[str]] = None,
        zip_include_packages: Optional[List[str]] = None,
        constants_module: Optional[ConstantsModule] = None,
        zip_includes: Optional[IncludesList] = None,
    ):
        self.included_files: InternalIncludesList = process_path_specs(
            include_files
        )
        self.excludes: Dict[str, Any] = dict.fromkeys(excludes or [])
        self.optimize_flag = 0
        self.path: List[str] = self._set_path(path)
        self.replace_paths = replace_paths or []
        self.zip_include_all_packages = zip_include_all_packages
        self.zip_exclude_packages = zip_exclude_packages or []
        self.zip_include_packages = zip_include_packages or []
        self.constants_module = constants_module
        self.zip_includes: InternalIncludesList = process_path_specs(
            zip_includes
        )
        self.modules = []
        self.aliases = {}
        self.excluded_dependent_files: Set[Path] = set()
        self._modules: Dict[str, Optional[Module]] = dict.fromkeys(
            excludes or []
        )
        self._bad_modules = {}
        for name in self._base_hooks.exclude.MODULES:
            self.exclude_module(name)
        self._add_base_modules()

    def _add_base_modules(self) -> None:
        """
        Add the base modules to the finder. These are the modules that
        Python imports itself during initialization and, if not found,
        can result in behavior that differs from running from source;
        also include modules used within the bootstrap code.

        When cx_Freeze is built, these modules (and modules they load) are
        included in the startup zip file.
        """
        self.include_module("traceback")
        self.include_module("warnings")
        self.include_module("unicodedata")
        self.include_package("encodings")
        self.include_module("io")
        self.include_module("os")
        self.include_module("sys")
        self.include_module("zlib")
        self.include_module("collections.abc")
        self.include_module("importlib.abc")

    def _add_module(
        self,
        name: str,
        path: Optional[Sequence[Union[Path, str]]] = None,
        file_name: Optional[Union[Path, str]] = None,
        parent: Optional[Module] = None,
    ) -> Module:
        """
        Add a module to the list of modules but if one is already found,
        then return it instead; this is done so that packages can be
        handled properly.
        """
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
                module.in_file_system = 0
        if module.path is None and path is not None:
            module.path = [Path(p) for p in path]
        if module.file is None and file_name is not None:
            module.file = file_name
        return module

    def _determine_parent(self, caller: Optional[Module]) -> Optional[Module]:
        """Determine the parent to use when searching packages."""
        if caller is not None:
            if caller.path is not None:
                return caller
            return self._get_parent_by_name(caller.name)
        return None

    @cached_property
    def _base_hooks(self):
        """Load the hooks dynamically to avoid cyclic errors, because hooks
        have references to finder."""
        hooks = get_resource_file_path("hooks", "__init__", ".py")
        fromlist = []
        # add python files (modules)
        for path in hooks.parent.glob("*.py"):
            fromlist.append("hooks" if path.stem == "__init__" else path.stem)
        # add directories (subpackages)
        for path in hooks.parent.glob("*/__init__.py"):
            fromlist.append(path.parent.stem)
        return __import__("cx_Freeze.hooks", fromlist=fromlist)

    @cached_property
    def _builtin_modules(self) -> Set[str]:
        """The built-in modules are determined based on the cx_Freeze build."""
        builtin_modules: Set[str] = set(sys.builtin_module_names)
        dynload = get_resource_file_path("bases", "lib-dynload", "")
        if dynload and dynload.is_dir():
            # discard modules that exist in bases/lib-dynload
            for file in dynload.iterdir():
                builtin_modules.discard(file.name.partition(".")[0])
        return builtin_modules

    def _ensure_from_list(
        self,
        caller: Module,
        package_module: Module,
        from_list: List[str],
        deferred_imports: DeferredList,
    ) -> None:
        """
        Ensure that the from list is satisfied. This is only necessary for
        package modules. If the package module has not been completely
        imported yet, defer the import until it has been completely imported
        in order to avoid spurious errors about missing modules.
        """
        if package_module.in_import and caller is not package_module:
            deferred_imports.append((caller, package_module, from_list))
        else:
            for name in from_list:
                if name in package_module.global_names:
                    continue
                sub_module_name = f"{package_module.name}.{name}"
                self._import_module(sub_module_name, deferred_imports, caller)

    def _get_parent_by_name(self, name: str) -> Optional[Module]:
        """Return the parent module given the name of a module."""
        pos = name.rfind(".")
        if pos > 0:
            parent_name = name[:pos]
            return self._modules[parent_name]
        return None

    def _import_all_sub_modules(
        self,
        module: Module,
        deferred_imports: DeferredList,
        recursive: bool = True,
    ):
        """Import all sub modules to the given package."""
        suffixes = importlib.machinery.all_suffixes()

        for path in module.path:
            for fullname in path.iterdir():
                if fullname.is_dir():
                    if not fullname.joinpath("__init__.py").exists():
                        continue
                    name = fullname.name
                else:
                    # We need to run through these in order to correctly pick
                    # up PEP 3149 library names
                    # (e.g. .cpython-39-x86_64-linux-gnu.so).
                    for suffix in suffixes:
                        if fullname.name.endswith(suffix):
                            name = fullname.name[: -len(suffix)]

                            # Skip modules whose names appear to contain '.',
                            # as we may be using the wrong suffix, and even if
                            # we're not, such module names will break the
                            # import code.
                            if "." not in name:
                                break

                    else:
                        continue
                    if name == "__init__":
                        continue

                sub_module_name = f"{module.name}.{name}"
                sub_module = self._internal_import_module(
                    sub_module_name, deferred_imports
                )
                if sub_module is None:
                    if sub_module_name not in self.excludes:
                        raise ImportError(
                            f"No module named {sub_module_name!r}"
                        )
                else:
                    module.global_names.add(name)
                    if sub_module.path and recursive:
                        self._import_all_sub_modules(
                            sub_module, deferred_imports, recursive
                        )

    def _import_deferred_imports(
        self, deferred_imports: DeferredList, skip_in_import: bool = False
    ):
        """Import any sub modules that were deferred, if applicable."""
        while deferred_imports:
            new_deferred_imports: DeferredList = []
            for caller, package_module, sub_module_names in deferred_imports:
                if package_module.in_import and skip_in_import:
                    continue
                self._ensure_from_list(
                    caller,
                    package_module,
                    sub_module_names,
                    new_deferred_imports,
                )
            deferred_imports = new_deferred_imports
            skip_in_import = True

    def _import_module(
        self,
        name: str,
        deferred_imports: DeferredList,
        caller: Optional[Module] = None,
        relative_import_index: int = 0,
    ):
        """
        Attempt to find the named module and return it or None if no module
        by that name could be found.
        """

        # absolute import (available in Python 2.5 and up)
        # the name given is the only name that will be searched
        if relative_import_index == 0:
            module = self._internal_import_module(name, deferred_imports)

        # old style relative import (regular 'import foo' in Python 2)
        # the name given is tried in the current package, and if no match
        # is found, sys.path is searched for a top-level module/pockage
        elif relative_import_index < 0:
            parent = self._determine_parent(caller)
            if parent is not None:
                fullname = f"{parent.name}.{name}"
                module = self._internal_import_module(
                    fullname, deferred_imports
                )
                if module is not None:
                    parent.global_names.add(name)
                    return module

            module = self._internal_import_module(name, deferred_imports)

        # new style relative import (available in Python 2.5 and up)
        # the index indicates how many levels to traverse and only that level
        # is searched for the named module
        elif relative_import_index > 0:
            parent = caller
            if parent.path is not None:
                relative_import_index -= 1
            while parent is not None and relative_import_index > 0:
                parent = self._get_parent_by_name(parent.name)
                relative_import_index -= 1
            if parent is None:
                module = None
            elif not name:
                module = parent
            else:
                name = f"{parent.name}.{name}"
                module = self._internal_import_module(name, deferred_imports)

        # if module not found, track that fact
        if module is None:
            if caller is None:
                raise ImportError(f"No module named {name!r}")
            self._run_hook("missing", name, caller)
            if name not in caller.ignore_names:
                callers = self._bad_modules.setdefault(name, {})
                callers[caller.name] = None

        return module

    def _internal_import_module(
        self, name: str, deferred_imports: DeferredList
    ) -> Optional[Module]:
        """
        Internal method used for importing a module which assumes that the
        name given is an absolute name. None is returned if the module
        cannot be found.
        """
        with suppress(KeyError):
            # Check in module cache before trying to import it again.
            return self._modules[name]

        if name in self._builtin_modules:
            module = self._add_module(name)
            logging.debug("Adding module [%s] [C_BUILTIN]", name)
            self._run_hook("load", module.name, module)
            module.in_import = False
            return module

        pos = name.rfind(".")
        if pos < 0:  # Top-level module
            path = self.path
            parent_module = None
        else:  # Dotted module name - look up the parent module
            parent_name = name[:pos]
            parent_module = self._internal_import_module(
                parent_name, deferred_imports
            )
            if parent_module is None:
                return None
            path = parent_module.path
            if path is None:
                path = self.path
            else:
                path = list(map(os.fspath, path))

        if name in self.aliases:
            actual_name = self.aliases[name]
            module = self._internal_import_module(
                actual_name, deferred_imports
            )
            self._modules[name] = module
            return module

        try:
            module = self._load_module(
                name, path, deferred_imports, parent_module
            )
        except ImportError:
            logging.debug("Module [%s] cannot be imported", name)
            self._modules[name] = None
            return None
        return module

    def _load_module(
        self,
        name: str,
        path: Optional[Sequence[str]],
        deferred_imports: DeferredList,
        parent: Optional[Module] = None,
    ) -> Optional[Module]:
        """Load the module, searching the module spec."""
        spec: Optional[importlib.machinery.ModuleSpec] = None
        loader: Optional[ExecutionLoader] = None
        module: Optional[Module] = None

        # Find modules to load
        try:
            # It's recommended to clear the caches first.
            importlib.machinery.PathFinder.invalidate_caches()
            spec = importlib.machinery.PathFinder.find_spec(name, path)
        except KeyError:
            if parent:
                # some packages use a directory with vendored modules
                # without an __init__.py and are not considered namespace
                # packages, then simulate a subpackage
                module = self._add_module(
                    name,
                    path=[Path(path[0], name.rpartition(".")[-1])],
                    parent=parent,
                )
                logging.debug("Adding module [%s] [PACKAGE]", name)
                module.file = Path(path[0], "__init__.py")
                module.source_is_string = True

        if spec:
            loader = spec.loader
            # Ignore built-in importers
            if loader is importlib.machinery.BuiltinImporter:
                return None
            if loader is importlib.machinery.FrozenImporter:
                return None
            # Load package or namespace package
            if spec.submodule_search_locations:
                module = self._add_module(
                    name,
                    path=list(spec.submodule_search_locations),
                    parent=parent,
                )
                if spec.origin in (None, "namespace"):
                    logging.debug("Adding module [%s] [NAMESPACE]", name)
                    module.file = module.path[0] / "__init__.py"
                    module.source_is_string = True
                else:
                    logging.debug("Adding module [%s] [PACKAGE]", name)
                    module.file = spec.origin  # path of __init__.py
            else:
                module = self._add_module(
                    name, file_name=spec.origin, parent=parent
                )

        if module is not None:
            self._load_module_code(module, loader, deferred_imports)
        return module

    def _load_module_code(
        self,
        module: Module,
        loader: Optional[ExecutionLoader],
        deferred_imports: DeferredList,
    ) -> Optional[Module]:
        name = module.name
        path = os.fspath(module.file)

        if isinstance(loader, importlib.machinery.SourceFileLoader):
            logging.debug("Adding module [%s] [SOURCE]", name)
            # Load & compile Python source code
            source_bytes = loader.get_data(path)
            try:
                module.code = loader.source_to_code(
                    source_bytes, path, _optimize=self.optimize_flag
                )
            except SyntaxError:
                logging.debug("Invalid syntax in [%s]", name)
                raise ImportError(
                    f"Invalid syntax in {path}", name=name
                ) from None
        elif isinstance(loader, importlib.machinery.SourcelessFileLoader):
            logging.debug("Adding module [%s] [BYTECODE]", name)
            # Load Python bytecode
            module.code = loader.get_code(name)
            if module.code is None:
                raise ImportError(f"Bad magic number in {path}", name=name)
        elif isinstance(loader, importlib.machinery.ExtensionFileLoader):
            logging.debug("Adding module [%s] [EXTENSION]", name)
        elif module.source_is_string:
            module.code = compile("", path, "exec")
        else:
            raise ImportError(f"Unknown module loader in {path}", name=name)

        # If there's a custom hook for this module, run it.
        self._run_hook("load", module.name, module)

        if module.code is not None:
            if self.replace_paths:
                module.code = self._replace_paths_in_code(module)

            # Scan the module code for import statements
            self._scan_code(module.code, module, deferred_imports)

            # Verify __package__ in use
            module.code = self._replace_package_in_code(module)

        module.in_import = False
        return module

    def _load_module_from_file(
        self, name: str, filename: Path, deferred_imports: DeferredList
    ) -> Optional[Module]:
        """Load the module from the filename."""
        loader: Optional[ExecutionLoader] = None

        ext = filename.suffix
        path = os.fspath(filename)
        if ext == "" or ext in importlib.machinery.SOURCE_SUFFIXES:
            loader = importlib.machinery.SourceFileLoader(name, path)
        elif ext in importlib.machinery.BYTECODE_SUFFIXES:
            loader = importlib.machinery.SourcelessFileLoader(name, path)
        elif ext in importlib.machinery.EXTENSION_SUFFIXES:
            loader = importlib.machinery.ExtensionFileLoader(name, path)

        module = self._add_module(name, file_name=filename)
        self._load_module_code(module, loader, deferred_imports)
        return module

    @staticmethod
    def _replace_package_in_code(module: Module) -> CodeType:
        """
        Replace the value of __package__ directly in the code,
        when the module is in a package and will be stored in library.zip.
        """
        code = module.code
        # Check if module is in a package and will be stored in library.zip
        # and is not defined in the module, like 'six' do
        if (
            module.parent is None
            or module.in_file_system >= 1
            or "__package__" in module.global_names
            or code is None
        ):
            return code
        # Only if the code references it.
        if "__package__" in code.co_names:
            consts = list(code.co_consts)
            pkg_const_index = len(consts)
            pkg_name_index = code.co_names.index("__package__")
            if pkg_const_index > 255 or pkg_name_index > 255:
                # Don't touch modules with many constants or names;
                # This is good for now.
                return code
            # Insert a bytecode to represent the code:
            # __package__ = module.parent.name
            codes = [LOAD_CONST, pkg_const_index, STORE_NAME, pkg_name_index]
            codestring = bytes(codes) + code.co_code
            consts.append(module.parent.name)
            code = code_object_replace(
                code, co_code=codestring, co_consts=consts
            )
        return code

    def _replace_paths_in_code(
        self, module: Module, code: Optional[CodeType] = None
    ) -> CodeType:
        """
        Replace paths in the code as directed, returning a new code object
        with the modified paths in place.
        """
        top_level_module = module  # type: Module
        while top_level_module.parent is not None:
            top_level_module = top_level_module.parent
        if code is None:
            code = module.code
        # Prepare the new filename.
        original_filename = Path(code.co_filename)
        for search_value, replace_value in self.replace_paths:
            if search_value == "*":
                if top_level_module.file is None:
                    continue
                if top_level_module.path:
                    search_dir = top_level_module.file.parent.parent
                else:
                    search_dir = top_level_module.file.parent
            else:
                search_dir = Path(search_value)
            with suppress(ValueError):
                new_filename = original_filename.relative_to(search_dir)
                new_filename = replace_value / new_filename
                break
        else:
            new_filename = original_filename

        # Run on subordinate code objects from function & class definitions.
        consts = list(code.co_consts)
        for i, const in enumerate(consts):
            if isinstance(const, type(code)):
                consts[i] = self._replace_paths_in_code(
                    top_level_module, const
                )

        return code_object_replace(
            code, co_consts=consts, co_filename=os.fspath(new_filename)
        )

    def _run_hook(self, hook: str, module_name: str, *args) -> None:
        """Run hook (load or missing) for the given module if one is present.
        For functions present in hooks.__init__:
        package aiofiles -> load_aiofiles function
        For functions in a separated module (lowercased):
        package PyQt5, module QtCore -> pyqt5.load_pyqt5_qtcore
        """
        base_hooks = self._base_hooks
        normalized_name = module_name.replace(".", "_")
        method = getattr(base_hooks, f"{hook}_{normalized_name}", None)
        if method is None:
            root = module_name.split(".")[0].lower()
            base_hooks = getattr(base_hooks, root, None)
            if base_hooks is not None:
                normalized_name = normalized_name.lower()
                method = getattr(base_hooks, f"{hook}_{normalized_name}", None)
        if method is not None:
            method(self, *args)

    @staticmethod
    def _set_path(path: Optional[List[str]] = None) -> Set[str]:
        """Set the path to search for modules, and fix the path for built-in
        modules when it differs from the running python built-in modules."""
        path = path or sys.path
        if path == sys.path:
            dynload = get_resource_file_path("bases", "lib-dynload", "")
            if dynload and dynload.is_dir():
                # add bases/lib-dynload to the finder path
                insert_at = 0
                dest_shared = get_config_var("DESTSHARED")
                if dest_shared:
                    for i, pth in enumerate(path):
                        if pth == dest_shared:
                            insert_at = i
                            break
                path = path.copy()
                path.insert(insert_at, os.fspath(dynload))
        return path

    def _scan_code(
        self,
        code,
        module: Module,
        deferred_imports: DeferredList,
        top_level: bool = True,
    ):
        """Scan code, looking for imported modules and keeping track of the
        constants that have been created in order to better tell which
        modules are truly missing."""
        arguments = []
        imported_module = None
        co_code = code.co_code
        extended_arg = 0
        for i in range(0, len(co_code), 2):
            opc = co_code[i]
            if opc >= HAVE_ARGUMENT:
                arg = co_code[i + 1] | extended_arg
                extended_arg = (arg << 8) if opc == EXTENDED_ARG else 0
            else:
                arg = None
                extended_arg = 0

            # keep track of constants (these are used for importing)
            # immediately restart loop so arguments are retained
            if opc == LOAD_CONST:
                arguments.append(code.co_consts[arg])
                continue

            # import statement: attempt to import module
            if opc == IMPORT_NAME:
                name = code.co_names[arg]
                if len(arguments) >= 2:
                    # pylint: disable-next=W0632
                    relative_import_index, from_list = arguments[-2:]
                else:
                    relative_import_index = -1
                    from_list = arguments[0] if arguments else []
                if name not in module.exclude_names:
                    imported_module = self._import_module(
                        name, deferred_imports, module, relative_import_index
                    )
                    if imported_module is not None:
                        if (
                            from_list
                            and from_list != ("*",)
                            and imported_module.path is not None
                        ):
                            self._ensure_from_list(
                                module,
                                imported_module,
                                from_list,
                                deferred_imports,
                            )

            # import * statement: copy all global names
            elif (
                opc == IMPORT_STAR
                and top_level
                and imported_module is not None
            ):
                module.global_names.update(imported_module.global_names)

            # store operation: track only top level
            elif top_level and opc in STORE_OPS:
                name = code.co_names[arg]
                module.global_names.add(name)

            # reset arguments; these are only needed for import statements so
            # ignore them in all other cases!
            arguments = []

        # Scan the code objects from function & class definitions
        for constant in code.co_consts:
            if isinstance(constant, type(code)):
                self._scan_code(
                    constant, module, deferred_imports, top_level=False
                )

    def add_alias(self, name: str, alias_for: str) -> None:
        """Add an alias for a particular module; when an attempt is made to
        import a module using the alias name, import the actual name instead.
        """
        self.aliases[name] = alias_for

    def add_constant(self, name: str, value: str) -> None:
        """Makes available a constant in the module BUILD_CONSTANTS which is
        used in the initscripts."""
        self.constants_module.values[name] = value

    def exclude_dependent_files(self, filename: Union[Path, str]) -> None:
        """Exclude the dependent files of the named file from the resulting
        frozen executable."""
        if not isinstance(filename, Path):
            filename = Path(filename)
        self.excluded_dependent_files.add(filename)

    def exclude_module(self, name: str) -> None:
        """Exclude the named module and its submodules from the resulting
        frozen executable."""
        modules_to_exclude = [name] + [
            mod for mod in self._modules if mod.startswith(f"{name}.")
        ]
        for mod in modules_to_exclude:
            self.excludes[mod] = None
            self._modules[mod] = None

    def include_file_as_module(
        self, path: Union[Path, str], name: Optional[str] = None
    ) -> Module:
        """Include the named file as a module in the frozen executable."""
        if isinstance(path, str):
            path = Path(path)
        if name is None:
            name = path.name.partition(".")[0]
        deferred_imports: DeferredList = []
        module = self._load_module_from_file(name, path, deferred_imports)
        if module is not None:
            parent = self._get_parent_by_name(name)
            if parent is not None:
                parent.global_names.add(module.name)
                module.parent = parent
        self._import_deferred_imports(deferred_imports)
        return module

    def include_files(
        self,
        source_path: Union[Path, str],
        target_path: Union[Path, str],
        copy_dependent_files: bool = True,
    ) -> None:
        """Include the files in the given directory in the target build."""
        self.included_files.extend(
            process_path_specs([(source_path, target_path)])
        )
        if not copy_dependent_files:
            self.exclude_dependent_files(source_path)

    def include_module(self, name: str) -> Module:
        """Include the named module in the frozen executable."""
        # includes has priority over excludes
        if name in self.excludes and name in self._modules:
            if self._modules[name] is None:
                self.excludes.pop(name)
                self._modules.pop(name)
        # include module
        deferred_imports: DeferredList = []
        module = self._import_module(name, deferred_imports)
        self._import_deferred_imports(deferred_imports, skip_in_import=True)
        return module

    def include_package(self, name: str) -> Module:
        """Include the named package and any submodules in the frozen
        executable."""
        deferred_imports: DeferredList = []
        module = self._import_module(name, deferred_imports)
        if module.path:
            self._import_all_sub_modules(module, deferred_imports)
        self._import_deferred_imports(deferred_imports, skip_in_import=True)
        return module

    def report_missing_modules(self) -> None:
        """Display a list of modules that weren't found."""
        if self._bad_modules:
            print("Missing modules:")
            names = list(self._bad_modules.keys())
            names.sort()
            for name in names:
                callers = list(self._bad_modules[name].keys())
                callers.sort()
                print(f"? {name} imported from", ", ".join(callers))
            print("This is not necessarily a problem - the modules ", end="")
            print("may not be needed on this platform.\n")

    @property
    def optimize_flag(self) -> int:
        """The value of optimize flag propagated according to the user's
        choice."""
        return self._optimize_flag

    @optimize_flag.setter
    def optimize_flag(self, value: int):
        # The value of optimize_flag is checked in dist.py or main,py. This
        # value is unlikely to be wrong, yet we check and ignore any divergent
        # value.
        if -1 <= value <= 2:
            self._optimize_flag = value

    def zip_include_files(
        self,
        source_path: Union[str, Path],
        target_path: Optional[Union[str, Path, PurePath]] = None,
    ) -> None:
        """Include files or all of the files in a directory to the zip file."""
        self.zip_includes.extend(
            process_path_specs([(source_path, target_path)])
        )
