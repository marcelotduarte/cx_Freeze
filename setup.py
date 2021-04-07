"""
Distutils script for cx_Freeze.
"""

from setuptools import setup, Extension
import distutils.command.build_ext
from distutils.sysconfig import get_config_var
import glob
import os
import subprocess
import sys

WIN32 = sys.platform == "win32"

if sys.version_info < (3, 6, 0):
    sys.exit("Python3 versions lower than 3.6.0 are not supported.")


class build_ext(distutils.command.build_ext.build_ext):
    def build_extension(self, ext):
        if "bases" not in ext.name:
            super().build_extension(ext)
            return
        if WIN32 and self.compiler.compiler_type == "mingw32":
            ext.sources.append("source/bases/manifest.rc")
        objects = self.compiler.compile(
            ext.sources,
            output_dir=self.build_temp,
            include_dirs=ext.include_dirs,
            debug=self.debug,
            depends=ext.depends,
        )
        filename = os.path.splitext(self.get_ext_filename(ext.name))[0]
        if self.inplace:
            fullname = os.path.join(os.path.dirname(__file__), filename)
        else:
            fullname = os.path.join(self.build_lib, filename)
        library_dirs = ext.library_dirs or []
        libraries = self.get_libraries(ext)
        extra_args = ext.extra_link_args or []
        if WIN32:
            compiler_type = self.compiler.compiler_type
            # support for delay load [windows]
            for arg in extra_args[:]:
                if arg.startswith("/DELAYLOAD:"):
                    lib_name = arg[len("/DELAYLOAD:") :]
                    extra_args.remove(arg)
                    if compiler_type == "msvc":
                        dll_path = self._get_dll_path(lib_name)
                        dll_name = os.path.basename(dll_path)
                        extra_args.append(f"/DELAYLOAD:{dll_name}")
                        if lib_name not in libraries:
                            libraries.append(lib_name)
                        if "delayimp" not in libraries:
                            libraries.append("delayimp")
            if compiler_type == "msvc":
                extra_args.append("/MANIFEST")
            elif compiler_type == "mingw32":
                if "Win32GUI" in ext.name:
                    extra_args.append("-mwindows")
                else:
                    extra_args.append("-mconsole")
                extra_args.append("-municode")
        else:
            library_dirs.append(get_config_var("LIBPL"))
            abiflags = getattr(sys, "abiflags", "")
            ver_major, ver_minor = sys.version_info[0:2]
            libraries.append(f"python{ver_major}.{ver_minor}{abiflags}")
            if get_config_var("LINKFORSHARED") and sys.platform != "darwin":
                extra_args.extend(get_config_var("LINKFORSHARED").split())
            if get_config_var("LIBS"):
                extra_args.extend(get_config_var("LIBS").split())
            if get_config_var("LIBM"):
                extra_args.append(get_config_var("LIBM"))
            if get_config_var("BASEMODLIBS"):
                extra_args.extend(get_config_var("BASEMODLIBS").split())
            if get_config_var("LOCALMODLIBS"):
                extra_args.extend(get_config_var("LOCALMODLIBS").split())
            # fix a bug using macOS on Github Actions
            if "--with-lto" in get_config_var("CONFIG_ARGS"):
                extra_args.append("-flto")
                extra_args.append("-Wl,-export_dynamic")
            else:
                extra_args.append("-s")
            extra_args.append("-Wl,-rpath,$ORIGIN/lib")
            extra_args.append("-Wl,-rpath,$ORIGIN/../lib")
        self.compiler.link_executable(
            objects,
            fullname,
            libraries=libraries,
            library_dirs=library_dirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extra_args,
            debug=self.debug,
        )

    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        if ext_name.endswith("util"):
            return filename
        exe_extension = self.compiler.exe_extension or ""
        return filename[: -len(get_config_var("EXT_SUFFIX"))] + exe_extension

    def _get_dll_path(self, name):
        """find the dll by name, priority by extension"""
        paths = [path for path in sys.path if os.path.isdir(path)]
        dll_path = None
        for path in paths:
            for dll_path in glob.glob(os.path.join(path, f"{name}*.pyd")):
                return dll_path
            for dll_path in glob.glob(os.path.join(path, f"{name}*.dll")):
                return dll_path
        return f"{name}.dll"


def get_cx_logging_h_dir():
    target_path = os.path.join(sys.exec_prefix, "Include", "cx_Logging.h")
    if os.path.exists(target_path):
        return os.path.dirname(target_path)
    return os.path.join(os.path.dirname(__file__), "source", "bases")


if __name__ == "__main__":
    # build base executables
    if WIN32:
        libraries = ["imagehlp", "Shlwapi"]
    else:
        libraries = []
    depends = ["source/bases/Common.c"]
    console = Extension(
        "cx_Freeze.bases.Console",
        ["source/bases/Console.c"],
        depends=depends,
        libraries=libraries,
    )
    extensions = [console]
    if WIN32:
        gui = Extension(
            "cx_Freeze.bases.Win32GUI",
            ["source/bases/Win32GUI.c"],
            depends=depends,
            libraries=libraries + ["user32"],
        )
        extensions.append(gui)
        service = Extension(
            "cx_Freeze.bases.Win32Service",
            ["source/bases/Win32Service.c"],
            depends=depends,
            include_dirs=[get_cx_logging_h_dir()],
            libraries=libraries + ["advapi32", "cx_Logging"],
        )
        extensions.append(service)
        # build utility module
        util_module = Extension(
            "cx_Freeze.util", ["source/util.c"], libraries=libraries
        )
        extensions.append(util_module)

    # define package data
    package_data = []
    for filename in os.listdir(os.path.join("cx_Freeze", "initscripts")):
        name, ext = os.path.splitext(filename)
        if ext != ".py":
            continue
        package_data.append(f"initscripts/{filename}")

    setup(
        cmdclass={"build_ext": build_ext},
        options={"install": {"optimize": 1}},
        ext_modules=extensions,
        packages=["cx_Freeze"],
        package_data={"cx_Freeze": package_data},
    )
