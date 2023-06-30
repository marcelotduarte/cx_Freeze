"""Implements the 'build_exe' command."""

from __future__ import annotations

import logging
import os
import sys
from sysconfig import get_platform, get_python_version

from setuptools import Command

from ..common import normalize_to_list
from ..exception import SetupError
from ..freezer import Freezer
from ..module import ConstantsModule

__all__ = ["BuildEXE"]


class BuildEXE(Command):
    """Build executables from Python scripts."""

    description = "build executables from Python scripts"
    user_options = [
        (
            "build-exe=",
            "b",
            "directory for built executables and dependent files",
        ),
        (
            "optimize=",
            "O",
            'optimization level: -O1 for "python -O", '
            '-O2 for "python -OO" and -O0 to disable [default: -O0]',
        ),
        ("excludes=", "e", "comma-separated list of modules to exclude"),
        ("includes=", "i", "comma-separated list of modules to include"),
        (
            "packages=",
            "p",
            "comma-separated list of packages to include, "
            "which includes all submodules in the package",
        ),
        (
            "replace-paths=",
            None,
            "comma-separated list of paths to replace in included modules, "
            "using the form <search>=<replace>",
        ),
        (
            "path=",
            None,
            "comma-separated list of paths to search for modules; the default "
            "value is sys.path (use only if you know what you are doing)",
        ),
        ("no-compress", None, "create a zipfile with no compression"),
        ("constants=", None, "comma-separated list of constants to include"),
        (
            "bin-includes",
            None,
            "list of files to include when determining "
            "dependencies of binary files that would normally be excluded",
        ),
        (
            "bin-excludes",
            None,
            "list of files to exclude when determining "
            "dependencies of binary files that would normally be included",
        ),
        (
            "bin-path-includes",
            None,
            "list of paths from which to include files when determining "
            "dependencies of binary files",
        ),
        (
            "bin-path-excludes",
            None,
            "list of paths from which to exclude files when determining "
            "dependencies of binary files",
        ),
        (
            "include-files=",
            "f",
            "list of tuples of additional files to include in distribution",
        ),
        (
            "zip-includes=",
            None,
            "list of tuples of additional files to include in zip file",
        ),
        (
            "zip-include-packages=",
            None,
            "comma-separated list of packages to include in the zip file "
            "(or * for all) [default: none]",
        ),
        (
            "zip-exclude-packages=",
            None,
            "comma-separated list of packages to exclude from the zip file "
            "and place in the file system instead (or * for all) "
            "[default: *]",
        ),
        (
            "silent",
            "s",
            "suppress all output except warnings "
            "(equivalent to --silent-level=1)",
        ),
        (
            "silent-level=",
            None,
            "suppress output from build_exe command."
            " level 0: get all messages; [default]"
            " level 1: suppress information messages, but still get warnings;"
            " (equivalent to --silent)"
            " level 2: suppress missing missing-module warnings"
            " level 3: suppress all warning messages",
        ),
        (
            "include-msvcr=",
            None,
            "include the Microsoft Visual C runtime files",
        ),
    ]
    boolean_options = ["no-compress", "include_msvcr", "silent"]

    def add_to_path(self, name):
        source_dir = getattr(self, name.lower())
        if source_dir is not None:
            sys.path.insert(0, source_dir)

    def build_extension(self, name, module_name=None):
        # XXX: This method, add_to_path and set_source_location can be deleted?
        if module_name is None:
            module_name = name
        source_dir = getattr(self, name.lower())
        if source_dir is None:
            return None
        orig_dir = os.getcwd()
        script_args = ["build"]
        command = self.distribution.get_command_obj("build")
        if command.compiler is not None:
            script_args.append(f"--compiler={command.compiler}")
        os.chdir(source_dir)
        logging.info("building '%s' extension in '%s'", name, source_dir)
        distutils_core = __import__("distutils.core", fromlist=["run_setup"])
        distribution = distutils_core.run_setup("setup.py", script_args)
        ext_modules = distribution.ext_modules
        modules = [m for m in ext_modules if m.name == module_name]
        if not modules:
            raise SetupError(
                "no module named '{module_name}' in '{source_dir}'"
            )
        command = distribution.get_command_obj("build_ext")
        command.ensure_finalized()
        if command.compiler is None:
            command.run()
        else:
            command.build_extensions()
        dir_name = os.path.join(source_dir, command.build_lib)
        os.chdir(orig_dir)
        if dir_name not in sys.path:
            sys.path.insert(0, dir_name)
        return os.path.join(
            source_dir,
            command.build_lib,
            command.get_ext_filename(module_name),
        )

    def initialize_options(self):
        self.list_options = [
            "excludes",
            "includes",
            "packages",
            "replace_paths",
            "constants",
            "bin_excludes",
            "bin_includes",
            "bin_path_includes",
            "bin_path_excludes",
            "include_files",
            "zip_includes",
            "zip_include_packages",
            "zip_exclude_packages",
        ]

        for option in self.list_options:
            setattr(self, option, [])

        self.zip_exclude_packages = ["*"]
        self.optimize = 0
        self.build_exe = None
        self.no_compress = False
        self.path = None
        self.include_msvcr = None
        self.silent = None
        self.silent_level = None

    def finalize_options(self):
        build = self.get_finalized_command("build")
        self.build_base = build.build_base
        if self.build_exe is None:
            # get the value from deprecated option
            options = build.distribution.get_option_dict("build")
            build_exe = options.get("build_exe", (None, None))[1]
            if build_exe:
                build.warn(
                    "[DEPRECATED] The use of build command with 'build-exe' "
                    "option is deprecated.\n\t\t"
                    "Use build_exe command with 'build-exe' option instead."
                )
                self.build_exe = build_exe
        if self.build_exe is None:
            dir_name = f"exe.{get_platform()}-{get_python_version()}"
            self.build_exe = os.path.join(self.build_base, dir_name)

        self.optimize = int(self.optimize)

        # the degree of silencing, set from either the silent or silent-level
        # option, as appropriate
        self.silent_setting = 0
        if self.silent is not None and self.silent:
            self.silent_setting = 1

        if self.silent_level is None:
            pass
        elif self.silent_level is False:
            self.silent_setting = 0
        elif self.silent_level is True:
            self.silent_setting = 1
        elif isinstance(self.silent_level, int):
            self.silent_setting = self.silent_level
        elif isinstance(self.silent_level, str):
            try:
                self.silent_setting = int(self.silent_level)
            except ValueError:
                self.silent_setting = 1
        else:
            self.silent_setting = 1

        # Make sure all options of multiple values are lists
        for option in self.list_options:
            setattr(self, option, normalize_to_list(getattr(self, option)))

    def run(self):
        metadata = self.distribution.metadata
        constants_module = ConstantsModule(
            metadata.version, constants=self.constants
        )

        freezer: Freezer = Freezer(
            self.distribution.executables,
            constants_module,
            self.includes,
            self.excludes,
            self.packages,
            self.replace_paths,
            (not self.no_compress),
            self.optimize,
            self.path,
            self.build_exe,
            bin_includes=self.bin_includes,
            bin_excludes=self.bin_excludes,
            bin_path_includes=self.bin_path_includes,
            bin_path_excludes=self.bin_path_excludes,
            include_files=self.include_files,
            zip_includes=self.zip_includes,
            zip_include_packages=self.zip_include_packages,
            zip_exclude_packages=self.zip_exclude_packages,
            silent=self.silent_setting,
            metadata=metadata,
            include_msvcr=self.include_msvcr,
        )

        # keep freezer around so that its data case be used in bdist_mac phase
        self.freezer = freezer
        freezer.freeze()

    def set_source_location(self, name, *pathParts):
        env_name = f"{name.upper()}_BASE"
        attr_name = name.lower()
        source_dir = getattr(self, attr_name)
        if source_dir is None:
            base_dir = os.environ.get(env_name)
            if base_dir is None:
                return
            source_dir = os.path.join(base_dir, *pathParts)
            if os.path.isdir(source_dir):
                setattr(self, attr_name, source_dir)

    # -- Predicates for the sub-command list ---------------------------

    def has_executables(self):
        return getattr(self.distribution, "executables", None) is not None
