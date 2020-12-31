#!/usr/bin/env python

from datetime import datetime
import sys

print("Hello from cx_Freeze")
print(f"The current date is {datetime.today():%B %d, %Y %H:%M:%S}\n")

print(f"Executable: {sys.executable}")
print(f"Prefix: {sys.prefix}")
print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"File system encoding: {sys.getfilesystemencoding()}\n")

print("ARGUMENTS:")
for a in sys.argv:
    print(f"{a}")
print()

print("PATH:")
for p in sys.path:
    print(f"{p}")
print()
