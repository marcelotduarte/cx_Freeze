# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable that makes use of
# the openpyxl package. This package, like a number of others, makes the
# assumption that it is found in the file system, and so fails miserably if
# it is included in a zip file.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [
    Executable('test_openpyxl.py')
]

setup(name='test_openpyxl',
      version='0.1',
      description='Sample cx_Freeze script testing the use of openpyxl',
      executables=executables
      )
