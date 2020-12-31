# A setup script to demonstrate the use of complex importlib machinery at work
#
# Each of these samples (server_simple.py, web_srv.py and wsgiserver.py) are
# acquired from GitHub via the get_examples.py script and stored for
# convenience.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

buildOptions = dict(zip_include_packages=["*"], zip_exclude_packages=[])
executables = [
    Executable("server_simple.py"),
    Executable("web_srv.py"),
    Executable("wsgiserver.py"),
]

setup(
    name="test_importlib",
    version="0.1",
    description="cx_Freeze script for web servers that test importlib",
    executables=executables,
    options=dict(build_exe=buildOptions),
)
