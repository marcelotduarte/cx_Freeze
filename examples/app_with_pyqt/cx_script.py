
from cx_Freeze import setup, Executable
from util import getQtPluginIncludes

PACKAGENAME = "TEST"

INCLUDE_QT = True  # whether to include certain PyQT-related files


# force the inclusion of certain plugins that cx-freeze cannot find on its own
requiredPlugins = [
    "styles/libqmacstyle.dylib",
    "sqldrivers/libqsqlite.dylib",
    "printsupport/libcocoaprintersupport.dylib"
]

if not INCLUDE_QT: requiredPlugins = []
include_files = []

include_files += getQtPluginIncludes(pluginList=requiredPlugins)

keyFiles = []

build_options = {"build_exe":"cx_build/",  # subdirectory to do build in
                 "build_base": "cx_build_dists"  # subdirectory to place .app and .dmg packages in
                 }
# Cause the PyQt5 to be included in the package in the old way (only specifically required files).
# This makes the package *much* smaller.
zip_include_packages = ["PyQt5"]
extraPackages = ["PyQt5.sip"]  # force PyQt5.sip to be included.

if not INCLUDE_QT:
    zip_include_packages = []
    extraPackages = []


build_exe_options = { "include_files": include_files,
                      "zip_include_packages": zip_include_packages,
                      "packages": extraPackages,
                      }

bdist_mac_options = {
    "bundle_name": "Test",
}

bdist_dmg_options = {
    "volume_label": PACKAGENAME,
}

exe = Executable(script = "test_script.py")

setup(  name = "Test application",
        author = "[author]",
        maintainer = "[maintainer]",
        maintainer_email = "[email]",
        options = {"build":build_options, "build_exe" : build_exe_options, "bdist_mac": bdist_mac_options,
                   "bdist_dmg": bdist_dmg_options},
        executables = [exe]
        )
