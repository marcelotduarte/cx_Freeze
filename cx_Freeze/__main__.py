"""
cx_Freeze command line tool (enable python -m cx_Freeze syntax)
"""

import sys

if __name__ == "__main__":
    import cx_Freeze.cli
    sys.exit(cx_Freeze.cli.main())
