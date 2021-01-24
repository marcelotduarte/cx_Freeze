"""
Distutils script for cx_Freeze.
"""

from setuptools import setup, Extension
import distutils.command.build_ext
from distutils.sysconfig import get_config_var
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
        os.environ["LD_RUN_PATH"] = "${ORIGIN}/../lib:${ORIGIN}/lib"
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


def find_cx_logging():
    cxfreeze_dir = os.path.dirname(os.path.abspath(__file__))
    logging_dir = os.path.join(cxfreeze_dir, "cx_Logging")
    try:
        subprocess.run(
            ["git", "submodule", "init", "cx_Logging"], cwd=cxfreeze_dir
        )
        subprocess.run(
            ["git", "submodule", "update", "cx_Logging"], cwd=cxfreeze_dir
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    if not os.path.exists(logging_dir):
        return None, None
    platform = distutils.util.get_platform()
    ver_major, ver_minor = sys.version_info[0:2]
    sub_dir = f"implib.{platform}-{ver_major}.{ver_minor}"
    import_library_dir = os.path.join(logging_dir, "build", sub_dir)
    include_dir = os.path.join(logging_dir, "src")
    if not os.path.exists(import_library_dir):
        try:
            subprocess.run(
                [sys.executable, "setup.py", "build"], cwd=logging_dir
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    if not os.path.exists(import_library_dir):
        return None, None
    return include_dir, import_library_dir


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
        include_dir, library_dir = find_cx_logging()
        if include_dir is not None:
            service = Extension(
                "cx_Freeze.bases.Win32Service",
                ["source/bases/Win32Service.c"],
                depends=depends,
                library_dirs=[library_dir],
                libraries=libraries + ["advapi32", "cx_Logging"],
                include_dirs=[include_dir],
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
    for filename in os.listdir(os.path.join("cx_Freeze", "samples")):
        sample_dir = os.path.join("cx_Freeze", "samples", filename)
        if not os.path.isdir(sample_dir):
            continue
        package_data.append(f"samples/{filename}/*.py")

    setup(
        cmdclass={"build_ext": build_ext},
        options={"install": {"optimize": 1}},
        ext_modules=extensions,
        packages=["cx_Freeze"],
        package_data={"cx_Freeze": package_data},
    )
