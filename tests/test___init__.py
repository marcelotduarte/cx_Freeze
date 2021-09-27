import pytest
import sys


@pytest.mark.parametrize(
    "platform_modules", [
        (None, []),
        ("win32", ["bdist_msi"]),
        ("darwin", ["bdist_dmg", "bdist_mac"]),
        ("linux", [])
    ]
)
def test_exposed_namespaces(mocker, platform_modules):
    """ This test asserts that all the namespaces that should be exposed when `importing cx_Freeze` are available """

    if "cx_Freeze" in sys.modules:  # Flush if already there ( from another test )
        del sys.modules['cx_Freeze']
    if platform_modules[0]:  # Mock platform before import :)
        mocker.patch.object(sys, "platform", platform_modules[0])
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

    if platform_modules[0]:
        for ns in platform_modules[1]:
            assert ns in dir(cx_Freeze)
