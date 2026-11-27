"""Tests for hooks of ortools."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from tests.conftest import TempPackage

TIMEOUT = 15 * (2 if IS_CONDA else 1) * (2 if IS_MACOS else 1)

zip_packages = pytest.mark.parametrize(
    "zip_packages", [False, True], ids=["", "zip_packages"]
)


SOURCE_TEST_ORTOOLS_9 = r'''
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

# [START program]
"""Simple Constraint optimization example."""

# [START import]
from ortools.constraint_solver import pywrapcp
# [END import]


def main():
    """Entry point of the program."""
    # Instantiate the solver.
    # [START solver]
    solver = pywrapcp.Solver("CPSimple")
    # [END solver]

    # Create the variables.
    # [START variables]
    num_vals = 3
    x = solver.IntVar(0, num_vals - 1, "x")
    y = solver.IntVar(0, num_vals - 1, "y")
    z = solver.IntVar(0, num_vals - 1, "z")
    # [END variables]

    # Constraint 0: x != y.
    # [START constraints]
    solver.Add(x != y)
    print("Number of constraints: ", solver.Constraints())
    # [END constraints]

    # Solve the problem.
    # [START solve]
    decision_builder = solver.Phase(
        [x, y, z], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE
    )
    # [END solve]

    # Print solution on console.
    # [START print_solution]
    count = 0
    solver.NewSearch(decision_builder)
    while solver.NextSolution():
        count += 1
        solution = f"Solution {count}:\n"
        for var in [x, y, z]:
            solution += f" {var.Name()} = {var.Value()}"
        print(solution)
    solver.EndSearch()
    print(f"Number of solutions found: {count}")
    # [END print_solution]

    # [START advanced]
    print("Advanced usage:")
    print(f"Memory usage: {pywrapcp.Solver.MemoryUsage()} bytes")
    print(f"Problem solved in {solver.WallTime()} ms")
    # [END advanced]


if __name__ == "__main__":
    main()
# [END program]
'''
SOURCE_TEST_ORTOOLS_10 = r'''
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

# [START program]
"""Simple Constraint optimization example."""

# [START import]
from ortools.constraint_solver.python import constraint_solver as cp

# [END import]


def main():
    """Entry point of the program."""
    # Instantiate the solver.
    # [START solver]
    solver = cp.Solver("CPSimple")
    # [END solver]

    # Create the variables.
    # [START variables]
    num_vals = 3
    x = solver.new_int_var(0, num_vals - 1, "x")
    y = solver.new_int_var(0, num_vals - 1, "y")
    z = solver.new_int_var(0, num_vals - 1, "z")
    # [END variables]

    # Constraint 0: x != y.
    # [START constraints]
    solver.add(x != y)
    print("Number of constraints: ", solver.num_constraints)
    # [END constraints]

    # Solve the problem.
    # [START solve]
    decision_builder = solver.phase(
        [x, y, z],
        cp.IntVarStrategy.CHOOSE_FIRST_UNBOUND,
        cp.IntValueStrategy.ASSIGN_MIN_VALUE,
    )
    # [END solve]

    # Print solution on console.
    # [START print_solution]
    count = 0
    solver.new_search(decision_builder)
    while solver.next_solution():
        count += 1
        solution = f"Solution {count}:\n"
        for var in [x, y, z]:
            solution += f" {var.name} = {var.value()}"
        print(solution)
    solver.end_search()
    print(f"Number of solutions found: {count}")
    # [END print_solution]

    # [START advanced]
    print("Advanced usage:")
    print(f"Memory usage: {solver.memory_usage()} bytes")
    print(f"Problem solved in {solver.wall_time_ms} ms")
    # [END advanced]


if __name__ == "__main__":
    main()
# [END program]
'''
SOURCE_TEST = """
pyproject.toml
    [project]
    name = "test_ortools"
    version = "0.1.2.3"
    dependencies = ["ortools"]

    [tool.cxfreeze]
    executables = ["test_ortools.py"]

    [tool.cxfreeze.build_exe]
    include-msvcr = true
    excludes = ["tkinter"]
    silent = true
"""

ORTOOLS_VERSIONS = []
version_info = sys.version_info[:2]
if version_info <= (3, 11):
    ORTOOLS_VERSIONS.append("ortools~=9.6.0")
if IS_LINUX:
    from platform import libc_ver

    version_raw = libc_ver()
    version = tuple(map(int, version_raw[1].split(".")))
    if version < (2, 28):
        # for Python 3.11-3.14
        ORTOOLS_VERSIONS.append("ortools>=9.11.0,<10.0.0")
    elif (version_info <= (3, 14) and ABI_THREAD == "") or (
        version_info == (3, 14) and ABI_THREAD == "t"
    ):
        # for Python 3.11-3.14 and 3.14t
        ORTOOLS_VERSIONS.append("ortools>=9.15.0,<10.0.0")
        if ABI_THREAD == "":
            # for Python 3.11-3.15
            ORTOOLS_VERSIONS.append("ortools>=10.0.0rc1")
elif ABI_THREAD == "" and not (IS_WINDOWS and IS_ARM_64):
    if version_info <= (3, 14):
        # for Python 3.11-3.14 on macOS and Windows
        ORTOOLS_VERSIONS.append("ortools>=9.15.0,<10.0.0")
    # for Python 3.11-3.15 on macOS and Windows
    ORTOOLS_VERSIONS.append("ortools>=10.0.0rc1")


@pytest.mark.skipif(IS_MINGW, reason="ortools not supported in mingw")
@pytest.mark.venv(install_dependencies=False)
@zip_packages
@pytest.mark.parametrize("ortools_version", ORTOOLS_VERSIONS)
def test_ortools(
    tmp_package: TempPackage, zip_packages: bool, ortools_version: str
) -> None:
    """Test if ortools is working correctly."""
    tmp_package.map_package_to_conda["ortools"] = "ortools-python"
    tmp_package.create(SOURCE_TEST)
    test_file = tmp_package.path / "test_ortools.py"
    if ">=10" in ortools_version:
        test_file.write_text(SOURCE_TEST_ORTOOLS_10)
    else:
        test_file.write_text(SOURCE_TEST_ORTOOLS_9)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.install(ortools_version)
    tmp_package.freeze()

    executable = tmp_package.executable("test_ortools")
    assert executable.is_file()
    result = tmp_package.run(executable, timeout=TIMEOUT)
    lines = ["Number of constraints: *"]
    for i in range(18):
        lines += [f"Solution {i + 1}:", " x = * y = * z = *"]
    lines += [
        "Number of solutions found: *",
        "Advanced usage:",
        "Memory usage: * bytes",
        "Problem solved in * ms",
    ]
    result.stdout.fnmatch_lines(lines)
