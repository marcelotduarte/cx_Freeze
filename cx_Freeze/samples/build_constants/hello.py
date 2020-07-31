#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys

print('Hello from cx_Freeze')
print('The current date is %s\n' %
             datetime.today().strftime('%B %d, %Y %H:%M:%S'))

print('Executable: %r\n' % sys.executable)

import BUILD_CONSTANTS

excludedVars = ["__builtins__", "__cached__", "__doc__", "__loader__", "__package__", "__spec__"]

print("== variables in BUILD_CONSTANTS ==\n")
for var in dir(BUILD_CONSTANTS):
    if var in excludedVars: continue
    print("{} = {}".format(var, repr(BUILD_CONSTANTS.__getattribute__(var))))
