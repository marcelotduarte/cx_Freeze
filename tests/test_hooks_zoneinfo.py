"""Tests for cx_Freeze.hooks.zoneinfo."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from pathlib import Path


SOURCE = """
test_tz.py
    from datetime import datetime, timezone
    from zoneinfo import TZPATH, ZoneInfo, available_timezones

    RFC1123 = "%a, %d %b %Y %H:%M:%S %z"

    print("TZPATH:", TZPATH)
    print("Available timezones:", len(available_timezones()))

    utc_time = datetime.now(timezone.utc)
    print("UTC time:", utc_time.strftime(RFC1123))

    tz1 = ZoneInfo("America/Sao_Paulo")
    brz_time = utc_time.astimezone(tz1)
    print("Brazil time:", brz_time.strftime(RFC1123))

    tz2 = ZoneInfo("US/Eastern")
    eas_time = utc_time.astimezone(tz2)
    print("US Eastern time:", eas_time.strftime(RFC1123))
command
    cxfreeze --script test_tz.py build_exe --excludes=tkinter --silent
"""


@pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)
def test_tz(tmp_path: Path, zip_packages: bool) -> None:
    """Test if zoneinfo hook is working correctly."""
    create_package(tmp_path, SOURCE)
    if zip_packages:
        with tmp_path.joinpath("command").open("a") as f:
            f.write(" --zip-include-packages=* --zip-exclude-packages=")
    output = run_command(tmp_path)
    if "? tzdata imported from zoneinfo_hook" in output:
        pytest.skip(reason="tzdata must be installed")

    executable = tmp_path / BUILD_EXE_DIR / f"test_tz{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(tmp_path, executable, timeout=10)
    lines = output.splitlines()
    assert lines[0].startswith("TZPATH")
    assert lines[1].startswith("Available")
    assert lines[2].startswith("UTC")
    assert lines[3].startswith("Brazil")
    assert lines[4].startswith("US")
