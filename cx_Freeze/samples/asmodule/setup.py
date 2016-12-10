# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable built from a module
# which includes an executable section protected by "if __name__ == '__main__'
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [
    Executable('asmodule.py')
]

setup(name='asmodule',
      version='0.1',
      description='Sample cx_Freeze script',
      executables=executables
      )
