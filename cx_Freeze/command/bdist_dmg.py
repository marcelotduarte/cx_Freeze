"""Implements the 'bdist_dmg' command (create macOS dmg and/or app bundle)."""

from __future__ import annotations

from optparse import OptionError
import os
import shutil
import subprocess
from typing import ClassVar

from setuptools import Command

import cx_Freeze.icons
from cx_Freeze.exception import ExecError

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
            "named color like goldenrod, a path to an image, or the words 'builtin-arrow'. Default is None.",
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
        if not self.volume_label:
            raise OptionError(msg="volume-label must be set")
        if self.applications_shortcut:
            self._symlinks = {'Applications': '/Applications'}
        if self.silent is None:
            self.silent = False
        if self.background:
            self.background = self.background.strip()

    def finalize_dmgbuild_options(self):
        pass

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

        # executables = self.distribution.executables
        # executable = executables[0]
        # if len(executables) > 1:
        #     self.warn(
        #         "using the first executable as entrypoint: "
        #         f"{executable.target_name}"
        #     )
        # if executable.icon is None:
        #     icon_name = "logox128.png"
        #     icon_source_dir = os.path.dirname(cx_Freeze.icons.__file__)
        #     self.copy_file(os.path.join(icon_source_dir, icon_name), icons_dir)
        # else:
        #     icon_name = executable.icon.name
        #     self.move_file(os.path.join(appdir, icon_name), icons_dir)


        with open("settings.py", "w") as f:
            # Disk Image Settings
            f.write(f"filename = '{self.dmg_name}'\n")
            f.write(f"volume_label = '{self.volume_label}'\n")
            f.write(f"format = '{self.format}'\n")
            f.write(f"filesystem = '{self.filesystem}'\n")
            # f.write(f"size = {self.size}\n")

            # Content Settings
            f.write(f"files = ['{self.dist_dir}']\n")
            f.write(f"symlinks = {self._symlinks}\n")
            # f.write(f"hide = [{self.hide}]\n")
            # f.write(f"hide_extensions = [{self.hide_extensions}]\n")
            if self.icon_locations:
                f.write(f"icon_locations = { self.icon_locations}\n")
            # Only one of these can be set
            # f.write(f"icon = {self.icon}\n")
            # f.write(f"badge_icon = {self.badge_icon}\n")

            # Window Settings
            f.write(f"background = {self.background}\n")
            f.write(f"show_status_bar = {self.show_status_bar}\n")
            f.write(f"show_tab_view = {self.show_tab_view}\n")
            f.write(f"show_pathbar = {self.show_path_bar}\n")
            f.write(f"show_sidebar = {self.show_sidebar}\n")
            f.write(f"sidebar_width = {self.sidebar_width}\n")
            if self.window_rect:
                f.write(f"window_rect = {self.window_rect}\n")
            f.write(f"default_view = {self.default_view}\n")
            f.write(f"show_icon_preview = {self.show_icon_preview}\n")
            # f.write(f"include_icon_view_settings = {self.include_icon_view_settings}\n")
            # f.write(f"include_list_view_settings = {self.include_list_view_settings}\n")

            # Icon View Settings
            # f.write(f"arrange_by = {self.arrange_by}\n")
            # f.write(f"grid_offset = {self.grid_offset}\n")
            # f.write(f"grid_spacing = {self.grid_spacing}\n")
            # f.write(f"scroll_position = {self.scroll_position}\n")
            # f.write(f"label_pos = {self.label_pos}\n")
            # f.write(f"text_size = {self.text_size}\n")
            # f.write(f"icon_size = {self.icon_size}\n")
            if self.icon_locations:
                f.write(f"icon_locations = {self.icon_locations}\n")

            # List View Settings
            # f.write(f"list_icon_size = {self.list_icon_size}\n")
            # f.write(f"list_text_size = {self.list_text_size}\n")
            # f.write(f"list_scroll_position = {self.list_scroll_position}\n")
            # f.write(f"list_sort_by = {self.list_sort_by}\n")
            # f.write(f"list_use_relative_dates = {self.list_use_relative_dates}\n")
            # f.write(f"list_calculate_all_sizes = {self.list_calculate_all_sizes}\n")
            # f.write(f"list_columns = {self.list_columns}\n")
            # f.write(f"list_column_widths = {self.list_column_widths}\n")
            # f.write(f"list_column_sort_directions = {self.list_column_sort_directions}\n")

            # License Settings
            f.write(f"license = {self.license}\n")

        print('\n\n\n\n')
        dmgargs = ['dmgbuild', '-s', 'settings.py', self.volume_label, self.dmg_name]

        # Create the dmg
        if subprocess.call(dmgargs) != 0:
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
