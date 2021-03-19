# A setup script to demonstrate the use of pyzmq
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

setup(
    name="test_pyzmq",
    version="0.1",
    description="cx_Freeze script to test pyzmq server and client",
    executables=[Executable("pyzmq_server.py"), Executable("pyzmq_client.py")],
    options={
        "build_exe": {"excludes": ["tkinter"]},
    },
)
