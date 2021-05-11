"""
Distutils script for cx_Freeze.
"""

from setuptools import setup, Extension
import setuptools.command.build_ext
import distutils.util
from distutils.sysconfig import get_config_var
import glob
import os
import subprocess
import sys
import sysconfig

WIN32 = sys.platform == "win32"

if sys.version_info < (3, 6, 0):
    sys.exit("Python3 versions lower than 3.6.0 are not supported.")


class build_ext(setuptools.command.build_ext.build_ext):
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
                    elif compiler_type == "mingw32":
                        if lib_name in libraries:
                            libraries.remove(lib_name)
                        lib_dir, library = self._dlltool_delay_load(lib_name)
                        libraries.append(library)
                        library_dirs.append(lib_dir)
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
        if ext_name.endswith("util"):
            return super().get_ext_filename(ext_name)
        # Examples of returned names:
        # Console-cp37-win32.exe, Console-cp39-win-amd64.exe,
        # Console-cp38-linux-x86_64
        ext_path = ext_name.split(".")
        py_version_nodot = sysconfig.get_config_var("py_version_nodot")
        platform_nodot = sysconfig.get_platform().replace(".", "")
        name_suffix = f"-cp{py_version_nodot}-{platform_nodot}"
        exe_extension = ".exe" if WIN32 else ""
        return os.path.join(*ext_path) + name_suffix + exe_extension

    @staticmethod
    def _get_dll_path(name):
        """Find the dll by name, priority by extension."""
        paths = [path for path in sys.path if os.path.isdir(path)]
        dll_path = None
        for path in paths:
            for dll_path in glob.glob(os.path.join(path, f"{name}*.pyd")):
                return dll_path
            for dll_path in glob.glob(os.path.join(path, f"{name}*.dll")):
                return dll_path
        return f"{name}.dll"

    def _dlltool_delay_load(self, name):
        """Get the delay load library to use with mingw32 gcc compiler"""
        platform = distutils.util.get_platform()
        ver_major, ver_minor = sys.version_info[0:2]
        dir_name = f"libdl.{platform}-{ver_major}.{ver_minor}"
        library_dir = os.path.join(self.build_temp, dir_name)
        os.makedirs(library_dir, exist_ok=True)
        # Use gendef and dlltool to generate the delay library
        dll_path = self._get_dll_path(name)
        def_name = os.path.join(library_dir, f"{name}.def")
        def_data = subprocess.check_output(["gendef", "-", dll_path])
        with open(def_name, "wb") as def_file:
            def_file.write(def_data)
        lib_path = os.path.join(library_dir, f"lib{name}.a")
        dlb_path = os.path.join(library_dir, f"lib{name}-dl.a")
        subprocess.check_call(
            [
                "dlltool",
                "--input-def",
                def_name,
                "--dllname",
                dll_path,
                "--output-lib",
                lib_path,
                "--output-delaylib",
                dlb_path,
            ]
        )
        return library_dir, f"{name}-dl"


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
            extra_link_args=["/DELAYLOAD:cx_Logging"],
            libraries=libraries + ["advapi32"],
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
