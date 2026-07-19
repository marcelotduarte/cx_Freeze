"""Tests for hooks of stdlib ssl."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_MACOS

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15

if IS_MACOS:
    mac_extra_test = pytest.mark.parametrize(
        "mac_extra_test", [False, True], ids=["", "mac_extra_test"]
    )
else:
    mac_extra_test = pytest.mark.parametrize(
        "mac_extra_test", [False], ids=[""]
    )
zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST_SSL = """
test_ssl.py
    import http.client
    import os
    import ssl

    print("Hello from cx_Freeze")
    print(ssl.__name__, "using", ssl.OPENSSL_VERSION)
    ssl_paths = ssl.get_default_verify_paths()
    print("cafile:",ssl_paths.cafile)
    print("openssl_cafile:", ssl_paths.openssl_cafile)
    print("SSL_CERT_FILE:", os.environ.get("SSL_CERT_FILE"))

    conn = http.client.HTTPSConnection("github.com")
    conn.request("GET", "/marcelotduarte/cx_Freeze")
    print("Host:", conn.host)
    r1 = conn.getresponse()
    print("Status:", r1.status, r1.reason)
pyproject.toml
    [project]
    name = "test_ssl"
    version = "0.1.2.3"

    [tool.cxfreeze]
    executables = ["test_ssl.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""


@pytest.mark.parametrize(
    "use_os_cert_file", [False, True], ids=["", "SSL_CERT_FILE"]
)
@mac_extra_test
@zip_packages
def test_ssl(
    tmp_package: TempPackage,
    zip_packages: bool,
    mac_extra_test: bool,
    use_os_cert_file: bool,
) -> None:
    """Test that the ssl is working correctly."""
    tmp_package.create(SOURCE_TEST_SSL)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    if mac_extra_test:
        tmp_package.freeze("cxfreeze bdist_mac")
        name = "test_ssl"
        version = "0.1.2.3"
        bundle_name = f"{name}-{version}"
        build_app_dir = tmp_package.path / "build" / f"{bundle_name}.app"
        executable = build_app_dir / "Contents/MacOS/test_ssl"
    else:
        tmp_package.freeze()
        executable = tmp_package.executable("test_ssl")
    assert executable.is_file()
    env = os.environ.copy()
    if use_os_cert_file:
        ssl_paths = __import__("ssl").get_default_verify_paths()
        cert_file = ssl_paths.cafile
        if cert_file is None or not os.path.exists(cert_file):
            cert_file = ssl_paths.openssl_cafile
        if cert_file and os.path.exists(cert_file):
            env["SSL_CERT_FILE"] = cert_file
    result = tmp_package.run(executable, env=env)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "ssl using *",
            "cafile: *",
            "openssl_cafile: *",
            "SSL_CERT_FILE: *",
            "Host: *",
            "Status: 200 OK",
        ]
    )
