"""Shared fixtures"""

from __future__ import annotations

import os
from pathlib import Path

import pytest


# pylint: disable=redefined-outer-name
@pytest.fixture()
def fix_test_path() -> Path:
    """This fixture returns the root of the test folder"""
    return Path(__file__).resolve().parent


@pytest.fixture()
def fix_test_samples_path(fix_test_path: Path) -> Path:
    """This fixture returns the samples folder for the tests"""
    return fix_test_path / "samples"


@pytest.fixture()
def fix_test_samples_dir(fix_test_samples_path: Path) -> str:
    """This fixture returns the samples folder for the tests"""
    return os.fspath(fix_test_samples_path)


@pytest.fixture()
def fix_main_samples_path(fix_test_path: Path) -> Path:
    """This fixture returns the cx_Freeze samples folder"""
    return fix_test_path.parent.joinpath("samples").resolve()
