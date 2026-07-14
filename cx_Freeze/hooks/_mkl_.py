"""Hooks triggered by finder when mkl package is included."""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze._metadata import DistributionCache
from cx_Freeze.exception import ModuleError
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


# The sample/pandas is used to test using the following:
#
# - Ubuntu 22.04 w/ Python 3.10 and numpy+mkl
# pip install -i https://pypi.anaconda.org/intel/simple numpy
#
# - Windows w/ Python 3.10 to 3.12 using cgohlke/numpy-mkl-wheels
# Download: https://github.com/cgohlke/numpy-mkl-wheels/releases/


class Hook(ModuleHook):
    """The Hook class for mkl."""

    def mkl(self, finder: ModuleFinder, module: Module) -> None:
        finder.exclude_module("mkl.tests")

        distribution = module.distribution
        if distribution and distribution.installer == "pip":
            target_dir = f"lib/{module.name}.libs"
            for file in distribution.binary_files:
                source = distribution.locate_file(file)
                target = f"{target_dir}/{source.name}"
                finder.lib_files[source] = target
                finder.include_files(source, target)
            for req_name in distribution.requires:
                with suppress(ModuleError):
                    req_dist = DistributionCache(req_name, finder)
                    for file in req_dist.binary_files:
                        source = distribution.locate_file(file)
                        target = f"{target_dir}/{source.name}"
                        finder.lib_files[source] = target
                        finder.include_files(source, target)
