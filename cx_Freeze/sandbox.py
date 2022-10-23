"""Extend setuptools.sandbox.run_setup to work with cx_Freeze setup()."""

import contextlib
import os
import sys
from pathlib import Path
from typing import Sequence, Union

import setuptools.sandbox as _sandbox

# pylint: disable-next=protected-access
_sandbox._MODULES_TO_HIDE.update({"cx_Freeze", "msilib"})

__all__ = ["run_setup"]


def run_setup(setup_script: Union[str, Path], args: Sequence):
    """Run a cx_Freeze setup script, sandboxed in its directory."""

    if isinstance(setup_script, Path):
        setup_script = os.fspath(setup_script)
    setup_dir = os.path.abspath(os.path.dirname(setup_script))
    with _setup_context(setup_dir):
        try:
            sys.argv[:] = [setup_script] + list(args)
            sys.path.insert(0, setup_dir)
            with _sandbox.DirectorySandbox(setup_dir):
                env = {"__file__": setup_script, "__name__": "__main__"}
                # pylint: disable-next=protected-access
                _sandbox._execfile(setup_script, env)
        except SystemExit as exc:
            if exc.args and exc.args[0]:
                raise
            # Normal exit, just return


@contextlib.contextmanager
def _setup_context(setup_dir: str):
    """Save and prepare de environment to run_setup."""

    with _sandbox.setup_context(setup_dir):
        # ensure cx_Freeze commands are available
        __import__("cx_Freeze")
        yield
