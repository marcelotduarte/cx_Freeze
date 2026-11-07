"""Hooks triggered by finder when AV (PyAV) package is included."""

from __future__ import annotations

import sys
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

from cx_Freeze.module import ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for AV (pyAV).

    Supported pypi versions (tested from 11.0 to 19.0.2).
    """

    def av(self, finder: ModuleFinder, module: Module) -> None:
        """Hooks for AV (PyAV) package."""
        if module.in_file_system == 0:
            finder.include_package("av")
        with suppress(ImportError):
            finder.include_module("av.deprecation")

        # conda-forge Windows
        source = Path(sys.base_prefix, "Library/bin/SDL3.dll")
        if source.exists():
            target = f"lib/{source.name}"
            finder.lib_files[source] = target
            finder.include_files(source, target)

    def av_audio(self, _finder: ModuleFinder, module: Module) -> None:
        module.global_names.add("_AudioCodecName")

    def av_audio_frame(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names.add("numpy")

    def av_container(
        self,
        finder: ModuleFinder,
        module: Module,  # noqa: ARG002
    ) -> None:
        """Newer version of AV needs uuid."""
        finder.include_module("uuid")

    def av_sidedata_encparams(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.add("numpy")

    def av_sidedata_motionvectors(
        self, _finder: ModuleFinder, module: Module
    ) -> None:
        module.ignore_names.add("numpy")

    def av_subtitles(self, _finder: ModuleFinder, module: Module) -> None:
        module.global_names.add("_SubtitleCodecName")

    def av_video(self, _finder: ModuleFinder, module: Module) -> None:
        module.global_names.add("_VideoCodecName")

    def av_video_frame(self, _finder: ModuleFinder, module: Module) -> None:
        module.ignore_names.add("numpy")
