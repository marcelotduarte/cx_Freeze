#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
from sys import stdout

stdout.write('Hello from cx_Freeze\n')
stdout.write('The current date is %s\n\n' %
             datetime.today().strftime('%B %d, %Y %H:%M:%S'))

stdout.write('Executable: %r\n' % sys.executable)
stdout.write('Prefix: %r\n' % sys.prefix)
stdout.write('Default encoding: %r\n' % sys.getdefaultencoding())
stdout.write('File system encoding: %r\n\n' % sys.getfilesystemencoding())


import BUILD_CONSTANTS

excludedVars = ["__builtins__", "__cached__", "__doc__", "__loader__", "__package__", "__spec__"]

print("== variables in BUILD_CONSTANTS ==\n")
for var in dir(BUILD_CONSTANTS):
    if var in excludedVars: continue
    print("{} = {}".format(var, repr(BUILD_CONSTANTS.__getattribute__(var))))
