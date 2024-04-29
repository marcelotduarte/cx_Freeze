import sys
from datetime import datetime, timezone

import BUILD_CONSTANTS

today = datetime.now(tz=timezone.utc)
print("Hello from cx_Freeze")
print(f"The current date is {today:%B %d, %Y %H:%M:%S}\n")

print(f"Executable: {sys.executable}")
print(f"Prefix: {sys.prefix}")
print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"File system encoding: {sys.getfilesystemencoding()}\n")

print("ARGUMENTS:")
for arg in sys.argv:
    print(f"{arg}")
print()

print("PATH:")
for path in sys.path:
    print(f"{path}")
print()

print(f"Executable: {sys.executable!r}\n")


excluded_vars = [
    "__builtins__",
    "__cached__",
    "__doc__",
    "__loader__",
    "__package__",
    "__spec__",
]

print("== variables in BUILD_CONSTANTS ==\n")
for var in dir(BUILD_CONSTANTS):
    if var in excluded_vars:
        continue
    attr = BUILD_CONSTANTS.__getattribute__(var)
    print(f"{var} = {attr!r}")
