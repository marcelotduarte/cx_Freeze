import sys
from datetime import datetime

print("Hello from cx_Freeze")
print(f"The current date is {datetime.today():%B %d, %Y %H:%M:%S}\n")

print(f"Executable: {sys.executable}")
print(f"Prefix: {sys.prefix}")
print(f"Default encoding: {sys.getdefaultencoding()}")
print(f"File system encoding: {sys.getfilesystemencoding()}\n")
if sys.platform == "win32":
    winver = sys.getwindowsversion()
    print(f"Windows version: {winver.major}.{winver.minor}\n")

print("ARGUMENTS:")
for arg in sys.argv:
    print(f"{arg}")
print()

print("PATH:")
for path in sys.path:
    print(f"{path}")
print()
