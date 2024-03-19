"""Test 'import cx_Freeze'."""

from __future__ import annotations

import sys

import pytest

import cx_Freeze


@pytest.mark.parametrize(
    ("platform", "extra_modules"),
    [
        (None, []),
        ("win32", ["bdist_msi"]),
        ("darwin", ["bdist_dmg", "bdist_mac"]),
        ("linux", ["bdist_appimage", "bdist_deb", "bdist_rpm"]),
    ],
)
def test_exposed_namespaces(platform, extra_modules) -> None:
    """Test asserts all the namespaces that should be exposed when
    `importing cx_Freeze` are available.
    """
    # These namespaces are there regardless of platform
    expected_namespaces = [
        "build_exe",
        "install",
        "install_exe",
        "setup",
        "ConstantsModule",
        "Executable",
        "Freezer",
        "Module",
        "ModuleFinder",
    ]
    for ens in expected_namespaces:
        assert ens in dir(cx_Freeze)

    if platform == sys.platform:
        for ens in extra_modules:
            assert ens in dir(cx_Freeze)
