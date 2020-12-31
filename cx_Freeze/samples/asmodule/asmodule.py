#!/usr/bin/env python

from datetime import datetime
import sys


def SayHello():
    print("Hello from cx_Freeze")
    print(
        "The current date is {}\n".format(
            datetime.today().strftime("%B %d, %Y %H:%M:%S")
        )
    )

    print(f"Executable: {sys.executable}")
    print(f"Prefix: {sys.prefix}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}\n")

    print("ARGUMENTS:")
    for a in sys.argv:
        print(f"{a}")
    print("")

    print("PATH:")
    for p in sys.path:
        print(f"{p}")
    print()
    return


if __name__ == "__main__":
    SayHello()
