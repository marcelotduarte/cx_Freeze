"""Implements the 'bdist_appimage' command (create Linux AppImage format).

https://appimage.org/
https://docs.appimage.org/
https://docs.appimage.org/packaging-guide/manual.html
"""

from __future__ import annotations

import logging
import os
import platform
import shutil
import stat
from ctypes.util import find_library
from pathlib import Path
from textwrap import dedent
from typing import ClassVar
from urllib.request import urlretrieve
from zipfile import ZipFile

from filelock import FileLock
from setuptools import Command

from cx_Freeze._compat import IS_LINUX
from cx_Freeze.common import resource_path
from cx_Freeze.exception import ExecError, PlatformError

__all__ = ["bdist_appimage"]

logger = logging.getLogger(__name__)

ARCH = platform.machine()

APPIMAGETOOL_RELEASES_URL = "https://github.com/AppImage/appimagetool/releases"
APPIMAGETOOL_DOWNLOAD = f"download/continuous/appimagetool-{ARCH}.AppImage"
APPIMAGETOOL_CACHE = f"~/.local/bin/appimagetool-{ARCH}.AppImage"

RUNTIME_RELEASES_URL = "https://github.com/AppImage/type2-runtime/releases"
RUNTIME_DOWNLOAD = f"download/continuous/runtime-{ARCH}"
RUNTIME_CACHE = f"~/.cache/cxfreeze/appimage/runtime-{ARCH}"


class bdist_appimage(Command):
    """Create a Linux AppImage."""

    description = "create a Linux AppImage"
    user_options: ClassVar[list[tuple[str, str | None, str]]] = [
        (
            "appimagetool=",
            None,
            f'path to appimagetool [default: "{APPIMAGETOOL_CACHE}"]',
        ),
        (
            "runtime-file=",
            None,
            f'path to type2 runtime [default: "{RUNTIME_CACHE}"]',
        ),
        ("sign", None, "Sign with gpg or gpg2"),
        ("sign-key=", None, "Key ID to use for gpg/gpg2 signatures"),
        (
            "updateinformation=",
            None,
            "Embed update information STRING (or 'guess') "
            "and generate zsync file",
        ),
        ("target-name=", None, "name of the file to create"),
        ("target-version=", None, "version of the file to create"),
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
            'directory to put final built distributions in [default: "dist"]',
        ),
        (
            "skip-build",
            None,
            "skip rebuilding everything (for testing/debugging)",
        ),
        ("silent", "s", "suppress all output except warnings"),
    ]
    boolean_options: ClassVar[list[str]] = [
        "skip-build",
        "silent",
    ]

    def initialize_options(self) -> None:
        self.appimagetool = None
        self.runtime_file = None
        self.sign = None
        self.sign_key = None
        self.updateinformation = None
        self.target_name = None
        self.target_version = None

        self.bdist_base = None
        self.build_dir = None
        self.dist_dir = None
        self.skip_build = None

        self.fullname = None
        self.silent = None

        self._warnings = []

    def finalize_options(self) -> None:
        if not IS_LINUX:
            msg = "bdist_appimage is only supported on Linux"
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
        if self.distribution.have_run.get("build_exe"):
            if not self.skip_build:
                self.skip_build = 1
        elif self.silent is not None:
            self.verbose = not self.silent
            build_exe = self.distribution.command_obj.get("build_exe")
            if build_exe:
                build_exe.silent = 1

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

        # download tools if not in cache
        self.appimagetool = self._get_file(
            self.appimagetool or APPIMAGETOOL_CACHE,
            os.path.join(APPIMAGETOOL_RELEASES_URL, APPIMAGETOOL_DOWNLOAD),
        )
        self.runtime_file = self._get_file(
            self.runtime_file or RUNTIME_CACHE,
            os.path.join(RUNTIME_RELEASES_URL, RUNTIME_DOWNLOAD),
        )

    def _get_file(self, filename: str, full_url: str) -> str:
        """Fetch 'filename' from the web if not available locally."""
        filename = os.path.expanduser(filename)
        self.mkpath(os.path.dirname(filename))
        with FileLock(filename + ".lock"):
            if not os.path.exists(filename):
                msg = (
                    "download and install "
                    f"{os.path.basename(filename)} from {full_url}"
                )
                self.announce(msg, logging.INFO)
                urlretrieve(full_url, filename)  # noqa: S310
                if os.path.splitext(filename)[1] == ".AppImage":
                    os.chmod(filename, stat.S_IRWXU)
        return filename

    def run(self) -> None:
        """Create the application bundle.

        https://docs.appimage.org/reference/appdir.html
        """
        if not self.skip_build:
            self.run_command("build_exe")

        # Make appimage (by default in dist directory)
        # Set the full path of appimage to be built
        self.mkpath(self.dist_dir)
        output = os.path.abspath(os.path.join(self.dist_dir, self.app_name))
        if os.path.exists(output):
            os.unlink(output)

        # Create AppDir format
        appdir = os.path.abspath(os.path.join(self.bdist_base, "AppDir"))
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

        # Add icons, desktop file and entrypoint
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
            icon_filename = os.fspath(resource_path(f"icons/{icon_name}"))
            self.copy_file(icon_filename, icons_dir)
        else:
            icon_name = executable.icon.name
            self.move_file(os.path.join(appdir, icon_name), icons_dir)
        relative_reference = os.path.join(share_icons, icon_name)

        # .DirIcon is a symlink to executable.icon or logox128.png
        origin = os.path.join(appdir, ".DirIcon")
        self.execute(
            os.symlink,
            (relative_reference, origin),
            msg=f"linking {origin} -> {relative_reference}",
        )
        origin = os.path.join(
            appdir, f"{self.target_name}{os.path.splitext(icon_name)[1]}"
        )
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
            Terminal={"false" if executable.app_type == "gui" else "true"}
            X-AppImage-Arch={ARCH}
            X-AppImage-Name={self.target_name}
            X-AppImage-Version={self.target_version or ""}
        """
        self.save_as_file(
            dedent(desktop_entry),
            os.path.join(appdir, f"{self.target_name}.desktop"),
        )
        entrypoint = f"""\
            #!/bin/sh
            # If running from an extracted image, fix APPDIR
            if [ -z "$APPIMAGE" ]; then
                self="$(readlink -f -- "$0")"
                export APPDIR="${{self%/*}}"
            fi
            # Call the application entry point
            # Use 'exec' to avoid a new process from being started.
            exec "$APPDIR/{executable.target_name}" "$@"
        """
        self.save_as_file(
            dedent(entrypoint), os.path.join(appdir, "AppRun"), mode="x"
        )

        # Build an AppImage from an AppDir
        os.environ["ARCH"] = ARCH
        if self.target_version:
            os.environ["VERSION"] = self.target_version
        cmd = [self.appimagetool]
        if find_library("fuse") is None:  # libfuse.so.2 is not found
            cmd.append("--appimage-extract-and-run")
        if self.runtime_file is not None:
            cmd += ["--runtime-file", self.runtime_file]
        if self.sign is not None:
            cmd.append("--sign")
        if self.sign_key is not None:
            cmd += ["--sign-key", self.sign_key]
        if self.updateinformation is not None:
            if self.updateinformation == "guess":
                # check for github, travis or gitlab
                if (
                    os.environ.get("GITHUB_REPOSITORY")
                    or os.environ.get("TRAVIS_REPO_SLUG")
                    or os.environ.get("CI_COMMIT_REF_NAME")
                ):
                    if os.environ.get("GITHUB_REPOSITORY"):
                        # appimagetool requires a GitHub token, but doesn't
                        # actually use it.
                        os.environ.setdefault("GITHUB_TOKEN", "fake-token")
                    cmd.append("--guess")
            else:
                cmd += ["--updateinformation", self.updateinformation]
        if self.verbose >= 1:
            cmd.append("--verbose")
        cmd += ["--no-appstream", appdir, output]
        with FileLock(self.appimagetool + ".lock"):
            cwd = os.getcwd()
            os.chdir(self.dist_dir)
            try:
                self.spawn(cmd, search_path=0)
            finally:
                os.chdir(cwd)

        self.warnings()
        if not os.path.exists(output):
            msg = "Could not build AppImage"
            raise ExecError(msg)

    def save_as_file(self, data, outfile, mode="r") -> tuple[str, int]:
        """Save an input data to a file respecting verbose, dry-run and force
        flags.
        """
        if not self.force and os.path.exists(outfile):
            if self.verbose >= 1:
                self.warn_delayed(f"not creating {outfile} (output exists)")
            return (outfile, 0)
        if self.verbose >= 1:
            self.announce(f"creating {outfile}", logging.INFO)

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
            self.announce(f"WARNING: {msg}", logging.WARNING)
