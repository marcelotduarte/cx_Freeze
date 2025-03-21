"""Setuptools script for cx_Freeze.

Use the following commands to install in the development mode:
    pip install -r requirements.txt -r requirements-dev.txt
    pip install -e. --no-build-isolation --no-deps

Documentation:
    https://cx-freeze.readthedocs.io/en/stable/development/index.html
"""

from __future__ import annotations

import contextlib
import os
import sys
from pathlib import Path
from shutil import which
from subprocess import CalledProcessError, check_call, check_output
from sysconfig import get_config_var, get_platform, get_python_version

import setuptools.command.build_ext
from setuptools import Extension, setup
from setuptools.errors import LinkError

ENABLE_SHARED = bool(get_config_var("Py_ENABLE_SHARED"))
PLATFORM = get_platform()
IS_MACOS = PLATFORM.startswith("macos")
IS_MINGW = PLATFORM.startswith("mingw")
IS_WINDOWS = PLATFORM.startswith("win")
IS_CONDA = Path(sys.prefix, "conda-meta").is_dir()


class BuildBases(setuptools.command.build_ext.build_ext):
    """Build C bases and extension."""

    def build_extension(self, ext) -> None:
        if "bases" not in ext.name:
            super().build_extension(ext)
            return
        if IS_MINGW or IS_WINDOWS:
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
        extra_args: list = ext.extra_link_args or []
        if PLATFORM.startswith("freebsd"):
            libraries.append("pthread")
        if IS_MINGW or IS_WINDOWS:
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
                        if PLATFORM.startswith("mingw_i686"):  # mingw32
                            # disable delay load to avoid a Segmentation fault
                            libraries.append(lib_name)
                        else:
                            libraries.append(library)
                        library_dirs.append(lib_dir)
            if compiler_type == "msvc":
                # setuptools adds an option that conflicts with the use of
                # RT_MANIFEST, so remove it to link successfully.
                with contextlib.suppress(ValueError):
                    self.compiler.ldflags_exe.remove("/MANIFEST:EMBED,ID=1")
            elif compiler_type == "mingw32":
                if "Win32GUI" in ext.name:
                    extra_args.append("-mwindows")
                else:
                    extra_args.append("-mconsole")
                extra_args.append("-municode")
        else:
            library_dirs.append(get_config_var("LIBPL"))
            if not ENABLE_SHARED or IS_CONDA:
                library_dirs.append(get_config_var("LIBDIR"))
            abi_thread = get_config_var("abi_thread") or ""
            libraries.append(f"python{get_python_version()}{abi_thread}")
            if get_config_var("LIBS"):
                extra_args.extend(get_config_var("LIBS").split())
            if get_config_var("LIBM"):
                extra_args.append(get_config_var("LIBM"))
            if get_config_var("BASEMODLIBS"):
                extra_args.extend(get_config_var("BASEMODLIBS").split())
            if get_config_var("LOCALMODLIBS"):
                extra_args.extend(get_config_var("LOCALMODLIBS").split())
                # fix for Python 3.12 Ubuntu Linux 24.04 (Noble Nimbat)
                with contextlib.suppress(ValueError):
                    extra_args.remove("Modules/_hacl/libHacl_Hash_SHA2.a")
            if IS_MACOS:
                extra_args.append("-Wl,-export_dynamic")
                extra_args.append("-Wl,-rpath,@loader_path/lib")
            else:
                if get_config_var("LINKFORSHARED"):
                    extra_args.extend(get_config_var("LINKFORSHARED").split())
                extra_args.append("-Wl,-rpath,$ORIGIN/lib")
                extra_args.append("-Wl,-rpath,$ORIGIN/../lib")
                if not self.debug:
                    extra_args.append("-s")
        link_error = None
        for arg in (None, "-fno-lto", "--no-lto"):
            try:
                self.compiler.link_executable(
                    objects,
                    fullname,
                    libraries=libraries,
                    library_dirs=library_dirs,
                    runtime_library_dirs=ext.runtime_library_dirs,
                    extra_postargs=extra_args + ([arg] if arg else []),
                    debug=self.debug,
                )
            except LinkError as exc:
                if IS_MINGW or IS_WINDOWS:
                    raise
                if arg is None:
                    link_error = exc.args
                continue
            else:
                link_error = None
                break
            if link_error is not None:
                raise LinkError from link_error

    def get_ext_filename(self, fullname) -> str:
        if fullname.endswith("util"):
            return super().get_ext_filename(fullname)
        # Examples of returned names:
        # console-cp39-win32.exe, console-cp39-win_amd64.exe,
        # console-cpython-39-x86_64-linux-gnu, console-cpython-39-darwin
        ext_path = Path(*fullname.split("."))
        name = ext_path.name
        soabi = get_config_var("SOABI")
        if soabi is None:  # Python <= 3.12 on Windows
            platform_nodot = PLATFORM.replace(".", "").replace("-", "_")
            soabi = f"{sys.implementation.cache_tag}-{platform_nodot}"
        exe_suffix = get_config_var("EXE")
        return os.fspath(ext_path.parent / f"{name}-{soabi}{exe_suffix}")

    @staticmethod
    def _get_dll_path(name: str) -> Path:
        """Find the dll by name, priority by pyd extension."""
        pattern_pyd = f"{name}*.pyd"
        pattern_dll = f"{name}*.dll"
        for path in map(Path, sys.path):
            if not path.is_dir():
                continue
            for dll_path in path.glob(pattern_pyd):
                return dll_path.resolve()
            for dll_path in path.glob(pattern_dll):
                return dll_path.resolve()
        return Path(f"{name}.dll")

    def _dlltool_delay_load(self, name: str) -> tuple[str, str]:
        """Get the delay load library to use with mingw32 compilers."""
        dir_name = f"libdl.{PLATFORM}-{get_python_version()}"
        library_dir = Path(self.build_temp, dir_name)
        library_dir.mkdir(parents=True, exist_ok=True)
        # Use gendef and dlltool to generate the library (.a and .delay.a)
        dll_path = self._get_dll_path(name)
        gendef_exe = Path(which("gendef"))
        def_data = check_output([gendef_exe, "-", dll_path])
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
            check_call(dlltool + output_delaylib_args)
        except CalledProcessError:
            # LLVM dlltool only supports generating an import library
            check_call(dlltool)
            library = name
        return os.fspath(library_dir), library

    def _copy_libraries_to_bases(self) -> None:
        """Copy standard libraries to cx_Freeze wheel, on posix systems, when
        python is compiled with --disable-shared, as is done in manylinux and
        macpython. Modules such as math, _struct and zlib, which are normally
        embedded in python, are compiled separately.
        Also, copies tcl/tk libraries.
        """
        # copy pre-built bases on Windows (compilation is optional)
        if IS_WINDOWS and not self.inplace:
            for ext in self.extensions:
                source = self.get_ext_filename(ext.name)
                if not os.path.exists(source):
                    continue
                target = f"{self.build_lib}/{source}"
                self.mkpath(os.path.dirname(target))
                self.copy_file(source, target)
            return
        # do not copy libraries in develop mode, Windows, conda, etc
        if self.inplace or IS_MINGW or IS_WINDOWS or IS_CONDA or ENABLE_SHARED:
            return
        # copy only for manylinux and macpython
        bases = f"{self.build_lib}/cx_Freeze/bases"
        ext_suffix = get_config_var("EXT_SUFFIX")
        if bool(get_config_var("DESTSHARED")):
            source_path = Path(get_config_var("DESTSHARED"))
            target_path = f"{bases}/lib-dynload"
            self.mkpath(target_path)
            for source in source_path.glob(f"*{ext_suffix}"):
                self.copy_file(source.as_posix(), target_path)
        # tcl/tk are detected in /usr/local/lib or /usr/share
        try:
            tkinter = __import__("tkinter")
        except ImportError:
            return
        root = tkinter.Tk(useTk=False)
        tcl_library = Path(root.tk.exprstring("$tcl_library"))
        path_to_copy = []
        if tcl_library.name == "Scripts":  # Frameworks on macOS
            tcl_name = f"tcl{tkinter.TclVersion}"
            path_to_copy.append((tcl_library, tcl_name))
            tcl8_name = Path(tcl_name).with_suffix("").name
            path_to_copy.append((tcl_library.parent / tcl8_name, tcl8_name))
            tk_library = Path(tcl_library.as_posix().replace("Tcl", "Tk"))
            path_to_copy.append((tk_library, tcl_name.replace("tcl", "tk")))
        else:
            tcl_name = tcl_library.name
            path_to_copy.append((tcl_library, tcl_name))
            tcl8_path = Path(tcl_library).with_suffix("")
            path_to_copy.append((tcl8_path, tcl8_path.name))
            tk_library = tcl_library.parent / tcl_name.replace("tcl", "tk")
            path_to_copy.append((tk_library, tk_library.name))
        # source paths of tcl8.6, tcl8 and tk8.6
        for source_path, target_name in path_to_copy:
            target_path = f"{bases}/share/{target_name}"
            self.mkpath(target_path)
            for source in source_path.rglob("*"):
                target = os.fspath(
                    target_path / source.relative_to(source_path)
                )
                if source.is_dir():
                    self.mkpath(target)
                else:
                    self.copy_file(source.as_posix(), target)

    def run(self) -> None:
        self._copy_libraries_to_bases()
        super().run()


def get_extensions() -> list[Extension]:
    """Build base executables and util module extension."""
    # [Windows only] With binaries included in bases, the compilation is
    # optional in the development mode.
    optional = IS_WINDOWS and (
        os.environ.get("CI", "") != "true"
        or os.environ.get("CIBUILDWHEEL", "0") != "1"
    )
    abi_thread = get_config_var("abi_thread") or ""
    version = sys.version_info[:2]
    extensions = [
        Extension(
            "cx_Freeze.bases.console",
            ["source/bases/console.c", "source/bases/_common.c"],
            optional=optional,
        )
    ]
    if version < (3, 13):
        extensions += [
            Extension(
                "cx_Freeze.bases.console_legacy",
                ["source/legacy/console.c"],
                depends=["source/legacy/common.c"],
                optional=optional,
            )
        ]
    if IS_MINGW or IS_WINDOWS:
        if version <= (3, 13) and abi_thread == "":
            extensions += [
                Extension(
                    "cx_Freeze.bases.Win32GUI",
                    ["source/legacy/Win32GUI.c"],
                    depends=["source/legacy/common.c"],
                    libraries=["user32"],
                    optional=optional,
                ),
                Extension(
                    "cx_Freeze.bases.Win32Service",
                    ["source/legacy/Win32Service.c"],
                    depends=["source/legacy/common.c"],
                    extra_link_args=["/DELAYLOAD:cx_Logging"],
                    libraries=["advapi32"],
                    optional=optional,
                ),
            ]
        extensions += [
            Extension(
                "cx_Freeze.bases.gui",
                ["source/bases/Win32GUI.c", "source/bases/_common.c"],
                libraries=["user32"],
                optional=optional,
            ),
            Extension(
                "cx_Freeze.bases.service",
                ["source/bases/Win32Service.c", "source/bases/_common.c"],
                extra_link_args=["/DELAYLOAD:cx_Logging"],
                libraries=["advapi32"],
                optional=optional,
            ),
            Extension(
                "cx_Freeze.util",
                ["source/util.c"],
                libraries=["imagehlp", "shlwapi"],
                optional=optional,
            ),
        ]
    return extensions


if __name__ == "__main__":
    setup(
        cmdclass={"build_ext": BuildBases},
        options={"install": {"optimize": 1}},
        ext_modules=get_extensions(),
    )
