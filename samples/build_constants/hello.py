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

excluded_vars = [
    "__builtins__",
    "__cached__",
    "__doc__",
    "__file__",
    "__loader__",
    "__name__",
    "__package__",
    "__spec__",
]

print("BUILD_CONSTANTS variables:")
for var in dir(BUILD_CONSTANTS):
    if var in excluded_vars:
        continue
    attr = getattr(BUILD_CONSTANTS, var)
    print(f"{var} = {attr!r}")
print()

print("ARGUMENTS:")
for arg in sys.argv:
    print(f"{arg}")
print()

print("PATH:")
for path in sys.path:
    print(f"{path}")
print()
