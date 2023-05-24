"""cxfreeze command line tool."""

from __future__ import annotations

import argparse
import os
import sys
import sysconfig

from . import __version__
from .common import normalize_to_list
from .executable import Executable
from .freezer import Freezer

__all__ = ["main"]

DESCRIPTION = """
Freeze a Python script and all of its referenced modules to a base \
executable which can then be distributed without requiring a Python \
installation.
"""

VERSION = f"""
%(prog)s {__version__}
Copyright (c) 2020-2023 Marcelo Duarte. All rights reserved.
Copyright (c) 2007-2020 Anthony Tuininga. All rights reserved.
Copyright (c) 2001-2006 Computronix Corporation. All rights reserved.
"""


def prepare_parser():
    """Helper function to parse the arguments."""
    parser = argparse.ArgumentParser(prog="cxfreeze", epilog=VERSION)
    parser.add_argument("--version", action="version", version=VERSION)
    # Executable parameters
    parser.add_argument(
        "script",
        nargs="?",
        metavar="SCRIPT",
        help="the name of the file containing the script which is to be "
        "frozen",
    )
    parser.add_argument(
        "--init-script",
        dest="init_script",
        metavar="NAME",
        help="script which will be executed upon startup; if the name of the "
        "file is not an absolute file name, the subdirectory initscripts "
        "(rooted in the directory in which the cx_Freeze package is found) "
        "will be searched for a file matching the name",
    )
    parser.add_argument(
        "--base-name",
        dest="base_name",
        metavar="NAME",
        help="the filename of the base executable; if a name is given without "
        "an absolute path, the subdirectory bases (rooted in the directory in "
        "which the freezer is found) will be searched for a file matching the "
        "name",
    )
    parser.add_argument(
        "--target-name",
        dest="target_name",
        metavar="NAME",
        help="the name of the target executable; the default value is the "
        "name of the script; the extension is optional (automatically added "
        "on Windows); support for names with version; if specified a "
        "pathname, raise an error",
    )
    parser.add_argument(
        "--icon",
        dest="icon",
        metavar="NAME",
        help="name of icon which should be included in the executable itself "
        "on Windows or placed in the target directory for other platforms "
        "(ignored by Python app from Microsoft Store)",
    )
    parser.add_argument(
        "--manifest",
        dest="manifest",
        metavar="NAME",
        help="name of manifest which should be included in the executable "
        "itself (Windows only - ignored by Python app from Microsoft Store)",
    )
    parser.add_argument(
        "--uac-admin",
        action="store_true",
        dest="uac_admin",
        help="creates a manifest for an application that will request eleva"
        "tion (Windows only - ignored by Python app from Microsoft Store)",
    )
    parser.add_argument(
        "--shortcut-name",
        dest="shortcut_name",
        metavar="NAME",
        help="the name to give a shortcut for the executable when included in "
        "an MSI package (Windows only)",
    )
    parser.add_argument(
        "--shortcut-dir",
        dest="shortcut_dir",
        metavar="DIR",
        help="the directory in which to place the shortcut when being instal"
        "led by an MSI package; see the MSI Shortcut table documentation for "
        "more information on what values can be placed here (Windows only)",
    )
    parser.add_argument(
        "--copyright",
        dest="copyright",
        help="the copyright value to include in the version resource "
        "associated with executable (Windows only)",
    )
    parser.add_argument(
        "--trademarks",
        dest="trademarks",
        help="the trademarks value to include in the version resource "
        "associated with the executable (Windows only)",
    )
    # Freezer parameters
    platform = sysconfig.get_platform()
    python_version = sysconfig.get_python_version()
    dir_name = f"exe.{platform}-{python_version}"
    parser.add_argument(
        "--target-dir",
        "--install-dir",
        dest="target_dir",
        default=os.path.abspath(os.path.join("build", dir_name)),
        metavar="DIR",
        help="directory for built executable and dependent files"
        " (default: %(default)s)",
    )
    parser.add_argument(
        "-O",
        action="count",
        default=0,
        dest="optimize",
        help="optimize generated bytecode as per PYTHONOPTIMIZE; "
        "use -OO in order to remove doc strings",
    )
    parser.add_argument(
        "--excludes",
        "--exclude-modules",
        dest="excludes",
        metavar="NAMES",
        help="comma-separated list of modules to exclude",
    )
    parser.add_argument(
        "--includes",
        "--include-modules",
        dest="includes",
        metavar="NAMES",
        help="comma-separated list of modules to include",
    )
    parser.add_argument(
        "--packages",
        dest="packages",
        metavar="NAMES",
        help="comma-separated list of packages to include, "
        "which includes all submodules in the package",
    )
    parser.add_argument(
        "--replace-paths",
        dest="replace_paths",
        metavar="DIRECTIVES",
        help="comma-separated list of paths to replace in the code object of "
        "included modules, using the form <search>=<replace>; search can be * "
        "which means all paths not already specified, leaving just the "
        "relative path to the module; multiple values are separated by the "
        "standard path separator",
    )
    parser.add_argument(
        "--default-path",
        action="append",
        dest="default_path",
        metavar="DIRS",
        help="list of paths separated by the standard path separator for the "
        "platform which will be used to initialize sys.path prior to running "
        "the module finder",
    )
    parser.add_argument(
        "--include-path",
        action="append",
        dest="include_path",
        metavar="DIRS",
        help="list of paths separated by the standard path separator for the "
        "platform which will be used to modify sys.path prior to running the "
        "module finder",
    )
    parser.add_argument(
        "-c",
        "--compress",
        action="store_true",
        dest="compress",
        help="compress byte code in zip files",
    )
    # TODO: "constants"
    parser.add_argument(
        "--bin-includes",
        dest="bin_includes",
        help="comma-separated list of files to include when determining "
        "dependencies of binary files that would normally be excluded, using "
        "first the full file name, then just the base file name, then the "
        "file name without any version numbers (the version numbers that "
        "normally follow the shared object extension are stripped prior to "
        "performing the comparison)",
    )
    parser.add_argument(
        "--bin-excludes",
        dest="bin_excludes",
        help="comma-separated list of files to exclude when determining "
        "dependencies of binary files that would normally be included, using "
        "first the full file name, then just the base file name, then the "
        "file name without any version numbers (the version numbers that "
        "normally follow the shared object extension are stripped prior to "
        "performing the comparison)",
    )
    parser.add_argument(
        "--bin-path-includes",
        dest="bin_path_includes",
        help="comma-separated list of paths from which to include files when "
        "determining dependencies of binary files",
    )
    parser.add_argument(
        "--bin-path-excludes",
        dest="bin_path_excludes",
        help="comma-separated list of paths from which to exclude files when "
        "determining dependencies of binary files",
    )
    parser.add_argument(
        "--include-files",
        dest="include_files",
        metavar="NAMES",
        help="comma-separated list of additional files to include in "
        "distribution",
    )
    parser.add_argument(
        "-z",
        "--zip-include",
        dest="zip_includes",
        action="append",
        default=[],
        metavar="SPEC",
        help="additional file to include in zip file or a specification of "
        "the form name=arcname which will specify the archive name to use; "
        "multiple --zip-include arguments can be used",
    )
    parser.add_argument(
        "--zip-include-packages",
        dest="zip_include_packages",
        metavar="NAMES",
        help="comma-separated list of packages which should be included in "
        "the zip file; the default is for all packages to be placed in the "
        "file system, not the zip file; those packages which are known to "
        "work well inside a zip file can be included if desired; use * to "
        "specify that all packages should be included in the zip file",
    )
    parser.add_argument(
        "--zip-exclude-packages",
        dest="zip_exclude_packages",
        default="*",
        metavar="NAMES",
        help="comma-separated list of packages which should be excluded from "
        "the zip file and placed in the file system instead; the default is "
        "for all packages to be placed in the file system since a number of pa"
        "ckages assume that is where they are found and will fail when placed "
        "in a zip file; use * to specify that all packages should be placed "
        "in the file system and excluded from the zip file (the default)",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        dest="silent",
        help="suppress all output except warnings and errors",
    )
    parser.add_argument(
        "--include-msvcr",
        action="store_true",
        dest="include_msvcr",
        help="include the Microsoft Visual C runtime files",
    )
    # remove the initial "usage: " of format_usage()
    parser.usage = parser.format_usage()[len("usage: ") :] + DESCRIPTION
    return parser


def parse_command_line(parser):
    """Helper function to parse the command line."""
    args = parser.parse_args()
    if args.script is None and args.includes is None:
        parser.error("script or a list of modules must be specified")
    if args.script is None and args.target_name is None:
        parser.error("script or a target name must be specified")
    args.includes = normalize_to_list(args.includes)
    args.excludes = normalize_to_list(args.excludes)
    args.packages = normalize_to_list(args.packages)
    replace_paths = []
    if args.replace_paths:
        for directive in args.replace_paths.split(os.pathsep):
            from_path, replacement = directive.split("=")
            replace_paths.append((from_path, replacement))
    args.replace_paths = replace_paths
    if args.default_path is not None:
        sys.path = [
            p for mp in args.default_path for p in mp.split(os.pathsep)
        ]
    if args.include_path is not None:
        paths = [p for mp in args.include_path for p in mp.split(os.pathsep)]
        sys.path = paths + sys.path
    if args.script is not None:
        sys.path.insert(0, os.path.dirname(args.script))
    args.bin_includes = normalize_to_list(args.bin_includes)
    args.bin_excludes = normalize_to_list(args.bin_excludes)
    args.bin_path_includes = normalize_to_list(args.bin_path_includes)
    args.bin_path_excludes = normalize_to_list(args.bin_path_excludes)
    args.include_files = normalize_to_list(args.include_files)
    zip_includes = []
    if args.zip_includes:
        for spec in args.zip_includes:
            if "=" in spec:
                zip_includes.append(spec.split("=", 1))
            else:
                zip_includes.append(spec)
    args.zip_includes = zip_includes
    args.zip_include_packages = normalize_to_list(args.zip_include_packages)
    args.zip_exclude_packages = normalize_to_list(args.zip_exclude_packages)
    return args


def main():
    """Entry point for cxfreeze command line tool."""
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)

    args = parse_command_line(prepare_parser())
    executables = [
        Executable(
            args.script,
            args.init_script,
            args.base_name,
            args.target_name,
            args.icon,
            args.shortcut_name,
            args.shortcut_dir,
            args.copyright,
            args.trademarks,
            args.manifest,
            args.uac_admin,
        )
    ]
    freezer: Freezer = Freezer(
        executables,
        excludes=args.excludes,
        includes=args.includes,
        packages=args.packages,
        replace_paths=args.replace_paths,
        compress=args.compress,
        optimize=args.optimize,
        path=None,
        target_dir=args.target_dir,
        bin_includes=args.bin_includes,
        bin_excludes=args.bin_excludes,
        bin_path_includes=args.bin_path_includes,
        bin_path_excludes=args.bin_path_excludes,
        include_files=args.include_files,
        zip_includes=args.zip_includes,
        zip_include_packages=args.zip_include_packages,
        zip_exclude_packages=args.zip_exclude_packages,
        silent=args.silent,
        include_msvcr=args.include_msvcr,
    )
    freezer.freeze()
