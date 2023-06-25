import sys
from datetime import datetime


def say_hello():
    print("Hello from cx_Freeze")
    print(f"The current date is {datetime.today():%B %d, %Y %H:%M:%S}\n")

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
    say_hello()
