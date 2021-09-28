import pytest
import sys


@pytest.mark.parametrize(
    "platform, extra_modules", [
        (None, []),
        ("win32", ["bdist_msi"]),
        ("darwin", ["bdist_dmg", "bdist_mac"]),
        ("linux", [])
    ]
)
def test_exposed_namespaces(mocker, platform, extra_modules):
    """ This test asserts that all the namespaces that should be exposed when `importing cx_Freeze` are available """

    if "cx_Freeze" in sys.modules:  # Flush if already there ( from another test )
        del sys.modules['cx_Freeze']
    if platform:  # Mock platform before import :)
        mocker.patch.object(sys, "platform", platform)
    import cx_Freeze

    expected_namespaces = [  # This namespaces are there regardless of platform
        "bdist_rpm",
        "build",
        "build_exe",
        "install",
        "install_exe",
        "setup",
        "ConfigError",
        "ConstantsModule",
        "Executable",
        "Freezer",
        "Module",
        "ModuleFinder",
    ]
    for ns in expected_namespaces:
        assert ns in dir(cx_Freeze)

    if platform:
        for ns in extra_modules:
            assert ns in dir(cx_Freeze)
