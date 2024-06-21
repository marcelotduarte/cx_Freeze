"""Implements the 'bdist_dmg' command (create macOS dmg and/or app bundle)."""

from __future__ import annotations

import os
import shutil
from typing import ClassVar

from dmgbuild import build_dmg
from setuptools import Command

import cx_Freeze.icons
from cx_Freeze import Executable
from cx_Freeze.exception import OptionError

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
            "If defined, specifies the size of the filesystem within the image. "
            "If this is not defined, cx_Freeze (and then dmgbuild) will attempt to determine a reasonable size for the image. "
            "If you set this, you should set it large enough to hold the files you intend to copy into the image. The syntax is "
            "the same as for the -size argument to hdiutil, i.e. you can use the suffixes `b`, `k`, `m`, `g`, `t`, `p` and `e` for "
            "bytes, kilobytes, megabytes, gigabytes, terabytes, exabytes and petabytes respectively.",
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
            "The position of the window in ((x, y), (w, h)) format, with y co-ordinates running from bottom to top. The Finder "
            " makes sure that the window will be on the user's display, so if you want your window at the top left of the display "
            "you could use (0, 100000) as the x, y co-ordinates. Unfortunately it doesn't appear to be possible to position the "
            "window relative to the top left or relative to the centre of the user's screen.",
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
        self.silent = None
        self.volume_label = self.distribution.get_fullname()
        self.applications_shortcut = False
        self._symlinks = {}
        self._files = []
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
        self.hide = None
        self.hide_extensions = None
        self.icon_locations = None
        self.default_view = None
        self.show_icon_preview = False
        self.license = None

        # Non-exposed options
        self.include_icon_view_settings = "auto"
        self.include_list_view_settings = "auto"
        self.arrange_by = None
        self.grid_offset = None
        self.grid_spacing = None
        self.scroll_position = None
        self.label_pos = None
        self.text_size = None
        self.icon_size = None
        self.list_icon_size = None
        self.list_text_size = None
        self.list_scroll_position = None
        self.list_sort_by = None
        self.list_use_relative_dates = None
        self.list_calculate_all_sizes = None
        self.list_columns = None
        self.list_column_widths = None
        self.list_column_sort_directions = None

    def finalize_options(self) -> None:
        if not self.volume_label:
            msg = "volume-label must be set"
            raise OptionError(msg)
        if self.applications_shortcut:
            self._symlinks["Applications"] = "/Applications"
        if self.silent is None:
            self.silent = False

        self.finalize_dmgbuild_options()

    def finalize_dmgbuild_options(self) -> None:
        if self.background:
            self.background = self.background.strip()
        if self.background == "builtin-arrow" and (
            self.icon_locations or self.window_rect
        ):
            msg = "background='builtin-arrow' cannot be used with icon_locations or window_rect"
            raise OptionError(msg)
        if not self.arrange_by:
            self.arrange_by = None
        if not self.grid_offset:
            self.grid_offset = (0, 0)
        if not self.grid_spacing:
            self.grid_spacing = 100
        if not self.scroll_position:
            self.scroll_position = (0, 0)
        if not self.label_pos:
            self.label_pos = "bottom"
        if not self.text_size:
            self.text_size = 16
        if not self.icon_size:
            self.icon_size = 128

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

        # Add the App Bundle to the list of files
        self._files.append(self.bundle_dir)

        # set the app_name for the application bundle
        app_name = os.path.basename(self.bundle_dir)
        # Set the defaults
        if (
            self.background == "builtin-arrow"
            and not self.icon_locations
            and not self.window_rect
        ):
            self.icon_locations = {
                "Applications": (500, 120),
                app_name: (140, 120),
            }
            self.window_rect = ((100, 100), (640, 380))

        executables = self.distribution.executables  # type: list[Executable]
        executable: Executable = executables[0]
        if len(executables) > 1:
            self.warn(
                "using the first executable as entrypoint: "
                f"{executable.target_name}"
            )
        if executable.icon is None:
            icon_name = "setup.icns"
            icon_source_dir = os.path.dirname(cx_Freeze.icons.__file__)
            self.icon = os.path.join(icon_source_dir, icon_name)
        else:
            self.icon = os.path.abspath(executable.icon)

        with open("settings.py", "w") as f:

            def add_param(name, value) -> None:
                # if value is a string, add quotes
                if isinstance(value, (str)):
                    f.write(f"{name} = '{value}'\n")
                else:
                    f.write(f"{name} = {value}\n")

            # Some fields expect and allow None, others don't
            # so we need to check for None and not add them for
            # the fields that don't allow it

            # Disk Image Settings
            add_param("filename", self.dmg_name)
            add_param("volume_label", self.volume_label)
            add_param("format", self.format)
            add_param("filesystem", self.filesystem)
            add_param("size", self.size)

            # Content Settings
            add_param("files", self._files)
            add_param("symlinks", self._symlinks)
            if self.hide:
                add_param("hide", self.hide)
            if self.hide_extensions:
                add_param("hide_extensions", self.hide_extensions)
            # Only one of these can be set
            if self.icon_locations:
                add_param("icon_locations", self.icon_locations)
            if self.icon:
                add_param("icon", self.icon)
            # We don't need to set this, as we only support icns
            # add param ( "badge_icon", self.badge_icon)

            # Window Settings
            add_param("background", self.background)
            add_param("show_status_bar", self.show_status_bar)
            add_param("show_tab_view", self.show_tab_view)
            add_param("show_pathbar", self.show_path_bar)
            add_param("show_sidebar", self.show_sidebar)
            add_param("sidebar_width", self.sidebar_width)
            if self.window_rect:
                add_param("window_rect", self.window_rect)
            if self.default_view:
                add_param("default_view", self.default_view)

            add_param("show_icon_preview", self.show_icon_preview)
            add_param(
                "include_icon_view_settings", self.include_icon_view_settings
            )
            add_param(
                "include_list_view_settings", self.include_list_view_settings
            )

            # Icon View Settings\
            add_param("arrange_by", self.arrange_by)
            add_param("grid_offset", self.grid_offset)
            add_param("grid_spacing", self.grid_spacing)
            add_param("scroll_position", self.scroll_position)
            add_param("label_pos", self.label_pos)
            if self.text_size:
                add_param("text_size", self.text_size)
            if self.icon_size:
                add_param("icon_size", self.icon_size)
            if self.icon_locations:
                add_param("icon_locations", self.icon_locations)

            # List View Settings
            if self.list_icon_size:
                add_param("list_icon_size", self.list_icon_size)
            if self.list_text_size:
                add_param("list_text_size", self.list_text_size)
            if self.list_scroll_position:
                add_param("list_scroll_position", self.list_scroll_position)
            add_param("list_sort_by", self.list_sort_by)
            add_param("list_use_relative_dates", self.list_use_relative_dates)
            add_param(
                "list_calculate_all_sizes", self.list_calculate_all_sizes
            )
            if self.list_columns:
                add_param("list_columns", self.list_columns)
            if self.list_column_widths:
                add_param("list_column_widths", self.list_column_widths)
            if self.list_column_sort_directions:
                add_param(
                    "list_column_sort_directions",
                    self.list_column_sort_directions,
                )

            # License Settings
            add_param("license", self.license)

        def log_handler(msg: dict[str, str]) -> None:
            if not self.silent:
                loggable = f"{','.join(f'{key}: {value}' for key, value in msg.items())}"
                self.announce(loggable)

        build_dmg(
            self.dmg_name,
            self.volume_label,
            "settings.py",
            callback=log_handler,
        )

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
