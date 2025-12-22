"""Tests for hooks: scipy, skimage and sklearn."""

from __future__ import annotations

import pytest

from cx_Freeze._compat import IS_CONDA

TIMEOUT = 15
TIMEOUT_SLOW = 60 if IS_CONDA else 30
TIMEOUT_VERY_SLOW = 120 if IS_CONDA else 60

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST_SCIPY = """
test_scipy.py
    import numpy as np
    import scipy
    from scipy.spatial.transform import Rotation
    from scipy import signal

    print("Hello from cx_Freeze")
    print("numpy version", np.__version__)
    print("scipy version", scipy.__version__)
    print(Rotation.from_euler("XYZ", [10, 10, 10], degrees=True).as_matrix())

    # Example usage of scipy.signal to create a Butterworth filter
    b, a = signal.butter(4, 0.2)
    print("Numerator coefficients:", b)
    print("Denominator coefficients:", a)
pyproject.toml
    [project]
    name = "test_scipy"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "numpy>=2;python_version >= '3.11'",
        "scipy<1.16;python_version < '3.11'",
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
    tmp_package.freeze()

    executable = tmp_package.executable("test_scipy")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        [
            "Hello from cx_Freeze",
            "numpy version *",
            "scipy version *",
            "[[*",
            " [*",
            " [*",
            "Numerator coefficients: *",
            "Denominator coefficients: *",
        ]
    )


SOURCE_TEST_SCIKIT_IMAGE = """
test_skimage.py
    import skimage

    print("Hello from cx_Freeze")
    print("skimage version", skimage.__version__)

    # Load the trained file from the module root.
    trained_file = skimage.data.lbp_frontal_face_cascade_filename()

    # Initialize the detector cascade.
    detector = skimage.feature.Cascade(trained_file)

    img = skimage.data.astronaut()

    detected = detector.detect_multi_scale(
        img=img, scale_factor=1.2, step_ratio=1,
        min_size=(60, 60), max_size=(123, 123)
    )
    print(detected)
pyproject.toml
    [project]
    name = "test_skimage"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "scikit-image",
    ]

    [tool.cxfreeze]
    executables = ["test_skimage.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "PySide6", "shiboken6"]
    include_msvcr = true
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_skimage(tmp_package, zip_packages: bool) -> None:
    """Test that the scikit-image is working correctly."""
    tmp_package.create(SOURCE_TEST_SCIKIT_IMAGE)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_skimage")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(
        ["Hello from cx_Freeze", "skimage version *", "[{*"]
    )


SOURCE_TEST_SCIKIT_LEARN = """
test_sklearn.py
    import sklearn

    print("Hello from cx_Freeze")
    print("sklearn version", sklearn.__version__)
pyproject.toml
    [project]
    name = "test_sklearn"
    version = "0.1.2.3"
    dependencies = [
        "numpy<2;python_version < '3.11'",
        "scikit-learn<1.7;python_version < '3.11'",
        "scikit-learn>=1.7;python_version >= '3.11'",
    ]

    [tool.cxfreeze]
    executables = ["test_sklearn.py"]

    [tool.cxfreeze.build_exe]
    excludes = ["tkinter", "PySide6", "shiboken6"]
    include_msvcr = true
    silent = true
"""


@pytest.mark.venv
@zip_packages
def test_sklearn(tmp_package, zip_packages: bool) -> None:
    """Test that the scikit-learn is working correctly."""
    tmp_package.create(SOURCE_TEST_SCIKIT_LEARN)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_sklearn")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT_SLOW)
    result.stdout.fnmatch_lines(["Hello from cx_Freeze", "sklearn version *"])
