"""Extend setuptools.sandbox.run_setup to work with cx_Freeze setup()."""

import contextlib
import sys
from pathlib import Path
from typing import Union

from setuptools.sandbox import (
    DirectorySandbox,
    override_temp,
    pushd,
    save_argv,
    save_path,
)

__all__ = ["run_setup"]


def run_setup(setup_script: Union[str, Path], args):
    """Run a cx_Freeze setup script, sandboxed in its directory."""

    fullpath = Path(setup_script).resolve()
    setup_dir = str(fullpath.parent)
    setup_script = str(fullpath)
    with _setup_context(setup_dir):
        try:
            sys.argv[:] = [setup_script] + list(args)
            sys.path.insert(0, setup_dir)
            with DirectorySandbox(setup_dir):
                env = {"__file__": setup_script, "__name__": "__main__"}
                _execfile(setup_script, env)
        except SystemExit as exc:
            if exc.args and exc.args[0]:
                raise
            # Normal exit, just return


@contextlib.contextmanager
def _setup_context(setup_dir: str):
    """Save and prepare de environment to run_setup."""

    temp_dir = str(Path(setup_dir, "temp"))
    with save_path():
        with save_argv():
            with override_temp(temp_dir):
                with pushd(setup_dir):
                    # ensure cx_Freeze commands are available
                    # __import__("cx_Freeze")
                    yield


# pylint: disable-next=redefined-builtin
def _execfile(filename: str, globals, locals=None):
    """Python 3 implementation of execfile."""

    script = Path(filename).read_bytes()
    if locals is None:
        locals = globals
    code = compile(script, filename, "exec")
    exec(code, globals, locals)  # pylint: disable=exec-used
