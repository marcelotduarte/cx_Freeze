#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys

print('Hello from cx_Freeze')
print('The current date is {}\n'.format(
             datetime.today().strftime('%B %d, %Y %H:%M:%S')))

print('Executable: {}'.format(sys.executable))
print('Prefix: {}'.format(sys.prefix))
print('Default encoding: {}'.format(sys.getdefaultencoding()))
print('File system encoding: {}\n'.format(sys.getfilesystemencoding()))

print('ARGUMENTS:')
for a in sys.argv:
    print('{}'.format(a))
print('')

print('PATH:')
for p in sys.path:
    print('{}'.format(p))
print()

