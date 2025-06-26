"""Tests for cx_Freeze.hooks of numpy, pandas and scipy."""

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
    IS_X86_64,
)

TIMEOUT = 10
TIMEOUT_SLOW = 60 if IS_CONDA else 20
TIMEOUT_VERY_SLOW = 90 if IS_CONDA else 30

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
        "numpy<1.26;python_version <= '3.10'",
        "numpy<2;python_version == '3.11'",
        "numpy>=2;python_version >= '3.12'",
        "matplotlib<3.4;python_version == '3.9' and sys_platform == 'linux'",
        "matplotlib<3.6;python_version == '3.9' and sys_platform != 'linux'",
        "matplotlib<3.6;python_version == '3.10'",
        "matplotlib<3.7;python_version == '3.11'",
        "matplotlib>=3.7;python_version >= '3.12'",
    ]

    [tool.cxfreeze]
    executables = ["test_matplotlib.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest", "PySide6", "shiboken6"]
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="matplotlib does not support Windows arm64",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_matplotlib(tmp_package, zip_packages: bool) -> None:
    """Test if matplotlib hook is working correctly."""
    tmp_package.create(SOURCE_TEST_MATPLOTLIB)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()

    executable = tmp_package.executable("test_matplotlib")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT_VERY_SLOW)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("numpy version")
    assert lines[2].startswith("matplotlib version")
    assert tmp_package.path.joinpath("test.png").is_file()


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="pandas does not support Windows arm64",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_pandas(tmp_package, zip_packages: bool) -> None:
    """Test that the pandas/numpy is working correctly."""
    tmp_package.create_from_sample("pandas")
    command = "python setup.py build_exe -O2 --excludes=tkinter,unittest"
    if zip_packages:
        command += " --zip-include-packages=* --zip-exclude-packages="
    command += " --include-msvcr"

    if IS_LINUX and IS_X86_64 and sys.version_info[:2] == (3, 10):
        tmp_package.install(
            "numpy", index="https://pypi.anaconda.org/intel/simple"
        )
    tmp_package.install("pandas")
    output = tmp_package.run(command)

    executable = tmp_package.executable("test_pandas")
    assert executable.is_file()

    output = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("pandas version")
    assert len(lines) == 8, lines[2:]


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
        "numpy<1.26;python_version <= '3.10'",
        "numpy<2;python_version == '3.11'",
        "numpy>=2;python_version >= '3.12'",
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
    (IS_LINUX or IS_WINDOWS) and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="rasterio not supported in windows/linux arm64",
    strict=True,
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="rasterio does not support mingw",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="rasterio does not support Python 3.13t",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_rasterio(tmp_package, zip_packages: bool) -> None:
    """Test if rasterio hook is working correctly."""
    tmp_package.create(SOURCE_TEST_RASTERIO)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()

    executable = tmp_package.executable("test_rasterio")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("numpy version")
    assert lines[2].startswith("rasterio version")


SOURCE_TEST_SCIPY = """
test_scipy.py
    import numpy as np
    import scipy
    from scipy.spatial.transform import Rotation

    print("numpy version", np.__version__)
    print("scipy version", scipy.__version__)
    print(Rotation.from_euler("XYZ", [10, 10, 10], degrees=True).as_matrix())
pyproject.toml
    [project]
    name = "test_scipy"
    version = "0.1.2.3"
    dependencies = [
        "numpy<1.26;python_version <= '3.10'",
        "numpy<2;python_version == '3.11'",
        "numpy>=2;python_version >= '3.12'",
        "scipy<1.9.2;python_version == '3.9'",
        "scipy<1.16;python_version == '3.10'",
        "scipy>=1.16;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_scipy.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "PySide6", "shiboken6"]
    include_msvcr = true
    optimize = 2
    silent = true
"""


@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="scipy does not support Windows arm64",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_scipy(tmp_package, zip_packages: bool) -> None:
    """Test that the scipy/numpy is working correctly."""
    tmp_package.create(SOURCE_TEST_SCIPY)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()

    executable = tmp_package.executable("test_scipy")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    lines = output.splitlines()
    assert lines[0].startswith("numpy version")
    assert lines[1].startswith("scipy version")
    assert len(lines) == 5, lines[2:]


SOURCE_TEST_SHAPELY = """
test_shapely.py
    import numpy as np
    import shapely
    import shapely.geos
    from shapely.geometry import box, Point

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("shapely version", shapely.__version__)
    print("shapely geos version", shapely.geos.geos_version)
    print("shapely geos version string", shapely.geos.geos_version_string)

    patch = Point(0.0, 0.0).buffer(10.0)
    polygon = box(0, 0, 2, 2)
    print(patch)
    print(polygon)
pyproject.toml
    [project]
    name = "test_shapely"
    version = "0.1.2.3"
    dependencies = [
        "numpy<1.26",
        "shapely",
    ]

    [tool.cxfreeze]
    executables = ["test_shapely.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""

SOURCE_TEST_SHAPELY2 = """
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
        "numpy<1.26;python_version <= '3.10'",
        "numpy<2;python_version == '3.11'",
        "numpy>=2;python_version >= '3.12'",
        "shapely<2.1;python_version == '3.10'",
        "shapely>=2.1;python_version > '3.10'",
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
    if sys.version_info[:2] < (3, 10):
        tmp_package.create(SOURCE_TEST_SHAPELY)
    else:
        tmp_package.create(SOURCE_TEST_SHAPELY2)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    output = tmp_package.run()

    executable = tmp_package.executable("test_shapely")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("numpy version")
    assert lines[2].startswith("shapely version")
    assert lines[3].startswith("shapely geos version")
    assert lines[4].startswith("shapely geos version string")
    assert lines[5].startswith("POLYGON")
    assert lines[5].startswith("POLYGON")
    assert lines[6].startswith("POLYGON")


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
    dependencies = [
        "numpy<1.26;python_version <= '3.10'",
        "numpy<2;python_version == '3.11'",
        "numpy>=2;python_version >= '3.12'",
        "vtk<9.3;python_version <= '3.10'",
        "vtk<9.4;python_version == '3.11'",
        "vtk>=9.4;python_version >= '3.12'",
    ]

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
    (IS_LINUX or IS_WINDOWS) and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support Windows/Linux arm64",
    strict=True,
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support mingw",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t",
    raises=ModuleNotFoundError,
    reason="vtkmodules (vtk) does not support Python 3.13t",
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
    output = tmp_package.run()

    executable = tmp_package.executable("test_vtk")
    assert executable.is_file()
    output = tmp_package.run(executable, timeout=TIMEOUT)
    lines = output.splitlines()
    assert lines[0] == "Hello from cx_Freeze"
    assert lines[1].startswith("numpy version")
    assert lines[2].startswith("vtkmodules version")
    assert lines[3].startswith("Original matrix:")
    assert lines[7].startswith("Inverse:")
