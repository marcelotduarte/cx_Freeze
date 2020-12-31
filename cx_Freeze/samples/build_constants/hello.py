#!/usr/bin/env python

from datetime import datetime
import sys

print("Hello from cx_Freeze")
print(
    "The current date is %s\n"
    % datetime.today().strftime("%B %d, %Y %H:%M:%S")
)

print(f"Executable: {sys.executable!r}\n")

import BUILD_CONSTANTS

excludedVars = [
    "__builtins__",
    "__cached__",
    "__doc__",
    "__loader__",
    "__package__",
    "__spec__",
]

print("== variables in BUILD_CONSTANTS ==\n")
for var in dir(BUILD_CONSTANTS):
    if var in excludedVars:
        continue
    attr = BUILD_CONSTANTS.__getattribute__(var)
    print(f"{var} = {attr!r}")
