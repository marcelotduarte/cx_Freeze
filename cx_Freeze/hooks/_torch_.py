"""A collection of functions which are triggered automatically by finder when
PyTorch package is included.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_LINUX, IS_MACOS, IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder
    from cx_Freeze.module import Module

# 1) Test in Windows from pypi
# pip install torch
#
# 2) Test in Windows from pytorch
# # https://pytorch.org/get-started/locally/
#
# 3) Test in Linux from pypi includes nvidia packages
# pip install torch


def load_torch(finder: ModuleFinder, module: Module) -> None:
    """Hook for PyTorch. Tested in Windows and Linux."""
    module_path = module.file.parent
    site_packages_path = module_path.parent

    # Activate the optimized mode by default
    if module.name in finder.zip_exclude_packages:
        print(f"WARNING: {module.name} hook optimizations disabled.")
        module.in_file_system = 1
    elif module.name in finder.zip_include_packages:
        print(f"WARNING: {module.name} hook optimizations enabled.")
        module.in_file_system = 2
    else:
        module.in_file_system = 2

    # has cuda libraries?
    try:
        finder.include_module("nvidia")
    except ImportError:
        pass
    else:
        code_string = module.file.read_text(encoding="utf_8")
        # patch the code to ignore CUDA_PATH_Vxx_x installation directory
        code_string = code_string.replace("CUDA_PATH", "NO_CUDA_PATH")
        if IS_LINUX:
            # fix for issue #2682
            lines = code_string.splitlines()
            for i, line in enumerate(lines[:]):
                if line.strip() == "_load_global_deps()":
                    lines[i] = line.replace(
                        "_load_global_deps()",
                        "import nvidia; _load_global_deps()",
                    )
            code_string = "\n".join(lines)
        module.code = compile(
            code_string,
            module.file.as_posix(),
            "exec",
            dont_inherit=True,
            optimize=finder.optimize,
        )

    # include the shared libraries in 'lib' as fixed libraries
    source_lib = module_path / "lib"
    if source_lib.exists():
        target_lib = f"lib/{module.name}/lib"
        if IS_MINGW or IS_WINDOWS:
            extension = "*.dll"
        elif IS_MACOS:
            extension = "*.dylib"
        else:
            extension = "*.so*"
        for source in source_lib.glob(extension):
            finder.lib_files[source] = f"{target_lib}/{source.name}"
            finder.include_files(source, f"{target_lib}/{source.name}")

    # include the binaries (torch 2.1+)
    source_bin = module_path / "bin"
    if source_bin.exists():
        finder.include_files(source_bin, f"lib/{module.name}/bin")
    # hidden modules
    finder.include_module("torch._C")
    finder.include_module("torch._VF")
    finder.include_package("torch.distributions")
    finder.include_package("torch.testing")
    # exclude C files
    finder.exclude_module("torch.include")
    finder.exclude_module("torch.share")
    finder.exclude_module("torchgen.packaged.ATen.templates")
    # torch 2.2
    finder.include_module("torch.return_types")

    # include 'config.py' source files
    for source in module_path.rglob("**/config.py"):
        target = "lib" / source.relative_to(site_packages_path)
        finder.include_files(source, target)
    for source in module_path.rglob("**/_config.py"):
        target = "lib" / source.relative_to(site_packages_path)
        finder.include_files(source, target)

    # include source files that uses @torch.jit._overload_method
    for source in module_path.rglob("*.py"):  # type: Path
        if b"@torch.jit._overload_method" in source.read_bytes():
            target = "lib" / source.relative_to(site_packages_path)
            finder.include_files(source, target)


def load_torch__dynamo_skipfiles(finder: ModuleFinder, module: Module) -> None:
    """Patch to work with Python 3.11+."""
    code_string = module.file.read_text(encoding="utf_8")
    code_string = code_string.replace(
        "return _strip_init_py(m.__file__)",
        'return _strip_init_py(getattr(m, "__file__", ""))',
    )
    module.code = compile(
        code_string,
        module.file.as_posix(),
        "exec",
        dont_inherit=True,
        optimize=finder.optimize,
    )


def load_torch__numpy(finder: ModuleFinder, module: Module) -> None:
    """Patch to work in Windows."""
    finder.exclude_module("torch._numpy.testing")
    finder.include_package(module.name)
