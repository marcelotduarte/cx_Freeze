"""
Setuptools script for cx_Freeze.

Use one of the following commands to install:
    pip install .
    python setup.py build install
Use one of the following commands to use the development mode:
    pip install -e .
    python setup.py develop
"""

import glob
import os
import subprocess
import sys
from sysconfig import get_config_var, get_platform, get_python_version

from setuptools import setup, Command, Extension
import setuptools.command.build_ext

WIN32 = sys.platform == "win32"
DARWIN = sys.platform == "darwin"

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
                    dll_path = self._get_dll_path(lib_name)
                    dll_name = os.path.basename(dll_path)
                    if compiler_type == "msvc":
                        extra_args.append(f"/DELAYLOAD:{dll_name}")
                        if lib_name not in libraries:
                            libraries.append(lib_name)
                        if "delayimp" not in libraries:
                            libraries.append("delayimp")
                    elif compiler_type == "mingw32":
                        if lib_name in libraries:
                            libraries.remove(lib_name)
                        lib_dir, library = self._dlltool_delay_load(lib_name)
                        for linker_option in self.compiler.linker_exe:
                            if "clang" in linker_option:
                                extra_args.append(f"-Wl,-delayload,{dll_name}")
                                break
                        if get_platform().startswith("mingw_i686"):  # mingw32
                            # disable delay load to avoid a Segmentation fault
                            libraries.append(lib_name)
                        else:
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
            abiflags = get_config_var("abiflags")
            libraries.append(f"python{get_python_version()}{abiflags}")
            if get_config_var("LINKFORSHARED") and not DARWIN:
                extra_args.extend(get_config_var("LINKFORSHARED").split())
            if get_config_var("LIBS"):
                extra_args.extend(get_config_var("LIBS").split())
            if get_config_var("LIBM"):
                extra_args.append(get_config_var("LIBM"))
            if get_config_var("BASEMODLIBS"):
                extra_args.extend(get_config_var("BASEMODLIBS").split())
            if get_config_var("LOCALMODLIBS"):
                extra_args.extend(get_config_var("LOCALMODLIBS").split())
            if DARWIN:
                # macOS on Github Actions
                extra_args.append("-Wl,-export_dynamic")
            else:
                if not self.debug:
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
        py_version_nodot = get_config_var("py_version_nodot")
        platform_nodot = get_platform().replace(".", "")
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
        """Get the delay load library to use with mingw32 gcc/clang compiler"""
        dir_name = f"libdl.{get_platform()}-{get_python_version()}"
        library_dir = os.path.join(self.build_temp, dir_name)
        os.makedirs(library_dir, exist_ok=True)
        # Use gendef and dlltool to generate the library (.a and .delay.a)
        dll_path = self._get_dll_path(name)
        def_name = os.path.join(library_dir, f"{name}.def")
        def_data = subprocess.check_output(["gendef", "-", dll_path])
        with open(def_name, "wb") as def_file:
            def_file.write(def_data)
        lib_path = os.path.join(library_dir, f"lib{name}.a")
        library = f"{name}.delay"
        dlb_path = os.path.join(library_dir, f"lib{library}.a")
        dlltool = ["dlltool", "-d", def_name, "-D", dll_path, "-l", lib_path]
        output_delaylib_args = ["-y", dlb_path]
        try:
            # GNU binutils dlltool support --output-delaylib
            subprocess.check_call(dlltool + output_delaylib_args)
        except subprocess.CalledProcessError:
            # LLVM dlltool only supports generating an import library
            subprocess.check_call(dlltool)
            library = name
        return library_dir, library

    def run(self):
        self.run_command("install_include")
        super().run()


class install_include(Command):
    def initialize_options(self):
        self.install_dir = None
        self.outfiles = []

    def finalize_options(self):
        self.set_undefined_options(
            "install",
            ("install_data", "install_dir"),
        )

    def run(self):
        if WIN32:
            target_dir = os.path.join(self.install_dir, "include")
            target_file_name = os.path.join(target_dir, "cx_Logging.h")
            if os.path.isfile(target_file_name):
                return
            self.mkpath(target_dir)
            self.copy_file("source\\bases\\cx_Logging.h", target_file_name)
            self.outfiles.append(target_file_name)


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
        cmdclass={"build_ext": build_ext, "install_include": install_include},
        options={"install": {"optimize": 1}},
        ext_modules=extensions,
        packages=["cx_Freeze"],
        package_data={"cx_Freeze": package_data},
    )
