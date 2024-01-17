"""Test winmsvcr."""
from __future__ import annotations

import sys

import pytest

from cx_Freeze.winmsvcr import FILES

EXPECTED = (
    "api-ms-win-*.dll",
    # VC 2015 and 2017
    "concrt140.dll",
    "msvcp140_1.dll",
    "msvcp140_2.dll",
    "msvcp140.dll",
    "ucrtbase.dll",
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


@pytest.mark.skipif(sys.platform != "win32", reason="Windows tests")
def test_files():
    """Test winmsvcr.FILES."""
    assert EXPECTED == FILES
