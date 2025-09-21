"""License sync."""

from __future__ import annotations

import importlib.metadata
from typing import TYPE_CHECKING

from cx_Freeze.exception import FileError

if TYPE_CHECKING:
    from pathlib import Path
FROZEN_HEADER = """## Why this file is included

This program has been frozen with cx_Freeze.  The freezing process
resulted in certain components from the cx_Freeze software being included
in the frozen application, in particular bootstrap code for launching
the frozen python script.  The cx_Freeze software is subject to the
license set out below.
"""
ERROR0 = "Unable to find license for frozen application."
ERROR1 = "Error reading source license text."
ERROR2 = "Error updating frozen license text"


def frozen_license(path: Path) -> Path:
    """Generate a text file of the license added to frozen programs.

    path: must be a directory where the file will be generated.
    """
    dist = importlib.metadata.distribution("freeze_core")
    srcpath = None
    for file in dist.files:
        if file.name == "LICENSE":
            srcpath = file.locate()
            break
    if srcpath is None:
        raise FileError(ERROR0)

    try:
        content = srcpath.read_text(encoding="utf_8")
    except OSError:
        raise FileError(ERROR1) from None

    dstpath = path / "frozen_application_license.txt"
    try:
        dstpath.write_text(FROZEN_HEADER + "\n" + content, encoding="utf_8")
    except OSError:
        raise FileError(ERROR2) from None
    return dstpath
