"""Tests for hooks of crypto packages."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD, IS_MINGW

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_ARGON2 = """
test_argon2.py
    from argon2 import PasswordHasher

    ph = PasswordHasher()
    hash = ph.hash("correct horse battery staple")

    print("Hello from cx_Freeze")
    print("argon2 hash:", hash)
pyproject.toml
    [project]
    name = "test_argon2"
    version = "0.1.2.3"
    dependencies = ["argon2-cffi"]

    [tool.cxfreeze]
    executables = ["test_argon2.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    sys.version_info[:2] == (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="argon2-cffi does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_argon2(tmp_package, zip_packages) -> None:
    """Test if argon2-cffi is working correctly."""
    tmp_package.map_package_to_mingw["argon2-cffi"] = "python-argon2_cffi"
    tmp_package.create(SOURCE_ARGON2)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_argon2")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "argon2 hash: *"])


SOURCE_BCRYPT = """
test_bcrypt.py
    import bcrypt

    print("Hello from cx_Freeze")
    print("bcrypt gensalt:", bcrypt.gensalt())
pyproject.toml
    [project]
    name = "test_bcrypt"
    version = "0.1.2.3"
    dependencies = [
        "bcrypt<4;python_version < '3.11'",
        "bcrypt>=4;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_bcrypt.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_bcrypt(tmp_package, zip_packages) -> None:
    """Test if bcrypt is working correctly."""
    tmp_package.create(SOURCE_BCRYPT)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_bcrypt")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "bcrypt gensalt: *"])


SOURCE_CRYPTO = """
test_crypto.py
    from Crypto.PublicKey import RSA

    secret_code = "Unguessable"  # noqa: S105
    key = RSA.generate(2048)
    encrypted_key = key.export_key(
        passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC"
    )
    with open("rsa_key.bin", "wb") as file_out:
        file_out.write(encrypted_key)

    print("Hello from cx_Freeze")
    print("cryptodome publickey:", key.publickey().export_key().decode())
pyproject.toml
    [project]
    name = "test_crypto"
    version = "0.1.2.3"
    dependencies = ["pycryptodome"]

    [tool.cxfreeze]
    executables = ["test_crypto.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 14) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pycryptodome does not support Python 3.14t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_crypto(tmp_package, zip_packages) -> None:
    """Test if pycryptodome is working correctly."""
    tmp_package.create(SOURCE_CRYPTO)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_crypto")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "cryptodome publickey:*"]
    )


SOURCE_CRYPTOGRAPHY = """
test_cryptography.py
    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(b"A really secret message. Not for prying eyes.")

    print("Hello from cx_Freeze")
    print("cryptography fernet token:", token)
pyproject.toml
    [project]
    name = "test_cryptography"
    version = "0.1.2.3"
    dependencies = ["cryptography"]

    [tool.cxfreeze]
    executables = ["test_cryptography.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    sys.version_info[:2] == (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="cryptography does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_cryptography(tmp_package, zip_packages) -> None:
    """Test if cryptography is working correctly."""
    tmp_package.create(SOURCE_CRYPTOGRAPHY)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_cryptography")
    assert executable.is_file()
    if IS_MINGW:
        tmp_package.monkeypatch.setenv("CRYPTOGRAPHY_OPENSSL_NO_LEGACY", "1")
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "cryptography fernet token: *"]
    )
