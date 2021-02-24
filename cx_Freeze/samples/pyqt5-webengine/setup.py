import sys
from cx_Freeze import setup, Executable


setup(
    name="PyQt5WebEngineTest",
    version="0.1",
    python_requires=">3.5",
    options={
        "bdist_mac": {
            "bundle_name": "PyQt5WebengineTest"
        }
    },
    executables=[
        Executable("pyqt5-webengine-test.py", target_name="pyqt5-webengine-test")
    ]
)
