"""A collection of functions which are triggered automatically by finder when
mkl package is included.
"""

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING

from cx_Freeze.exception import ModuleError
from cx_Freeze.module import DistributionCache

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

# The sample/pandas is used to test using the following:
#
# - Ubuntu 22.04 w/ Python 3.10 and numpy+mkl
# pip install -i https://pypi.anaconda.org/intel/simple numpy
#
# - Windows w/ Python 3.9 to 3.12 using cgohlke/numpy-mkl-wheels
# Download: https://github.com/cgohlke/numpy-mkl-wheels/releases/


def load_mkl(finder: ModuleFinder, module: Module) -> None:
    """The mkl package."""
    distribution = module.distribution
    if distribution and distribution.installer == "pip":
        for file in distribution.binary_files:
            source = file.locate().resolve()
            finder.include_files(source, f"lib/mkl/{source.name}")
        for req_name in distribution.requires:
            with suppress(ModuleError):
                req_dist = DistributionCache(finder.cache_path, req_name)
                for file in req_dist.binary_files:
                    source = file.locate().resolve()
                    finder.include_files(source, f"lib/mkl/{source.name}")
