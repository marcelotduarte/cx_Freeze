"""
cx_Freeze command line tool (enable python -m cx_Freeze syntax)
"""

import sys
import cx_Freeze.cli

if __name__ == "__main__":
    sys.exit(cx_Freeze.cli.main())
