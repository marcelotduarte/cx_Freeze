"""Tests for hooks of pydantic."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_PYDANTIC = """
test_pydantic.py
    import pydantic

    print("Hello from cx_Freeze")
    print("pydantic version", pydantic.__version__)

    # https://github.com/pydantic/pydantic?tab=readme-ov-file#a-simple-example
    from datetime import datetime

    from pydantic import BaseModel


    class User(BaseModel):
        id: int
        name: str = "John Doe"
        signup_ts: datetime | None = None
        friends: list[int] = []


    external_data = {
        "id": "123",
        "signup_ts": "2017-06-01 12:22",
        "friends": [1, "2", b"3"],
    }
    user = User(**external_data)
    print(user)
    print(user.id)
pyproject.toml
    [project]
    name = "test_pydantic"
    version = "0.1.2.3"
    dependencies = ["pydantic==2.13.0b2"]

    [tool.cxfreeze]
    executables = ["test_pydantic.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    sys.version_info[:2] == (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pydantic_core does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_pydantic(tmp_package, zip_packages: bool) -> None:
    """Test if pydantic hook is working correctly."""
    tmp_package.create(SOURCE_TEST_PYDANTIC)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()
    executable = tmp_package.executable("test_pydantic")
    assert executable.is_file()
    result = tmp_package.run(executable)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "pydantic version *",
            "id=123 name='John Doe' "
            "signup_ts=datetime.datetime(2017, 6, 1, 12, 22) "
            "friends=[1, 2, 3]",
            "123",
        ]
    )
