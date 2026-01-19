"""Tests for hooks of streamlit."""

from __future__ import annotations

import subprocess

import pytest

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
    try:
        result = tmp_package.run(executable, timeout=TIMEOUT)
    except subprocess.TimeoutExpired as exc:
        result = pytest.RunResult(
            -9,
            exc.output.decode().splitlines(),
            exc.stderr and exc.stderr.decode().splitlines(),
            0,
        )
    result.stdout.fnmatch_lines(
        ["*You can now view your Streamlit app in your browser."]
    )
