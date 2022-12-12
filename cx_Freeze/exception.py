"""Internal exception classes."""

from __future__ import annotations

__all__ = ["ConfigError"]


class ConfigError(Exception):
    """Raised when an error is detected in the configuration.
    The associated value is a string indicating what precisely went wrong."""

    def __init__(self, msg: str):
        self.what: str = msg
        super().__init__()

    def __str__(self) -> str:
        return self.what


class DarwinException(Exception):
    """Raied when an error is detected in the module darwintools."""
