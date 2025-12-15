"""Tests for hooks:
numpy, matplotlib, pandas, raterio, scipy, shapely, and vtk.
"""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MACOS,
    IS_MINGW,
    IS_WINDOWS,
)

TIMEOUT = 15
TIMEOUT_SLOW = 60 if IS_CONDA else 30
TIMEOUT_VERY_SLOW = 120 if IS_CONDA else 60

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)

SOURCE_TEST_MATPLOTLIB = """
test_matplotlib.py
    import numpy as np
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    t = np.arange(0, 3, 0.01)
    plt.plot(t, 2 * np.sin(2 * np.pi * t))
    plt.savefig("test.png")

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("matplotlib version", matplotlib.__version__)
pyproject.toml
    [project]
    name = "test_matplotlib"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "matplotlib<3.7;python_version < '3.11'",
        "matplotlib>=3.7;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_matplotlib.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and sys.version_info[:2] == (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="matplotlib depends on kiwisolver that does not support "
    "Python 3.13t on Windows",
)
@pytest.mark.venv
@zip_packages
def test_matplotlib(tmp_package, zip_packages: bool) -> None:
    """Test if matplotlib hook is working correctly."""
    tmp_package.map_package_to_conda["matplotlib"] = "matplotlib-base"
    tmp_package.create(SOURCE_TEST_MATPLOTLIB)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_matplotlib")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_VERY_SLOW)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "numpy version *", "matplotlib version *"]
    )
    assert tmp_package.path.joinpath("test.png").is_file()


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pandas does not support Windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    IS_WINDOWS and sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="pandas does not support Python 3.13t/3.14t on Windows",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_pandas(tmp_package, zip_packages: bool) -> None:
    """Test that the pandas/numpy is working correctly."""
    tmp_package.create_from_sample("pandas")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_pandas")
    assert executable.is_file()

    result = tmp_package.run(executable, timeout=TIMEOUT_VERY_SLOW)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "numpy version *",
            "pandas version *",
            " *",
            "0*",
            "1*",
            "2*",
            "3*",
            "4*",
        ]
    )


SOURCE_TEST_RASTERIO = """
test_rasterio.py
    import numpy as np
    import rasterio

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("rasterio version", rasterio.__version__)
pyproject.toml
    [project]
    name = "test_rasterio"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "rasterio",
    ]

    [tool.cxfreeze]
    executables = ["test_rasterio.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="rasterio not supported in mingw",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_rasterio(tmp_package, zip_packages: bool) -> None:
    """Test if rasterio hook is working correctly."""
    tmp_package.create(SOURCE_TEST_RASTERIO)
    if IS_MACOS and zip_packages:
        pytest.xfail("rasterio 1.4.4 fails in macOS using zipfile")
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_rasterio")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)

    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "numpy version *", "rasterio version *"]
    )


SOURCE_TEST_SHAPELY = """
test_shapely.py
    import numpy as np
    import shapely
    from shapely import Point

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("shapely version", shapely.__version__)
    print("shapely geos version", shapely.geos_version)
    print("shapely geos version string", shapely.geos_version_string)

    patch = Point(0.0, 0.0).buffer(10.0)
    polygon = shapely.box(0, 0, 2, 2)
    print(patch)
    print(polygon)
pyproject.toml
    [project]
    name = "test_shapely"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "shapely<2.1;python_version < '3.11'",
        "shapely>=2.1;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_shapely.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="shapely does not support Windows arm64",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_shapely(tmp_package, zip_packages: bool) -> None:
    """Test if shapely hook is working correctly."""
    # shapely 1.8.5 supports Python <= 3.11
    tmp_package.create(SOURCE_TEST_SHAPELY)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_shapely")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "numpy version *",
            "shapely version *",
            "shapely geos version *",
            "shapely geos version string *",
            "POLYGON *",
            "POLYGON *",
        ]
    )


SOURCE_TEST_VTK = """
test_vtk.py
    import numpy as np
    import vtkmodules
    from vtkmodules.vtkCommonMath import vtkMatrix3x3

    def main():
        shape = (3, 3)
        m = vtkMatrix3x3()
        m.SetElement(2, 1, 2.0)  # Set element (2,1) to 2.0
        print('Original matrix:')
        print_matrix(m.GetData(), shape)
        m.Invert()
        print('Inverse:')
        print_matrix(m.GetData(), shape)

    def print_matrix(m, shape):
        data = np.array(m)
        data = data.reshape(shape)
        print(data)

    if __name__ == '__main__':
        print("Hello from cx_Freeze")
        print("numpy version", np.__version__)
        print("vtkmodules version", vtkmodules.__version__)
        main()
pyproject.toml
    [project]
    name = "test_vtk"
    version = "0.1.2.3"
    dependencies = ["vtk"]

    [tool.cxfreeze]
    executables = ["test_vtk.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.skipif(
    IS_CONDA and (IS_LINUX or (IS_ARM_64 and IS_MACOS)),
    reason="vtkmodules (vtk) is too slow in conda-forge (Linux and OSX_ARM64)",
)
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support Windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) not supported in mingw",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support Python 3.13t/3.14t",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 14),
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support Python 3.14+",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_vtk(tmp_package, zip_packages: bool) -> None:
    """Test if vtkmodules hook is working correctly."""
    tmp_package.create(SOURCE_TEST_VTK)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_vtk")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "numpy version *",
            "vtkmodules version *",
            "Original matrix:",
            "Inverse:",
        ]
    )
