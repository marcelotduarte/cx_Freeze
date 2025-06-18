"""License sync."""

from __future__ import annotations

import sys
from pathlib import Path

FROZEN_HEADER = """\
## Why this file is included

This program has been frozen with cx_Freeze.  The freezing process
resulted in certain components from the cx_Freeze software being included
in the frozen application, in particular bootstrap code for launching
the frozen python script.  The cx_Freeze software is subject to the
license set out below.
"""
ERROR1 = """Error reading source license text.  Check that the license.rst
file is included in doc directory."""
ERROR2 = "Error updating frozen license text"


def update_frozen_license() -> int:
    """Updates the license text that is incorporated in frozen programs.

    Update license in cx_Freeze/initscripts/frozen_application_license.txt
    to ensure it is in sync with the cx_Freeze license in documentation.
    """
    srcpath = Path("LICENSE.md")
    dstpath = Path("cx_Freeze/initscripts/frozen_application_license.txt")
    try:
        content = srcpath.read_text(encoding="utf_8")
    except OSError:
        print(ERROR1, file=sys.stderr)
        return 1
    content = content.replace('\\"', '"').replace("\\'", "'")
    try:
        dstpath.write_text(FROZEN_HEADER + "\n" + content, encoding="utf_8")
        print(dstpath, "ok")
    except OSError as io_error:
        print(ERROR2, f"({io_error}).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # ensure that the correct license text will be included in
    # frozen applications
    sys.exit(update_frozen_license())
