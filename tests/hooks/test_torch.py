"""Tests for hooks of torch."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from cx_Freeze import ConstantsModule, ModuleFinder

if TYPE_CHECKING:
    from tests.conftest import TempPackage

# A minimal stand-in for the torch package: just the modules that the hook
# includes explicitly, plus the module that imports unittest at runtime.
SOURCE_FAKE_TORCH = """
torch/__init__.py
    from torch.utils import _config_module
torch/_C.py
    pass
torch/_VF.py
    pass
torch/return_types.py
    pass
torch/distributions/__init__.py
    pass
torch/testing/__init__.py
    pass
torch/utils/__init__.py
    pass
torch/utils/_config_module.py
    import unittest
    from unittest import mock
"""


def test_torch_includes_unittest(tmp_package: TempPackage) -> None:
    """Test that the torch hook includes unittest (a default exclude)."""
    tmp_package.create(SOURCE_FAKE_TORCH)
    finder = ModuleFinder(
        ConstantsModule(), path=[os.fspath(tmp_package.path), *sys.path]
    )
    try:
        finder.include_module("torch")
        names = {module.name for module in finder.modules}
    finally:
        finder.cleanup()
    assert "torch.utils._config_module" in names
    assert "unittest" in names
    assert "unittest.mock" in names
