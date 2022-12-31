"""Extend setuptools.sandbox.run_setup to work with cx_Freeze setup()."""

from __future__ import annotations

import os
from collections.abc import Sequence
from pathlib import Path

import setuptools.sandbox as _sandbox

# pylint: disable-next=protected-access
_sandbox._MODULES_TO_HIDE.update({"cx_Freeze", "msilib"})

__all__ = ["run_setup"]


def run_setup(setup_script: str | Path, args: Sequence):
    """Run a cx_Freeze setup script, sandboxed in its directory."""

    _sandbox.run_setup(os.fspath(setup_script), list(args))
