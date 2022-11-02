"""
Setuptools script for cx_Freeze.

Use ONE of the following commands to install from source:
    pip install .
    python setup.py build install

Use the following commands to install in the development mode:
    pip install -r requirements-dev.txt
    pip install -e . --no-build-isolation --no-deps

"""
# pylint: disable=attribute-defined-outside-init,missing-function-docstring

import os
import sys
from pathlib import Path
from shutil import which
from subprocess import CalledProcessError, check_call, check_output
from sysconfig import get_config_var, get_platform, get_python_version
from typing import List, Tuple, Union

import setuptools.command.build_ext
from setuptools import Extension, setup
from setuptools.errors import LinkError

WIN32 = sys.platform == "win32"
DARWIN = sys.platform == "darwin"
IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()


class BuildBases(setuptools.command.build_ext.build_ext):
    """Build C bases and extension."""

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
        filename = Path(self.get_ext_filename(ext.name)).with_suffix("")
        fullname = os.fspath(Path(self.build_lib, filename))
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
                    dll_name = dll_path.name
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
            if not bool(get_config_var("Py_ENABLE_SHARED")):
                library_dirs.append(get_config_var("LIBDIR"))
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
        for arg in (None, "--no-lto"):
            if arg:
                extra_args.append(arg)
            try:
                self.compiler.link_executable(
                    objects,
                    fullname,
                    libraries=libraries,
                    library_dirs=library_dirs,
                    runtime_library_dirs=ext.runtime_library_dirs,
                    extra_postargs=extra_args,
                    debug=self.debug,
                )
            except LinkError:
                if WIN32:
                    raise
                continue
            else:
                break

    def get_ext_filename(self, fullname):
        if fullname.endswith("util"):
            return super().get_ext_filename(fullname)
        # Examples of returned names:
        # console-cp37-win32.exe, console-cp39-win_amd64.exe,
        # console-cpython-39-x86_64-linux-gnu, console-cpython-36m-darwin
        ext_path = Path(*fullname.split("."))
        name = ext_path.name
        if WIN32:
            py_version_nodot = get_config_var("py_version_nodot")
            platform_nodot = get_platform().replace(".", "").replace("-", "_")
            soabi = f"cp{py_version_nodot}-{platform_nodot}"
            suffix = ".exe"
        else:
            soabi = get_config_var("SOABI")
            suffix = ""
        name_base = f"{name}-{soabi}"
        return os.fspath(ext_path.parent / (name_base + suffix))

    @staticmethod
    def _get_dll_path(name: str) -> Path:
        """Find the dll by name, priority by pyd extension."""
        pattern_pyd = f"{name}*.pyd"
        pattern_dll = f"{name}*.dll"
        for path in sys.path:
            path = Path(path).resolve()
            if not path.is_dir():
                continue
            for dll_path in path.glob(pattern_pyd):
                return dll_path
            for dll_path in path.glob(pattern_dll):
                return dll_path
        return Path(f"{name}.dll")

    def _dlltool_delay_load(self, name: str) -> Tuple[str, str]:
        """Get the delay load library to use with mingw32 gcc/clang compiler"""
        dir_name = f"libdl.{get_platform()}-{get_python_version()}"
        library_dir = Path(self.build_temp, dir_name)
        library_dir.mkdir(parents=True, exist_ok=True)
        # Use gendef and dlltool to generate the library (.a and .delay.a)
        dll_path = self._get_dll_path(name)
        gendef_exe = Path(which("gendef"))
        def_data = check_output(_make_strs([gendef_exe, "-", dll_path]))
        def_name = library_dir / f"{name}.def"
        def_name.write_bytes(def_data)
        lib_path = library_dir / f"lib{name}.a"
        library = f"{name}.delay"
        dlb_path = library_dir / f"lib{library}.a"
        dlltool_exe = gendef_exe.parent / "dlltool.exe"
        dlltool = [dlltool_exe, "-d", def_name, "-D", dll_path, "-l", lib_path]
        output_delaylib_args = ["-y", dlb_path]
        try:
            # GNU binutils dlltool support --output-delaylib
            check_call(_make_strs(dlltool + output_delaylib_args))
        except CalledProcessError:
            # LLVM dlltool only supports generating an import library
            check_call(_make_strs(dlltool))
            library = name
        return os.fspath(library_dir), library

    def _copy_libraries_to_bases(self):
        """Copy standard libraries to cx_Freeze wheel, on posix systems, when
        python is compiled with --disable-shared, as is done in manylinux and
        macpython. Modules such as math, _struct and zlib, which are normally
        embedded in python, are compiled separately.
        Also, copies tcl/tk libraries."""
        if WIN32 or IS_CONDA or bool(get_config_var("Py_ENABLE_SHARED")):
            return
        bases = f"{self.build_lib}/cx_Freeze/bases"
        if bool(get_config_var("DESTSHARED")):
            source_path = Path(get_config_var("DESTSHARED"))
            target_path = f"{bases}/lib-dynload"
            self.mkpath(target_path)
            for source in source_path.iterdir():
                self.copy_file(source.as_posix(), target_path)
        # tcl/tk at /usr/share
        try:
            tkinter = __import__("tkinter")
        except (ImportError, AttributeError):
            return
        root = tkinter.Tk(useTk=False)
        # tcl
        source_path = Path(root.tk.exprstring("$tcl_library"))
        target_path = f"{bases}/tcltk/{source_path.name}"
        self.mkpath(target_path)
        for source in source_path.rglob("*"):
            target = os.fspath(target_path / source.relative_to(source_path))
            if source.is_dir():
                self.mkpath(target)
            else:
                self.copy_file(source.as_posix(), target)
        # tk
        source_name = source_path.name.replace("tcl", "tk")
        source_path = source_path.parent / source_name
        target_path = f"{bases}/tcltk/{source_path.name}"
        self.mkpath(target_path)
        for source in source_path.rglob("*"):
            target = os.fspath(target_path / source.relative_to(source_path))
            if source.is_dir():
                self.mkpath(target)
            else:
                self.copy_file(source.as_posix(), target)

    def run(self):
        self._copy_libraries_to_bases()
        super().run()


def _make_strs(paths: List[Union[str, Path]]) -> List[str]:
    """Convert paths to strings for legacy compatibility."""
    if sys.version_info > (3, 8) and not WIN32:
        return paths
    return list(map(os.fspath, paths))


def update_frozen_license():
    """Updates the license text that is incorporated in frozen programs
    (in cx_Freeze/freeze_license/cx_frozen_license.txt) to ensure it is
    in sync with the cx_Freeze license in documentation."""
    srcpath = os.path.join("doc", "src", "license.rst")
    dstpath = os.path.join(
        "cx_Freeze", "initscripts", "frozen_application_license.txt"
    )
    frozen_header = """Why this file is included
=========================

This program has been frozen with cx_Freeze.  The freezing process
resulted in certain components from the cx_Freeze software being included
in the frozen application, in particular bootstrap code for launching
the frozen python script.  The cx_Freeze software is subject to the
license set out below.
"""
    try:
        with open(srcpath, encoding="utf-8") as license_doc:
            content = license_doc.read()
    except (OSError, FileNotFoundError):
        print(
            "** Error reading source license text.  Check that the "
            "license.rst file is included in doc directory. **"
        )
        return
    lines = list(content.splitlines())
    lines = lines[1:]
    content = frozen_header + "\n".join(lines) + "\n"
    try:
        with open(dstpath, "w", encoding="utf-8") as frozen_license_file:
            frozen_license_file.write(content)
    except OSError as io_error:
        print(f"** Error updating frozen license text ({io_error}) **")
        return
    return


if __name__ == "__main__":
    # ensure that the correct license text will be included in
    # frozen applications
    update_frozen_license()

    # build base executables
    depends = ["source/bases/common.c"]
    console = Extension(
        "cx_Freeze.bases.console",
        ["source/bases/console.c"],
        depends=depends,
    )
    extensions = [console]
    if WIN32:
        gui = Extension(
            "cx_Freeze.bases.Win32GUI",
            ["source/bases/Win32GUI.c"],
            depends=depends,
            libraries=["user32"],
        )
        extensions.append(gui)
        service = Extension(
            "cx_Freeze.bases.Win32Service",
            ["source/bases/Win32Service.c"],
            depends=depends,
            extra_link_args=["/DELAYLOAD:cx_Logging"],
            include_dirs=["source/bases"],
            libraries=["advapi32"],
        )
        extensions.append(service)
        # build utility module
        util_module = Extension(
            "cx_Freeze.util",
            ["source/util.c"],
            libraries=["imagehlp", "shlwapi"],
        )
        extensions.append(util_module)

    setup(
        cmdclass={"build_ext": BuildBases},
        options={"install": {"optimize": 1}},
        ext_modules=extensions,
    )
