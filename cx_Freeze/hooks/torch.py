"""A collection of functions which are triggered automatically by finder when
PyTorch package is included.
"""

from __future__ import annotations

import os

from ..finder import ModuleFinder
from ..module import Module

# 1) Test in Windows from pypi
# pip install torch
#
# 2) Test in Windows from pytorch
# set PIP_FIND_LINKS=https://download.pytorch.org/whl/cu117/torch_stable.html
# pip install torch==1.13.1+cu117
#
# 3) Test in Linux from pypi includes nvidia packages
# pip install torch


def load_torch(finder: ModuleFinder, module: Module) -> None:
    """Hook for PyTorch. Tested in Windows and Linux."""
    # Activate an optimized mode when torch is in zip_include_packages
    if module.in_file_system == 0:
        module.in_file_system = 2
    # patch the code to ignore CUDA_PATH_Vxx_x installation directory
    code_string = module.file.read_text(encoding="utf-8")
    code_string = code_string.replace("CUDA_PATH", "NO_CUDA_PATH")
    module.code = compile(code_string, os.fspath(module.file), "exec")
    # include the shared libraries in 'lib' to avoid searching through the
    # system.
    source_lib = module.file.parent / "lib"
    target_lib = f"lib/{module.name}/lib"
    if source_lib.exists():
        for source in source_lib.glob("*.dll"):
            finder.include_files(source, f"{target_lib}/{source.name}")
    # hidden modules
    finder.include_module("torch._C")
    finder.include_module("torch._VF")
    finder.include_package("torch.distributions")
    finder.include_package("torch.testing")
    # exclude C files
    finder.exclude_module("torch.include")
    finder.exclude_module("torch.share")
    finder.exclude_module("torch.share")
    finder.exclude_module("torchgen.packaged.ATen.templates")
