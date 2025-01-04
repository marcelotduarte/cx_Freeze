"""cxfreeze command line tool."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from cx_Freeze import __version__, setup
from cx_Freeze._pyproject import get_pyproject_tool_data

__all__ = ["main"]

DESCRIPTION = """
Freeze a Python script and all of its referenced modules to a base \
executable which can then be distributed without requiring a Python \
installation.
"""

VERSION = f"""
%(prog)s {__version__}
Copyright (c) 2020-2025 Marcelo Duarte. All rights reserved.
Copyright (c) 2007-2019 Anthony Tuininga. All rights reserved.
Copyright (c) 2001-2006 Computronix Corporation. All rights reserved.
"""

EPILOG = """
Note:
    * Windows only options are ignored by other OS and \
when used by Python app from Microsoft Store.

Additional help:
    %(prog)s build_exe --help

Linux and similar OS:
    %(prog)s bdist_appimage --help
    %(prog)s bdist_deb --help
    %(prog)s bdist_rpm --help
macOS:
    %(prog)s bdist_dmg --help
    %(prog)s bdist_mac --help
Windows:
    %(prog)s bdist_msi --help
"""


def prepare_parser() -> argparse.ArgumentParser:
    """Helper function to parse the arguments."""
    parser = argparse.ArgumentParser(
        prog="cxfreeze",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )
    # Executable parameters
    parser.add_argument(
        "--script",
        metavar="NAME",
        help="the name of the file containing the script which is to be "
        "frozen",
    )
    parser.add_argument(
        "--init-script",
        metavar="NAME",
        help="script which will be executed upon startup; if the name of the "
        "file is not an absolute file name, the subdirectory initscripts "
        "(rooted in the directory in which the cx_Freeze package is found) "
        "will be searched for a file matching the name",
    )
    parser.add_argument(
        "--base",
        "--base-name",
        metavar="NAME",
        help="the name of the base executable; the pre-defined values are: "
        '"console", "gui" and "service"; a user-defined base is accepted '
        "if it is given with an absolute path name [default: console]",
    )
    parser.add_argument(
        "--target-name",
        metavar="NAME",
        help="the name of the target executable; the default value is the "
        "name of the script; it is recommended NOT to use an extension "
        "(automatically added on Windows); target-name with version is "
        "supported; if specified a path, raise an error",
    )
    parser.add_argument(
        "--target-dir",
        metavar="DIR",
        help="directory for built executables and dependent files",
    )
    parser.add_argument(
        "--icon",
        metavar="NAME",
        help="name of icon which should be included in the executable itself "
        "on Windows or placed in the target directory for other platforms; "
        "it is recommended NOT to use an extension (automatically added "
        '".ico" on Windows, ".icns" on macOS and ".png" or ".svg" on Linux '
        "and others)",
    )
    parser.add_argument(
        "--manifest",
        metavar="NAME",
        help="name of manifest which should be included in the executable "
        "itself (Windows only)",
    )
    parser.add_argument(
        "--uac-admin",
        action="store_true",
        help="creates a manifest for an application that will request "
        "elevation (Windows only)",
    )
    parser.add_argument(
        "--uac-uiaccess",
        action="store_true",
        dest="uac_uiaccess",
        help="changes the application manifest to bypass user interface "
        "control (Windows only)",
    )
    parser.add_argument(
        "--shortcut-name",
        metavar="NAME",
        help="the name to give a shortcut for the executable when included in "
        "an MSI package (Windows only)",
    )
    parser.add_argument(
        "--shortcut-dir",
        metavar="DIR",
        help="the directory in which to place the shortcut when being instal"
        "led by an MSI package; see the MSI Shortcut table documentation for "
        "more information on what values can be placed here (Windows only)",
    )
    parser.add_argument(
        "--copyright",
        help="the copyright value to include in the version resource "
        "associated with executable (Windows only)",
    )
    parser.add_argument(
        "--trademarks",
        help="the trademarks value to include in the version resource "
        "associated with the executable (Windows only)",
    )
    # options to redirect to global
    parser.add_argument(
        "--debug", action="store_true", help="print debug information"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="run verbosely"
    )

    # Command positional parameter
    parser.add_argument(
        "command",
        nargs=argparse.OPTIONAL,
        metavar="COMMAND",
        help="build, build_exe or supported bdist commands (and to be "
        "backwards compatible, can replace --script option)",
    )
    # Version
    parser.add_argument("--version", action="version", version=VERSION)

    return parser


def main() -> None:
    """Entry point for cxfreeze command line tool."""
    sys.setrecursionlimit(sys.getrecursionlimit() * 10)

    parser = prepare_parser()
    args, argv = parser.parse_known_args()
    script = args.script
    command = args.command
    verbose = args.verbose

    # help
    if "-h" in argv or "--help" in argv:
        if command is None:
            parser.print_help()
        else:
            setup(
                executables=None,
                script_args=[command, "--help"],
                script_name=parser.prog,
            )
        parser.exit()

    # usage
    deprecated = []
    if script is None:
        if command is None:
            parser.error("--script or command must be specified")
        elif not command.startswith(("build", "bdist", "install")):
            args.script, command = command, script  # backwards compatible
            deprecated.append("usage: required to use --script NAME")
    if command is None:
        command = "build_exe"

    # deprecated options
    if command == "build_exe" or "build_exe" in argv:
        args_to_replace = [
            ("--install-dir", "--build-exe"),
            ("--exclude-modules", "--excludes"),
            ("--include-modules", "--includes"),
            ("-c", None),
            ("--compress", None),
            ("-OO", "--optimize=2"),  # test -OO before -O
            ("-O", "--optimize=1"),
            ("-z", "--zip-includes"),
            ("--default-path", "--path"),
            ("-s", "--silent"),
        ]
        new_argv = []
        for arg in argv:
            new_argv.append(arg)
            for search, replace in args_to_replace:
                if arg.startswith(search):
                    new_argv.pop()
                    if replace is None:
                        deprecated.append(f"{search} option removed")
                    else:
                        new_argv.append(arg.replace(search, replace))
                        deprecated.append(
                            f"{search} option replaced by {replace}"
                        )
                    break
        argv = new_argv

    # redirected options
    if args.target_dir:
        argv.append(f"--build-exe={args.target_dir}")
    if args.debug:
        import setuptools.dist

        os.environ["DISTUTILS_DEBUG"] = "1"
        setuptools.dist.DEBUG = 1

    # finalize command line options
    executables = []
    script_args = [command, *argv]
    if args.script:
        delattr(args, "command")
        delattr(args, "debug")
        delattr(args, "target_dir")
        delattr(args, "verbose")
        executables = [vars(args)]
    if script_args[0] == "build" and "build_exe" not in script_args:
        script_args.insert(1, "build_exe")
    if verbose:
        script_args.insert(0, "--verbose")

    # fix sys.path for cxfreeze command line
    command = Path(sys.argv[0])
    if command.stem == "cxfreeze":
        path_to_remove = os.fspath(command.parent)
        if path_to_remove in sys.path:
            sys.path.remove(path_to_remove)
        else:
            # using cmd on Windows
            path_to_remove = os.fspath(command.with_suffix(".exe"))
            if path_to_remove in sys.path:
                sys.path.remove(path_to_remove)
        sys.path.insert(0, os.getcwd())

    # get options from pyproject.toml
    options = get_pyproject_tool_data()
    executables.extend(options.pop("executables", []))

    setup(
        command_options=options,
        executables=executables,
        script_args=script_args,
        script_name=parser.prog,
    )

    if deprecated:
        for warning_msg in deprecated:
            print("WARNING: deprecated", warning_msg)
