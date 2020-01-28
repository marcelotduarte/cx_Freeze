# A setup script to demonstrate the use of pillow
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])
executables = [Executable("test_pillow.py")]

setup(name='test_pillow',
      version='0.1',
      description='cx_Freeze script to test pillow (PIL)',
      executables=executables,
      options=dict(build_exe=buildOptions))
