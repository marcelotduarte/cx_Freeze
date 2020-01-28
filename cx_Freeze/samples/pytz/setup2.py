'''A setup script to demonstrate build using pytz
   This version requires the zoneinfo in the file system
'''
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import distutils
import sys
import os

from cx_Freeze import setup, Executable

dir_name = "exe.%s-%s.2" % \
        (distutils.util.get_platform(), sys.version[0:3])
build_exe = os.path.join('build', dir_name)

setup(name='test_pytz',
      version='0.2',
      description='cx_Freeze script to test pytz',
      executables=[Executable("test_pytz.py")],
      options={
          'build_exe': {'zip_include_packages': ["*"],
                        'zip_exclude_packages': ["pytz"],
                        'build_exe': build_exe}
          })
