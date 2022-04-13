"""Implements 'build' command.

Borrowed from distutils.command.build of Python 3.10 and merged with
build subclass of cx_Freeze 6.10.

"""

import os
import sys
from sysconfig import get_platform, get_python_version

from setuptools import Command
from setuptools.errors import OptionError

__all__ = ["Build"]


def show_compilers():
    """List available compilers."""
    try:
        distutils_ccompiler = __import__(
            "distutils.ccompiler", fromlist=["show_compilers"]
        )
        distutils_ccompiler.show_compilers()
    except (ImportError, AttributeError):
        print("The list of available compilers was not found.")


# pylint: disable=attribute-defined-outside-init,missing-function-docstring
class Build(Command):
    """Build everything needed to install."""

    description = "build everything needed to install"

    user_options = [
        ("build-base=", "b", "base directory for build library"),
        (
            "build-purelib=",
            None,
            "build directory for platform-neutral distributions",
        ),
        (
            "build-platlib=",
            None,
            "build directory for platform-specific distributions",
        ),
        (
            "build-lib=",
            None,
            "build directory for all distribution (defaults to either "
            + "build-purelib or build-platlib",
        ),
        ("build-scripts=", None, "build directory for scripts"),
        ("build-temp=", "t", "temporary build directory"),
        (
            "plat-name=",
            "p",
            "platform name to build for, if supported "
            f"(default: {get_platform()})",
        ),
        ("compiler=", "c", "specify the compiler type"),
        ("parallel=", "j", "number of parallel build jobs"),
        (
            "debug",
            "g",
            "compile extensions and libraries with debugging information",
        ),
        ("force", "f", "forcibly build everything (ignore file timestamps)"),
        (
            "executable=",
            "e",
            "specify final destination interpreter path (build.py)",
        ),
        ("build-exe=", None, "build directory for executables"),
    ]

    boolean_options = ["debug", "force"]

    help_options = [
        ("help-compiler", None, "list available compilers", show_compilers),
    ]

    def initialize_options(self):
        self.build_base = "build"
        # these are decided only after 'build_base' has its final value
        # (unless overridden by the user or client)
        self.build_purelib = None
        self.build_platlib = None
        self.build_lib = None
        self.build_temp = None
        self.build_scripts = None
        self.compiler = None
        self.plat_name = None
        self.debug = None
        self.force = 0
        self.executable = None
        self.parallel = None
        self.build_exe = None

    def finalize_options(self):
        platform = get_platform()
        python_version = get_python_version()
        if self.plat_name is None:
            self.plat_name = platform
        else:
            # plat-name only supported for windows (other platforms are
            # supported via ./configure flags, if at all).  Avoid misleading
            # other platforms.
            if os.name != "nt":
                raise OptionError(
                    "--plat-name only supported on Windows (try "
                    "using './configure --help' on your platform)"
                )

        plat_specifier = f".{self.plat_name}-{python_version}"

        # Make it so Python 2.x and Python 2.x with --with-pydebug don't
        # share the same build directories. Doing so confuses the build
        # process for C modules
        if hasattr(sys, "gettotalrefcount"):
            plat_specifier += "-pydebug"

        # 'build_purelib' and 'build_platlib' just default to 'lib' and
        # 'lib.<plat>' under the base build directory.  We only use one of
        # them for a given distribution, though --
        if self.build_purelib is None:
            self.build_purelib = os.path.join(self.build_base, "lib")
        if self.build_platlib is None:
            self.build_platlib = os.path.join(
                self.build_base, "lib" + plat_specifier
            )

        # 'build_lib' is the actual directory that we will use for this
        # particular module distribution -- if user didn't supply it, pick
        # one of 'build_purelib' or 'build_platlib'.
        if self.build_lib is None:
            if self.distribution.has_ext_modules():
                self.build_lib = self.build_platlib
            else:
                self.build_lib = self.build_purelib

        # 'build_temp' -- temporary directory for compiler turds,
        # "build/temp.<plat>"
        if self.build_temp is None:
            self.build_temp = os.path.join(
                self.build_base, "temp" + plat_specifier
            )
        if self.build_scripts is None:
            self.build_scripts = os.path.join(
                self.build_base, f"scripts-{python_version}"
            )

        if self.executable is None and sys.executable:
            self.executable = os.path.normpath(sys.executable)

        if isinstance(self.parallel, str):
            try:
                self.parallel = int(self.parallel)
            except ValueError:
                raise OptionError("parallel should be an integer") from None

        # 'build_exe' is the actual directory that we will use for this
        if self.build_exe is None:
            self.build_exe = os.path.join(
                self.build_base, "exe" + plat_specifier
            )

    def run(self):
        # Run all relevant sub-commands.  This will be some subset of:
        #  - build_py      - pure Python modules
        #  - build_clib    - standalone C libraries
        #  - build_ext     - Python extensions
        #  - build_scripts - (Python) scripts
        #  - build_exe     - executables
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)

    # -- Predicates for the sub-command list ---------------------------

    def has_pure_modules(self):
        return self.distribution.has_pure_modules()

    def has_c_libraries(self):
        return self.distribution.has_c_libraries()

    def has_ext_modules(self):
        return self.distribution.has_ext_modules()

    def has_scripts(self):
        return self.distribution.has_scripts()

    def has_executables(self):
        return self.distribution.has_executables()

    sub_commands = [
        ("build_py", has_pure_modules),
        ("build_clib", has_c_libraries),
        ("build_ext", has_ext_modules),
        ("build_scripts", has_scripts),
        ("build_exe", has_executables),
    ]
