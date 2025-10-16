"""Tests for hooks of ortools."""

from __future__ import annotations

import sys

import pytest

from cx_Freeze._compat import (
    ABI_THREAD,
    IS_ARM_64,
    IS_CONDA,
    IS_LINUX,
    IS_MINGW,
    IS_WINDOWS,
)

TIMEOUT = 15

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST = """
test_ortools.py
    # Copyright 2010-2025 Google LLC
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.

    '''Magic sequence problem.

    This models aims at building a sequence of numbers such that the number of
    occurrences of i in this sequence is equal to the value of the ith number.
    It uses an aggregated formulation of the count expression called
    distribute().

    Usage: python magic_sequence_distribute.py NUMBER
    '''

    from absl import app
    from absl import flags
    from ortools.constraint_solver import pywrapcp
    from pprint import pprint

    FLAGS = flags.FLAGS


    def main(argv):
        # Create the solver.
        solver = pywrapcp.Solver("magic sequence")

        # Create an array of IntVars to hold the answers.
        size = int(argv[1]) if len(argv) > 1 else 100
        all_values = list(range(0, size))
        all_vars = [solver.IntVar(0, size, "vars_%d" % i) for i in all_values]

        # The number of variables equal to j shall be the value of all_vars[j].
        solver.Add(solver.Distribute(all_vars, all_values, all_vars))

        # The sum of all the values shall be equal to the size.
        # (This constraint is redundant, but speeds up the search.)
        solver.Add(solver.Sum(all_vars) == size)

        solver.NewSearch(
            solver.Phase(
                all_vars, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE
            )
        )
        solver.NextSolution()
        pprint(all_vars)
        solver.EndSearch()


    if __name__ == "__main__":
        app.run(main)
pyproject.toml
    [project]
    name = "test_ortools"
    version = "0.1.2.3"
    dependencies = ["ortools>9.6"]

    [tool.cxfreeze]
    executables = ["test_ortools.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""


@pytest.mark.xfail(
    IS_CONDA and (not IS_LINUX or sys.version_info[:2] > (3, 11)),
    raises=ModuleNotFoundError,
    reason="ortools is supported in conda python <= 3.11 on Linux only",
    strict=True,
)
@pytest.mark.xfail(
    IS_MINGW,
    raises=ModuleNotFoundError,
    reason="ortools not supported in mingw",
    strict=True,
)
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="ortools does not support Windows arm64",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 13) and ABI_THREAD == "t" and not IS_LINUX,
    raises=ModuleNotFoundError,
    reason="ortools supports Python 3.13t on Linux only",
    strict=True,
)
@pytest.mark.xfail(
    sys.version_info[:2] >= (3, 14),
    raises=ModuleNotFoundError,
    reason="rasterio does not support Python 3.14+",
    strict=True,
)
@pytest.mark.venv
@zip_packages
def test_ortools(tmp_package, zip_packages: bool) -> None:
    """Test if ortools is working correctly."""
    tmp_package.map_package_to_conda["ortools"] = "ortools-python"
    tmp_package.create(SOURCE_TEST)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable("test_ortools")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    lines = []
    for i in range(100):
        prefix = " "
        suffix = ","
        if i == 0:
            prefix = "["
        elif i == 99:
            suffix = "]"
        lines.append(f"{prefix}vars_{i}(*){suffix}")
    result.stdout.fnmatch_lines(lines)


@pytest.mark.skipif(not IS_CONDA, reason="conda-forge test only")
@pytest.mark.venv(install_dependencies=False)
@zip_packages
def test_ortools_pip_on_conda(tmp_package, zip_packages: bool) -> None:
    """Test if ortools is working in conda-forge using pip."""
    tmp_package.create(SOURCE_TEST)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    # install from pypi
    tmp_package.install("ortools", backend="pip")
    tmp_package.freeze()

    executable = tmp_package.executable("test_ortools")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    lines = []
    for i in range(100):
        prefix = " "
        suffix = ","
        if i == 0:
            prefix = "["
        elif i == 99:
            suffix = "]"
        lines.append(f"{prefix}vars_{i}(*){suffix}")
    result.stdout.fnmatch_lines(lines)
