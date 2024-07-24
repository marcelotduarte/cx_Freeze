"""The internal _importlib module."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 10, 2):
    from importlib import metadata
else:
    import importlib_metadata as metadata

__all__ = ["metadata"]
