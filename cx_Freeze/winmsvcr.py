"""DLL list of MSVC runtimes.

Extracted from:
    https://github.com/conda-forge/vc-feedstock/blob/main/recipe/meta.yaml

"""

from __future__ import annotations

MSVC_FILES = (
    # VC 2015 and 2017
    "concrt140.dll",
    "msvcp140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "vcamp140.dll",
    "vccorlib140.dll",
    "vcomp140.dll",
    "vcruntime140.dll",
    # VS 2019
    "msvcp140_atomic_wait.dll",
    "msvcp140_codecvt_ids.dll",
    "vcruntime140_1.dll",
    # VS 2022
    "vcruntime140_threads.dll",
)

UCRT_FILES = (
    "api-ms-win-*.dll",
    "ucrtbase.dll",
)
