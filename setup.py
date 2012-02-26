"""
Distutils script for cx_Freeze.
"""

import cx_Freeze
import distutils.command.bdist_rpm
import distutils.command.build_ext
import distutils.command.build_scripts
import distutils.command.install
import distutils.command.install_data
import distutils.sysconfig
import os
import sys

from distutils.core import setup
from distutils.extension import Extension

CX_LOGGING_TAG = "trunk"

class bdist_rpm(distutils.command.bdist_rpm.bdist_rpm):

    # rpm automatically byte compiles all Python files in a package but we
    # don't want that to happen for initscripts and samples so we tell it to
    # ignore those files
    def _make_spec_file(self):
        specFile = distutils.command.bdist_rpm.bdist_rpm._make_spec_file(self)
        specFile.insert(0, "%define _unpackaged_files_terminate_build 0%{nil}")
        return specFile

    def run(self):
        distutils.command.bdist_rpm.bdist_rpm.run(self)
        specFile = os.path.join(self.rpm_base, "SPECS",
                "%s.spec" % self.distribution.get_name())
        queryFormat = "%{name}-%{version}-%{release}.%{arch}.rpm"
        command = "rpm -q --qf '%s' --specfile %s" % (queryFormat, specFile)
        origFileName = os.popen(command).read()
        parts = origFileName.split("-")
        parts.insert(2, "py%s%s" % sys.version_info[:2])
        newFileName = "-".join(parts)
        self.move_file(os.path.join("dist", origFileName),
                os.path.join("dist", newFileName))


class build_ext(distutils.command.build_ext.build_ext):

    def build_extension(self, ext):
        if ext.name.find("bases") < 0:
            distutils.command.build_ext.build_ext.build_extension(self, ext)
            return
        if sys.platform == "win32":
            if sys.version_info[:2] < (2, 6):
                ext.sources.append("source/bases/dummy.rc")
            elif self.compiler.compiler_type == "mingw32":
                ext.sources.append("source/bases/manifest.rc")
        os.environ["LD_RUN_PATH"] = "${ORIGIN}:${ORIGIN}/../lib"
        objects = self.compiler.compile(ext.sources,
                output_dir = self.build_temp,
                include_dirs = ext.include_dirs,
                debug = self.debug,
                depends = ext.depends)
        fileName = os.path.splitext(self.get_ext_filename(ext.name))[0]
        fullName = os.path.join(self.build_lib, fileName)
        libraryDirs = ext.library_dirs or []
        libraries = self.get_libraries(ext)
        extraArgs = ext.extra_link_args or []
        if sys.platform != "win32":
            vars = distutils.sysconfig.get_config_vars()
            if not vars.get("Py_ENABLE_SHARED", 0):
                libraryDirs.append(vars["LIBPL"])
                libraries.append("python%s.%s" % sys.version_info[:2])
                if vars["LINKFORSHARED"] and sys.platform != "darwin":
                    extraArgs.extend(vars["LINKFORSHARED"].split())
                if vars["LIBS"]:
                    extraArgs.extend(vars["LIBS"].split())
                if vars["LIBM"]:
                    extraArgs.append(vars["LIBM"])
                if vars["BASEMODLIBS"]:
                    extraArgs.extend(vars["BASEMODLIBS"].split())
                if vars["LOCALMODLIBS"]:
                    extraArgs.extend(vars["LOCALMODLIBS"].split())
            extraArgs.append("-s")
        elif ext.name.find("Win32GUI") > 0 \
                and self.compiler.compiler_type == "mingw32":
            extraArgs.append("-mwindows")
        self.compiler.link_executable(objects, fullName,
                libraries = libraries,
                library_dirs = libraryDirs,
                runtime_library_dirs = ext.runtime_library_dirs,
                extra_postargs = extraArgs,
                debug = self.debug)

    def get_ext_filename(self, name):
        fileName = distutils.command.build_ext.build_ext.get_ext_filename(self,
                name)
        if name.endswith("util"):
            return fileName
        vars = distutils.sysconfig.get_config_vars()
        soExt = vars["SO"]
        ext = self.compiler.exe_extension or ""
        return fileName[:-len(soExt)] + ext


class build_scripts(distutils.command.build_scripts.build_scripts):

    def copy_scripts(self):
        distutils.command.build_scripts.build_scripts.copy_scripts(self)
        if sys.platform == "win32":
            for script in self.scripts:
                batFileName = os.path.join(self.build_dir, script + ".bat")
                fullScriptName = r"%s\Scripts\%s" % \
                        (os.path.dirname(sys.executable), script)
                command = "%s %s %%*" % (sys.executable, fullScriptName)
                open(batFileName, "w").write("@echo off\n\n%s" % command)


class install(distutils.command.install.install):

    def get_sub_commands(self):
        subCommands = distutils.command.install.install.get_sub_commands(self)
        subCommands.append("install_packagedata")
        return subCommands


class install_packagedata(distutils.command.install_data.install_data):

    def run(self):
        installCommand = self.get_finalized_command("install")
        installDir = getattr(installCommand, "install_lib")
        sourceDirs = ["samples", "initscripts"]
        while sourceDirs:
            sourceDir = sourceDirs.pop(0)
            targetDir = os.path.join(installDir, "cx_Freeze", sourceDir)
            self.mkpath(targetDir)
            for name in os.listdir(sourceDir):
                if name in ("build", "CVS") or name.startswith("."):
                    continue
                fullSourceName = os.path.join(sourceDir, name)
                if os.path.isdir(fullSourceName):
                    sourceDirs.append(fullSourceName)
                else:
                    fullTargetName = os.path.join(targetDir, name)
                    self.copy_file(fullSourceName, fullTargetName)
                    self.outfiles.append(fullTargetName)


def find_cx_Logging():
    currentDir = os.getcwd()
    dirName, baseName = os.path.split(currentDir)
    parts = [dirName, ".."]
    if baseName != "trunk":
        parts.append("..")
    parts.append("cx_Logging")
    if CX_LOGGING_TAG != "trunk":
        parts.append("tags")
    parts.append(CX_LOGGING_TAG)
    loggingDir = os.path.normpath(os.path.join(*parts))
    if not os.path.exists(loggingDir):
        return
    subDir = "implib.%s-%s" % (distutils.util.get_platform(), sys.version[:3])
    importLibraryDir = os.path.join(loggingDir, "build", subDir)
    if not os.path.exists(importLibraryDir):
        return
    return loggingDir, importLibraryDir


commandClasses = dict(
        build_ext = build_ext,
        build_scripts = build_scripts,
        bdist_rpm = bdist_rpm,
        install = install,
        install_packagedata = install_packagedata)

# generate C source for base frozen modules
subDir = "temp.%s-%s" % (distutils.util.get_platform(), sys.version[:3])
baseModulesDir = os.path.join("build", subDir)
baseModulesFileName = os.path.join(baseModulesDir, "BaseModules.c")
finder = cx_Freeze.ModuleFinder(bootstrap = True)
finder.WriteSourceFile(baseModulesFileName)

# build utility module
if sys.platform == "win32":
    libraries = ["imagehlp"]
else:
    libraries = []
utilModule = Extension("cx_Freeze.util", ["source/util.c"],
        libraries = libraries)

# build base executables
depends = ["source/bases/Common.c"]
fullDepends = depends + [baseModulesFileName]
includeDirs = [baseModulesDir]
console = Extension("cx_Freeze.bases.Console", ["source/bases/Console.c"],
        depends = fullDepends, include_dirs = includeDirs)
consoleKeepPath = Extension("cx_Freeze.bases.ConsoleKeepPath",
        ["source/bases/ConsoleKeepPath.c"], depends = depends)
extensions = [utilModule, console, consoleKeepPath]
if sys.platform == "win32":
    gui = Extension("cx_Freeze.bases.Win32GUI", ["source/bases/Win32GUI.c"],
            include_dirs = includeDirs, depends = fullDepends,
            libraries = ["user32"])
    extensions.append(gui)
    moduleInfo = find_cx_Logging()
    if moduleInfo is not None and sys.version_info[:2] < (3, 0):
        includeDir, libraryDir = moduleInfo
        includeDirs.append(includeDir)
        service = Extension("cx_Freeze.bases.Win32Service",
                ["source/bases/Win32Service.c"], depends = fullDepends,
                library_dirs = [libraryDir],
                libraries = ["advapi32", "cx_Logging"],
                include_dirs = includeDirs)
        extensions.append(service)

docFiles = "LICENSE.txt README.txt HISTORY.txt doc/cx_Freeze.html"

classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: Utilities"
]

setup(name = "cx_Freeze",
        description = "create standalone executables from Python scripts",
        long_description = "create standalone executables from Python scripts",
        version = "4.2.3",
        cmdclass = commandClasses,
        options = dict(bdist_rpm = dict(doc_files = docFiles),
                install = dict(optimize = 1)),
        ext_modules = extensions,
        packages = ['cx_Freeze'],
        maintainer="Anthony Tuininga",
        maintainer_email="anthony.tuininga@gmail.com",
        url = "http://cx-freeze.sourceforge.net",
        scripts = ["cxfreeze"],
        classifiers = classifiers,
        keywords = "freeze",
        license = "Python Software Foundation License")

