"""
cx_Freeze command line tool (enable python -m cx_Freeze syntax)
"""

import sys


def main():  # needed for console script
    if __package__ == "":
        # To be able to run 'python cx_Freeze-6.*.whl/cxfreeze':
        import os.path

        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    import cx_Freeze.cli

    sys.exit(cx_Freeze.cli.main())


if __name__ == "__main__":
    sys.exit(main())
