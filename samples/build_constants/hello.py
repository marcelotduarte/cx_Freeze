#!/usr/bin/env python

from __future__ import annotations

import sys
from datetime import datetime

import BUILD_CONSTANTS

print("Hello from cx_Freeze")
print(
    "The current date is %s\n"
    % datetime.today().strftime("%B %d, %Y %H:%M:%S")
)

print(f"Executable: {sys.executable!r}\n")


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
