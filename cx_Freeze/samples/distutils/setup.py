# A setup script to demonstrate the use of distutils
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])
executables = [Executable("test_dist.py")]

setup(
    name="test_dist",
    version="0.1",
    description="cx_Freeze script to test distutils",
    executables=executables,
    options=dict(build_exe=buildOptions),
)
