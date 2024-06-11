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
        ("format=", None, "format of the disk image (default: UDZO)"),
        ("filesystem=", None, "filesystem of the disk image (default: HFS+)"),
        (
            "size=",
            None,
            "If defined, specifies the size of the filesystem within the image. If this is not defined, cx_Freeze (and then dmgbuild) will attempt to determine a reasonable size for the image. "
            "If you set this, you should set it large enough to hold the files you intend to copy into the image. The syntax is the same as for the -size argument to hdiutil, i.e. you can use the suffixes `b`, `k`, `m`, `g`, `t`, `p` and `e` for bytes, kilobytes, megabytes, gigabytes, terabytes, exabytes and petabytes respectively.",
        ),
        (
            "background",
            "b",
            "A rgb color in the form #3344ff, svg "
            "named color like goldenrod, a path to an image, or the words 'builtin-arrow'",
        ),
        (
            "show-status-bar",
            None,
            "Show the status bar in the Finder window. Default is False.",
        ),
        (
            "show-tab-view",
            None,
            "Show the tab view in the Finder window. Default is False.",
        ),
        (
            "show-path-bar",
            None,
            "Show the path bar in the Finder window. Default is False.",
        ),
        (
            "show-sidebar",
            None,
            "Show the sidebar in the Finder window. Default is False.",
        ),
        (
            "sidebar-width",
            None,
            "Width of the sidebar in the Finder window. Default is None.",
        ),
        (
            "window-rect",
            None,
            "Window rectangle in the form x,y,width,height"
            "The position of the window in ((x, y), (w, h)) format, with y co-ordinates running from bottom to top. The Finder makes sure that the window will be on the user's display, so if you want your window at the top left of the display you could use (0, 100000) as the x, y co-ordinates. Unfortunately it doesn't appear to be possible to position the window relative to the top left or relative to the centre of the user's screen.",
        ),
        (
            "icon-locations",
            None,
            "A dictionary specifying the co-ordinates of items in the root directory of the disk image, where the keys are filenames and the values are (x, y) tuples. e.g.:"
            'icon-locations = { "Applications": (100, 100), "README.txt": (200, 100) }',
        ),
        (
            "default-view",
            None,
            'The default view of the Finder window. Possible values are "icon-view", "list-view", "column-view", "coverflow".',
        ),
        (
            "show-icon-preview",
            None,
            "Show icon preview in the Finder window. Default is False.",
        ),
        (
            "license",
            None,
            "Dictionary specifying license details with 'default-language', 'licenses', and 'buttons'."
            "default-language: Language code (e.g., 'en_US') if no matching system language."
            "licenses: Map of language codes to license file paths (e.g., {'en_US': 'path/to/license_en.txt'})."
            "buttons: Map of language codes to UI strings ([language, agree, disagree, print, save, instruction])."
            "Example: {'default-language': 'en_US', 'licenses': {'en_US': 'path/to/license_en.txt'}, 'buttons': {'en_US': ['English', 'Agree', 'Disagree', 'Print', 'Save', 'Instruction text']}}",
        ),
    ]

    def initialize_options(self) -> None:
        self.volume_label = self.distribution.get_fullname()
        self.applications_shortcut = False
        self.silent = None
        self.format = "UDZO"
        self.filesystem = "HFS+"
        self.size = None
        self.background = None
        self.show_status_bar = False
        self.show_tab_view = False
        self.show_path_bar = False
        self.show_sidebar = False
        self.sidebar_width = None
        self.window_rect = None
        self.icon_locations = None
        self.default_view = None
        self.show_icon_preview = False
        self.license = None

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
