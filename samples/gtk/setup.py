from cx_Freeze import setup

options = {
    "build_exe": {
        "excludes": [
            "tkinter",
        ],
    },
}

setup(
    name="gtkapp_sample",
    version="0.1",
    description="Sample cx_Freeze Gtk script",
    executables=["test_gtk.py"],
    options=options,
)
