"""
Distutils script for cx_Freeze.
"""

from setuptools import setup, Extension
import distutils.command.build_ext
from distutils.sysconfig import get_config_var
import os
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
        fileName = os.path.splitext(self.get_ext_filename(ext.name))[0]
        if self.inplace:
            fullName = os.path.join(os.path.dirname(__file__), fileName)
        else:
            fullName = os.path.join(self.build_lib, fileName)
        libraryDirs = ext.library_dirs or []
        libraries = self.get_libraries(ext)
        extraArgs = ext.extra_link_args or []
        if WIN32:
            compiler_type = self.compiler.compiler_type
            if compiler_type == "msvc":
                extraArgs.append("/MANIFEST")
            elif compiler_type == "mingw32":
                if "Win32GUI" in ext.name:
                    extraArgs.append("-mwindows")
                else:
                    extraArgs.append("-mconsole")
                extraArgs.append("-municode")
        else:
            libraryDirs.append(get_config_var("LIBPL"))
            abiflags = getattr(sys, "abiflags", "")
            libraries.append(
                "python%s.%s%s"
                % (sys.version_info[0], sys.version_info[1], abiflags)
            )
            if get_config_var("LINKFORSHARED") and sys.platform != "darwin":
                extraArgs.extend(get_config_var("LINKFORSHARED").split())
            if get_config_var("LIBS"):
                extraArgs.extend(get_config_var("LIBS").split())
            if get_config_var("LIBM"):
                extraArgs.append(get_config_var("LIBM"))
            if get_config_var("BASEMODLIBS"):
                extraArgs.extend(get_config_var("BASEMODLIBS").split())
            if get_config_var("LOCALMODLIBS"):
                extraArgs.extend(get_config_var("LOCALMODLIBS").split())
            # fix a bug using macOS on Github Actions #812
            # PY_LDFLAGS_NODIST = "-flto -Wl,-export_dynamic -g"
            if get_config_var("PY_LDFLAGS_NODIST"):
                extraArgs.extend(get_config_var("PY_LDFLAGS_NODIST").split())
            else:
                extraArgs.append("-s")
        self.compiler.link_executable(
            objects,
            fullName,
            libraries=libraries,
            library_dirs=libraryDirs,
            runtime_library_dirs=ext.runtime_library_dirs,
            extra_postargs=extraArgs,
            debug=self.debug,
        )

    def get_ext_filename(self, name):
        fileName = super().get_ext_filename(name)
        if name.endswith("util"):
            return fileName
        soExt = get_config_var("EXT_SUFFIX")
        ext = self.compiler.exe_extension or ""
        return fileName[: -len(soExt)] + ext


def find_cx_Logging():
    import subprocess

    dirName = os.path.dirname(
        os.path.dirname(os.path.os.path.abspath(__file__))
    )
    loggingDir = os.path.join(dirName, "cx_Logging")
    if not os.path.exists(loggingDir):
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/anthony-tuininga/cx_Logging.git",
                    loggingDir,
                ]
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    if not os.path.exists(loggingDir):
        return
    subDir = "implib.{}-{}".format(
        distutils.util.get_platform(), sys.version[:3]
    )
    importLibraryDir = os.path.join(loggingDir, "build", subDir)
    includeDir = os.path.join(loggingDir, "src")
    if not os.path.exists(importLibraryDir):
        try:
            subprocess.run(
                [sys.executable, "setup.py", "install"], cwd=loggingDir
            )
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
    if not os.path.exists(importLibraryDir):
        return
    return includeDir, importLibraryDir


commandClasses = {"build_ext": build_ext}

# build base executables
if WIN32:
    libraries = ["imagehlp", "Shlwapi"]
else:
    libraries = []
options = {"install": {"optimize": 1}}
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
    moduleInfo = find_cx_Logging()
    if moduleInfo is not None:
        includeDir, libraryDir = moduleInfo
        service = Extension(
            "cx_Freeze.bases.Win32Service",
            ["source/bases/Win32Service.c"],
            depends=depends,
            library_dirs=[libraryDir],
            libraries=libraries + ["advapi32", "cx_Logging"],
            include_dirs=[includeDir],
        )
        extensions.append(service)
    # build utility module
    utilModule = Extension(
        "cx_Freeze.util", ["source/util.c"], libraries=libraries
    )
    extensions.append(utilModule)

# define package data
packageData = []
for fileName in os.listdir(os.path.join("cx_Freeze", "initscripts")):
    name, ext = os.path.splitext(fileName)
    if ext != ".py":
        continue
    packageData.append("initscripts/%s" % fileName)
for fileName in os.listdir(os.path.join("cx_Freeze", "samples")):
    dirName = os.path.join("cx_Freeze", "samples", fileName)
    if not os.path.isdir(dirName):
        continue
    packageData.append("samples/%s/*.py" % fileName)

setup(
    cmdclass=commandClasses,
    options=options,
    ext_modules=extensions,
    packages=["cx_Freeze"],
    package_data={"cx_Freeze": packageData},
)
