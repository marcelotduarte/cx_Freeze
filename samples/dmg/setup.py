"""A very simple setup script to create a single executable.

hello.py is a very simple 'Hello, world' type script which also displays the
environment in which the script runs.

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the script without Python
"""

from cx_Freeze import Executable, setup

executables = [
    Executable(
        script="hello.py",
        # You can also specify an icon for the executable that will be reused for the dmg
        # only the first executable is used for the icon
        # icon="../../cx_Freeze/icons/python.icns" #noqa: ERA001
    )
]

setup(
    name="hello",
    version="0.1.2.3",
    description="Sample cx_Freeze script",
    executables=executables,
    options={
        "bdist_mac": {
            "bundle_name": "hello",
        },
        "bdist_dmg": {
            "applications_shortcut": True,
            "volume_label": "Howdy Yall",
            "background": "builtin-arrow",
            "license": {
                "default-language": "en_US",
                "licenses": {"en_US": "Do it right, do it legal, do it safe."},
                "buttons": {
                    "en_US": [
                        "English",
                        "Agree",
                        "Disagree",
                        "Print",
                        "Save",
                        "If you agree, click Agree to continue the installation. If you do not agree, click Disagree to cancel the installation.",
                    ]
                },
            },
        },
    },
)
