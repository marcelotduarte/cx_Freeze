# A setup script to demonstrate build using cffi (inside a cryptography pkg)
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])
executables = [Executable("test_crypt.py")]

setup(name='test_crypt',
      version='0.1',
      description='cx_Freeze script to test cryptography',
      executables=executables,
      options=dict(build_exe=buildOptions))
