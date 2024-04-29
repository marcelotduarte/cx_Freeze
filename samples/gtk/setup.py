import os
import sys

from cx_Freeze import Executable, setup

include_files = []
dll_search_paths = os.getenv("PATH", os.defpath).split(os.pathsep)
required_dlls = [
    "libgtk-3-0.dll",
    "libgdk-3-0.dll",
    "libepoxy-0.dll",
    "libgdk_pixbuf-2.0-0.dll",
    "libpango-1.0-0.dll",
    "libpangocairo-1.0-0.dll",
    "libpangoft2-1.0-0.dll",
    "libpangowin32-1.0-0.dll",
    "libatk-1.0-0.dll",
]

for dll in required_dlls:
    dll_path = None
    for p in dll_search_paths:
        p = os.path.join(p, dll)
        if os.path.isfile(p):
            dll_path = p
            break
    assert (
        dll_path is not None
    ), f"Unable to locate {dll} in {dll_search_paths}"
    include_files.append((dll_path, dll))

required_gi_namespaces = [
    "Atk-1.0",
    "GLib-2.0",
    "GModule-2.0",
    "GObject-2.0",
    "Gdk-3.0",
    "GdkPixbuf-2.0",
    "Gio-2.0",
    "Gtk-3.0",
    "Pango-1.0",
    "cairo-1.0",
    "HarfBuzz-0.0",
    "freetype2-2.0",
]

for ns in required_gi_namespaces:
    subpath = f"lib/girepository-1.0/{ns}.typelib"
    fullpath = os.path.join(sys.prefix, subpath)
    assert os.path.isfile(fullpath), f"Required file {fullpath} is missing"
    include_files.append((fullpath, subpath))

options = {
    "build_exe": {
        "packages": ["gi"],
        "include_files": include_files,
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
