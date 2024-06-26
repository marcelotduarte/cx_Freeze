from cx_Freeze import Executable, setup

options = {
    "build_exe": {
        "excludes": [
            "tkinter",
        ],
    },
}

executables = [Executable("test_gtk.py")]

setup(
    name="gtkapp_sample",
    version="0.1",
    description="Sample cx_Freeze Gtk script",
    executables=executables,
    options=options,
)
