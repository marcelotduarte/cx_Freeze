"""Implements the 'bdist_dmg' command (create macOS dmg and/or app bundle)."""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import ClassVar

from setuptools import Command

__all__ = ["bdist_dmg"]


class bdist_dmg(Command):
    """Create a Mac DMG disk image containing the Mac application bundle."""

    description = (
        "create a Mac DMG disk image containing the Mac application bundle"
    )
    user_options: ClassVar[list[tuple[str, str | None, str]]] = [
        ("volume-label=", None, "Volume label of the DMG disk image"),
        (
            "applications-shortcut=",
            None,
            "Boolean for whether to include "
            "shortcut to Applications in the DMG disk image",
        ),
        ("silent", "s", "suppress all output except warnings"),
    ]

    def initialize_options(self) -> None:
        self.volume_label = self.distribution.get_fullname()
        self.applications_shortcut = False
        self.silent = None

    def finalize_options(self) -> None:
        if self.silent is None:
            self.silent = False

    def build_dmg(self) -> None:
        # Remove DMG if it already exists
        if os.path.exists(self.dmg_name):
            os.unlink(self.dmg_name)

        # Make dist folder
        self.dist_dir = os.path.join(self.build_dir, "dist")
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        self.mkpath(self.dist_dir)

        # Copy App Bundle
        dest_dir = os.path.join(
            self.dist_dir, os.path.basename(self.bundle_dir)
        )
        if self.silent:
            shutil.copytree(self.bundle_dir, dest_dir, symlinks=True)
        else:
            self.copy_tree(self.bundle_dir, dest_dir, preserve_symlinks=True)

        createargs = [
            "hdiutil",
            "create",
        ]
        if self.silent:
            createargs += ["-quiet"]
        createargs += [
            "-fs",
            "HFSX",
            "-format",
            "UDZO",
            self.dmg_name,
            "-imagekey",
            "zlib-level=9",
            "-srcfolder",
            self.dist_dir,
            "-volname",
            self.volume_label,
        ]

        if self.applications_shortcut:
            apps_folder_link = os.path.join(self.dist_dir, "Applications")
            os.symlink(
                "/Applications", apps_folder_link, target_is_directory=True
            )

        # Create the dmg
        if subprocess.call(createargs) != 0:
            msg = "creation of the dmg failed"
            raise OSError(msg)

    def run(self) -> None:
        # Create the application bundle
        self.run_command("bdist_mac")

        # Find the location of the application bundle and the build dir
        self.bundle_dir = self.get_finalized_command("bdist_mac").bundle_dir
        self.build_dir = self.get_finalized_command("build_exe").build_base

        # Set the file name of the DMG to be built
        self.dmg_name = os.path.join(
            self.build_dir, self.volume_label + ".dmg"
        )

        self.execute(self.build_dmg, ())
