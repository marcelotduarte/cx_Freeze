"""The classes and functions with which cx_Freeze extends setuptools."""
# pylint: disable=C0116,C0103,W0201

import setuptools  # isort:skip
import distutils.command.build  # pylint: disable=W0402
import distutils.core  # pylint: disable=W0402
import logging
import os
import sys
import sysconfig
import warnings
from pathlib import Path
from typing import Optional

import setuptools.command.install
from setuptools.errors import SetupError

from .common import normalize_to_list
from .freezer import Freezer
from .module import ConstantsModule

if sys.platform == "win32":
    from .command.bdist_msi import BdistMSI
elif sys.platform == "darwin":
    from .command.bdist_mac import BdistDMG, BdistMac
else:
    from .command.bdist_rpm import BdistRPM

__all__ = [
    "build",
    "build_exe",
    "install",
    "install_exe",
    "setup",
]


class Distribution(setuptools.Distribution):
    """Distribution with support for executables."""

    def __init__(self, attrs):
        self.executables = []
        super().__init__(attrs)


class build(distutils.command.build.build):
    """Build everything needed to install."""

    user_options = distutils.command.build.build.user_options + [
        ("build-exe=", None, "build directory for executables")
    ]

    def get_sub_commands(self):
        sub_commands = distutils.command.build.build.get_sub_commands(self)
        if self.distribution.executables:
            sub_commands.append("build_exe")
        return sub_commands

    def initialize_options(self):
        distutils.command.build.build.initialize_options(self)
        self.build_exe = None

    def finalize_options(self):
        distutils.command.build.build.finalize_options(self)
        if self.build_exe is None:
            platform = sysconfig.get_platform()
            python_version = sysconfig.get_python_version()
            dir_name = f"exe.{platform}-{python_version}"
            self.build_exe = os.path.join(self.build_base, dir_name)


class build_exe(setuptools.Command):
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
        ("namespace-packages=", None, "[DEPRECATED]"),
        (
            "replace-paths=",
            None,
            "comma-separated list of paths to replace in included modules, "
            "using the form <search>=<replace>",
        ),
        ("path=", None, "comma-separated list of paths to search"),
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
        distribution = distutils.core.run_setup("setup.py", script_args)
        modules = [
            m for m in distribution.ext_modules if m.name == module_name
        ]
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
            # DEPRECATED
            "namespace_packages",
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
        self.set_undefined_options("build", ("build_exe", "build_exe"))
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
        if self.namespace_packages:
            warnings.warn(
                "namespace-packages is obsolete and will be removed in the "
                "next version"
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
            binIncludes=self.bin_includes,
            binExcludes=self.bin_excludes,
            binPathIncludes=self.bin_path_includes,
            binPathExcludes=self.bin_path_excludes,
            includeFiles=self.include_files,
            zipIncludes=self.zip_includes,
            zipIncludePackages=self.zip_include_packages,
            zipExcludePackages=self.zip_exclude_packages,
            silent=self.silent_setting,
            metadata=metadata,
            includeMSVCR=self.include_msvcr,
        )

        # keep freezer around so that its data case be used in bdist_mac phase
        self.freezer = freezer
        freezer.Freeze()

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


class install(setuptools.command.install.install):
    """Install everything from build directory."""

    user_options = setuptools.command.install.install.user_options + [
        ("install-exe=", None, "installation directory for executables")
    ]

    def expand_dirs(self):
        setuptools.command.install.install.expand_dirs(self)
        self._expand_attrs(["install_exe"])

    def get_sub_commands(self):
        sub_commands = setuptools.command.install.install.get_sub_commands(
            self
        )
        if self.distribution.executables:
            sub_commands.append("install_exe")
        return [s for s in sub_commands if s != "install_egg_info"]

    def initialize_options(self):
        setuptools.command.install.install.initialize_options(self)
        self.install_exe = None

    def finalize_options(self):
        if self.prefix is None and sys.platform == "win32":
            winreg = __import__("winreg")
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Software\Microsoft\Windows\CurrentVersion",
            )
            prefix = str(winreg.QueryValueEx(key, "ProgramFilesDir")[0])
            metadata = self.distribution.metadata
            self.prefix = f"{prefix}/{metadata.name}"
        setuptools.command.install.install.finalize_options(self)
        self.convert_paths("exe")
        if self.root is not None:
            self.change_roots("exe")

    def select_scheme(self, name):
        setuptools.command.install.install.select_scheme(self, name)
        if self.install_exe is None:
            if sys.platform == "win32":
                self.install_exe = "$base"
            else:
                metadata = self.distribution.metadata
                dir_name = f"{metadata.name}-{metadata.version}"
                self.install_exe = f"$base/lib/{dir_name}"


class install_exe(setuptools.Command):
    """Install executables built from Python scripts."""

    description = "install executables built from Python scripts"
    user_options = [
        ("install-dir=", "d", "directory to install executables to"),
        ("build-dir=", "b", "build directory (where to install from)"),
        ("force", "f", "force installation (overwrite existing files)"),
        ("skip-build", None, "skip the build steps"),
    ]

    def initialize_options(self):
        self.install_dir: Optional[str] = None
        self.force = 0
        self.build_dir = None
        self.skip_build = None

    def finalize_options(self):
        self.set_undefined_options("build", ("build_exe", "build_dir"))
        self.set_undefined_options(
            "install",
            ("install_exe", "install_dir"),
            ("force", "force"),
            ("skip_build", "skip_build"),
        )

    def run(self):
        if not self.skip_build:
            self.run_command("build_exe")
        self.outfiles = self.copy_tree(self.build_dir, self.install_dir)
        if sys.platform != "win32":
            install_dir = Path(self.install_dir)
            base_dir = install_dir.parent.parent
            bin_dir: Path = base_dir / "bin"
            if not bin_dir.exists():
                bin_dir.mkdir(parents=True)
            source_dir = ".." / install_dir.relative_to(base_dir)
            for executable in self.distribution.executables:
                name = executable.target_name
                source = source_dir / name
                target = bin_dir / name
                if target.exists():
                    target.unlink()
                target.symlink_to(source)
                self.outfiles.append(target.as_posix())

    def get_inputs(self):
        return self.distribution.executables or []

    def get_outputs(self):
        return self.outfiles or []


def _add_command_class(command_classes, name, cls):
    if name not in command_classes:
        command_classes[name] = cls


def setup(**attrs):
    attrs.setdefault("distclass", Distribution)
    command_classes = attrs.setdefault("cmdclass", {})
    if sys.platform == "win32":
        _add_command_class(command_classes, "bdist_msi", BdistMSI)
    elif sys.platform == "darwin":
        _add_command_class(command_classes, "bdist_dmg", BdistDMG)
        _add_command_class(command_classes, "bdist_mac", BdistMac)
    else:
        _add_command_class(command_classes, "bdist_rpm", BdistRPM)
    _add_command_class(command_classes, "build", build)
    _add_command_class(command_classes, "build_exe", build_exe)
    _add_command_class(command_classes, "install", install)
    _add_command_class(command_classes, "install_exe", install_exe)
    setuptools.setup(**attrs)
