"""Implements the 'bdist_appimage' command (create Linux AppImage format).

https://appimage.org/
https://docs.appimage.org/
https://docs.appimage.org/packaging-guide/manual.html#ref-manual
"""

from __future__ import annotations

import os
import platform
import shutil
import stat
from ctypes.util import find_library
from logging import INFO, WARNING
from pathlib import Path
from textwrap import dedent
from typing import ClassVar
from urllib.request import urlretrieve
from zipfile import ZipFile

from filelock import FileLock
from setuptools import Command

import cx_Freeze.icons
from cx_Freeze.exception import ExecError, PlatformError

__all__ = ["bdist_appimage"]

ARCH = platform.machine()
APPIMAGEKIT_URL = "https://github.com/AppImage/AppImageKit/releases"
APPIMAGEKIT_PATH = f"download/continuous/appimagetool-{ARCH}.AppImage"
APPIMAGEKIT_TOOL = "~/.local/bin/appimagetool"


class bdist_appimage(Command):
    """Create a Linux AppImage."""

    description = "create a Linux AppImage"
    user_options: ClassVar[list[tuple[str, str | None, str]]] = [
        (
            "appimagekit=",
            None,
            f"path to AppImageKit [default: {APPIMAGEKIT_TOOL}]",
        ),
        (
            "bdist-base=",
            None,
            "base directory for creating built distributions",
        ),
        (
            "build-dir=",
            "b",
            "directory of built executables and dependent files",
        ),
        (
            "dist-dir=",
            "d",
            "directory to put final built distributions in [default: dist]",
        ),
        (
            "skip-build",
            None,
            "skip rebuilding everything (for testing/debugging)",
        ),
        ("target-name=", None, "name of the file to create"),
        ("target-version=", None, "version of the file to create"),
        ("silent", "s", "suppress all output except warnings"),
    ]
    boolean_options: ClassVar[list[str]] = [
        "skip-build",
        "silent",
    ]

    def initialize_options(self) -> None:
        self.appimagekit = None

        self.bdist_base = None
        self.build_dir = None
        self.dist_dir = None
        self.skip_build = None

        self.target_name = None
        self.target_version = None
        self.fullname = None
        self.silent = None

        self._warnings = []

    def finalize_options(self) -> None:
        if os.name != "posix":
            msg = (
                "don't know how to create AppImage "
                f"distributions on platform {os.name}"
            )
            raise PlatformError(msg)

        # inherit options
        self.set_undefined_options(
            "build_exe",
            ("build_exe", "build_dir"),
            ("silent", "silent"),
        )
        self.set_undefined_options(
            "bdist",
            ("bdist_base", "bdist_base"),
            ("dist_dir", "dist_dir"),
            ("skip_build", "skip_build"),
        )
        # for the bdist commands, there is a chance that build_exe has already
        # been executed, so check skip_build if build_exe have_run
        if not self.skip_build and self.distribution.have_run.get("build_exe"):
            self.skip_build = 1

        if self.target_name is None:
            if self.distribution.metadata.name:
                self.target_name = self.distribution.metadata.name
            else:
                executables = self.distribution.executables
                executable = executables[0]
                self.warn_delayed(
                    "using the first executable as target_name: "
                    f"{executable.target_name}"
                )
                self.target_name = executable.target_name

        if self.target_version is None and self.distribution.metadata.version:
            self.target_version = self.distribution.metadata.version

        name = self.target_name
        version = self.target_version
        name, ext = os.path.splitext(name)
        if ext == ".AppImage":
            self.app_name = self.target_name
            self.fullname = name
        elif version:
            self.app_name = f"{name}-{version}-{ARCH}.AppImage"
            self.fullname = f"{name}-{version}"
        else:
            self.app_name = f"{name}-{ARCH}.AppImage"
            self.fullname = name

        if self.silent is not None:
            self.verbose = 0 if self.silent else 2
            build_exe = self.distribution.command_obj.get("build_exe")
            if build_exe:
                build_exe.silent = self.silent

        # validate or download appimagekit
        self._get_appimagekit()

    def _get_appimagekit(self) -> None:
        """Fetch AppImageKit from the web if not available locally."""
        appimagekit = os.path.expanduser(self.appimagekit or APPIMAGEKIT_TOOL)
        appimagekit_dir = os.path.dirname(appimagekit)
        self.mkpath(appimagekit_dir)
        with FileLock(appimagekit + ".lock"):
            if not os.path.exists(appimagekit):
                self.announce(
                    f"download and install AppImageKit from {APPIMAGEKIT_URL}",
                    INFO,
                )
                name = os.path.basename(APPIMAGEKIT_PATH)
                filename = os.path.join(appimagekit_dir, name)
                if not os.path.exists(filename):
                    urlretrieve(  # noqa: S310
                        os.path.join(APPIMAGEKIT_URL, APPIMAGEKIT_PATH),
                        filename,
                    )
                    os.chmod(filename, stat.S_IRWXU)
                if not os.path.exists(appimagekit):
                    self.execute(
                        os.symlink,
                        (filename, appimagekit),
                        msg=f"linking {appimagekit} -> {filename}",
                    )
        self.appimagekit = appimagekit

    def run(self) -> None:
        # Create the application bundle
        if not self.skip_build:
            self.run_command("build_exe")

        # Make appimage (by default in dist directory)
        # Set the full path of appimage to be built
        self.mkpath(self.dist_dir)
        output = os.path.abspath(os.path.join(self.dist_dir, self.app_name))
        if os.path.exists(output):
            os.unlink(output)

        # Make AppDir folder
        appdir = os.path.join(self.bdist_base, "AppDir")
        if os.path.exists(appdir):
            self.execute(shutil.rmtree, (appdir,), msg=f"removing {appdir}")
        self.mkpath(appdir)

        # Copy from build_exe
        self.copy_tree(self.build_dir, appdir, preserve_symlinks=True)

        # Remove zip file after putting all files in the file system
        # (appimage is a compressed file, no need of internal zip file)
        library_data = Path(appdir, "lib", "library.dat")
        if library_data.exists():
            target_lib_dir = library_data.parent
            filename = target_lib_dir / library_data.read_bytes().decode()
            with ZipFile(filename) as outfile:
                outfile.extractall(target_lib_dir)
            filename.unlink()
            library_data.unlink()

        # Add icon, desktop file, entrypoint
        share_icons = os.path.join("share", "icons")
        icons_dir = os.path.join(appdir, share_icons)
        self.mkpath(icons_dir)

        executables = self.distribution.executables
        executable = executables[0]
        if len(executables) > 1:
            self.warn_delayed(
                "using the first executable as entrypoint: "
                f"{executable.target_name}"
            )
        if executable.icon is None:
            icon_name = "logox128.png"
            icon_source_dir = os.path.dirname(cx_Freeze.icons.__file__)
            self.copy_file(os.path.join(icon_source_dir, icon_name), icons_dir)
        else:
            icon_name = executable.icon.name
            self.move_file(os.path.join(appdir, icon_name), icons_dir)
        relative_reference = os.path.join(share_icons, icon_name)
        origin = os.path.join(appdir, ".DirIcon")
        self.execute(
            os.symlink,
            (relative_reference, origin),
            msg=f"linking {origin} -> {relative_reference}",
        )

        desktop_entry = f"""\
            [Desktop Entry]
            Type=Application
            Name={self.target_name}
            Exec={executable.target_name}
            Comment={self.distribution.get_description()}
            Icon=/{share_icons}/{os.path.splitext(icon_name)[0]}
            Categories=Development;
            Terminal=true
            X-AppImage-Arch={ARCH}
            X-AppImage-Name={self.target_name}
            X-AppImage-Version={self.target_version or ''}
        """
        self.save_as_file(
            dedent(desktop_entry),
            os.path.join(appdir, f"{self.target_name}.desktop"),
        )
        entrypoint = f"""\
            #! /bin/bash
            # If running from an extracted image, fix APPDIR
            if [ -z "$APPIMAGE" ]; then
                self="$(readlink -f -- $0)"
                export APPDIR="${{self%/*}}"
            fi
            # Call the application entry point
            "$APPDIR/{executable.target_name}" "$@"
        """
        self.save_as_file(
            dedent(entrypoint), os.path.join(appdir, "AppRun"), mode="x"
        )

        # Build an AppImage from an AppDir
        os.environ["ARCH"] = ARCH
        cmd = [self.appimagekit, "--no-appstream", appdir, output]
        if find_library("fuse") is None:  # libfuse.so.2 is not found
            cmd.insert(1, "--appimage-extract-and-run")
        with FileLock(self.appimagekit + ".lock"):
            self.spawn(cmd, search_path=0)
        if not os.path.exists(output):
            msg = "Could not build AppImage"
            raise ExecError(msg)

        self.warnings()

    def save_as_file(self, data, outfile, mode="r") -> tuple[str, int]:
        """Save an input data to a file respecting verbose, dry-run and force
        flags.
        """
        if not self.force and os.path.exists(outfile):
            if self.verbose >= 1:
                self.warn_delayed(f"not creating {outfile} (output exists)")
            return (outfile, 0)
        if self.verbose >= 1:
            self.announce(f"creating {outfile}", INFO)

        if self.dry_run:
            return (outfile, 1)

        if isinstance(data, str):
            data = data.encode()
        with open(outfile, "wb") as out:
            out.write(data)
        st_mode = stat.S_IRUSR
        if "w" in mode:
            st_mode = st_mode | stat.S_IWUSR
        if "x" in mode:
            st_mode = st_mode | stat.S_IXUSR
        os.chmod(outfile, st_mode)
        return (outfile, 1)

    def warn_delayed(self, msg) -> None:
        self._warnings.append(msg)

    def warnings(self) -> None:
        for msg in self._warnings:
            self.announce(f"WARNING: {msg}", WARNING)
