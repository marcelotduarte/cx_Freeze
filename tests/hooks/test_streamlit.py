"""Tests for hooks of streamlit."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import ABI_THREAD, IS_MINGW

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)
SOURCE_TEST = """
test_streamlit.py
    import sys
    import streamlit

    streamlit.header("Hello from cx_Freeze")
    streamlit.write(f"streamlit version {streamlit.__version__}")
pyproject.toml
    [project]
    name = "test_streamlit"
    version = "0.1.2.3"
    dependencies = ["streamlit"]

    [[tool.cxfreeze.executables]]
    script = "test_streamlit.py"
    init_script = "streamlit"

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="streamlit not supported in mingw",
    strict=True,
)
@pytest.mark.skipif(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    reason="streamlit does not support Python 3.13t/3.14t",
)
@pytest.mark.venv
@zip_packages
def test_streamlit(tmp_package, zip_packages: bool) -> None:
    """Test if streamlit hook is working correctly."""
    tmp_package.create(SOURCE_TEST)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_streamlit")
    assert executable.is_file()
    result = tmp_package.run(
        [
            executable,
            "--server.showEmailPrompt=false",
            "--browser.gatherUsageStats=false",
        ],
        timeout=TIMEOUT,
        raise_on_timeout=False,
    )
    result.stdout.fnmatch_lines(
        ["*You can now view your Streamlit app in your browser."]
    )
