"""Test exceptions."""

from __future__ import annotations

import pytest

from cx_Freeze.exception import ConfigError, DarwinException


@pytest.mark.parametrize("custom_exception", [ConfigError, DarwinException])
def test_raise_exceptions(custom_exception):
    """This method tests that exceptions can be raised + caught and the __str__
    value is correctly called"""
    try:
        raise custom_exception("Something Bad Happened")
    except custom_exception as err:
        print(str(err))  # Force invokation of the __str__ method
