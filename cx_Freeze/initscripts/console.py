"""Initialization script for cx_Freeze. Sets the attribute sys.frozen so that
modules that expect it behave as they should.
"""

from __future__ import annotations

import importlib.util
import sys

sys.frozen = True


def run(name) -> None:
    """Execute the main script of the frozen application."""
    spec = importlib.util.find_spec(name)
    code = spec.loader.get_code(name)
    main_module = sys.modules["__main__"]
    main_globals = main_module.__dict__
    main_globals.update(
        __cached__=spec.cached,
        __file__=spec.cached,
        __loader__=spec.loader,
        __spec__=spec,
    )
    exec(code, main_globals)
