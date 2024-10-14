"""A simple setup script to create executables using scipy."""

# test_scipy.py is a very simple scipy application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

from cx_Freeze import setup

setup(
    name="scipy_samples",
    version="0.1",
    description="Sample scipy script",
    executables=["test_scipy.py"],
)
