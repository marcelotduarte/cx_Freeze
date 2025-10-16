"""Tests for hooks of multiprocess."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest

from cx_Freeze._compat import IS_ARM_64, IS_CONDA, IS_LINUX, IS_WINDOWS

if TYPE_CHECKING:
    from collections.abc import Iterator

TIMEOUT_ULTRA_VERY_SLOW = 240 if IS_CONDA else 120

SOURCE = """\
sample0.py
    from multiprocess import Pool, freeze_support, set_start_method

    def foo(n):
        return f"Hello from cx_Freeze #{n}"

    if __name__ == "__main__":
        freeze_support()
        set_start_method('spawn')
        with Pool(2) as pool:
            results = pool.map(foo, range(10))
        for line in sorted(results):
            print(line)
sample1.py
    import multiprocess as mp

    def foo(q):
        q.put("Hello from cx_Freeze")

    if __name__ == "__main__":
        mp.freeze_support()
        mp.set_start_method('spawn')
        q = mp.SimpleQueue()
        p = mp.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()
sample2.py
    import multiprocess as mp

    def foo(q):
        q.put("Hello from cx_Freeze")

    if __name__ == "__main__":
        ctx = mp.get_context('spawn')
        ctx.freeze_support()
        q = ctx.Queue()
        p = ctx.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()
sample3.py
    if __name__ == "__main__":
        import multiprocess as mp
        mp.freeze_support()
        mp.set_start_method('spawn')
        mgr = mp.Manager()
        var = [1] * 10000000
        print("creating dict", end="...")
        mgr_dict = mgr.dict({'test': var})
        print("done!")
pyproject.toml
    [project]
    name = "test_mp"
    version = "0.1.2.3"
    description = "Sample for test with cx_Freeze"
    dependencies = ["multiprocess"]

    [tool.cxfreeze]
    executables = ["sample0.py", "sample1.py", "sample2.py", "sample3.py"]

    [tool.cxfreeze.build_exe]
    include_msvcr = true
    excludes = ["tkinter", "unittest"]
    silent = true
"""
EXPECTED_OUTPUT = [
    "Hello from cx_Freeze #9",
    "Hello from cx_Freeze",
    "Hello from cx_Freeze",
    "creating dict...done!",
]


def _parameters_data() -> Iterator:
    import multiprocessing as mp  # noqa: PLC0415

    methods = mp.get_all_start_methods()
    for method in methods:
        source = SOURCE.replace("('spawn')", f"('{method}')")
        for i, expected in enumerate(EXPECTED_OUTPUT):
            if method == "forkserver" and i != 3:
                continue  # only sample3 works with forkserver method
            sample = f"sample{i}"
            test_id = f"{sample}-{method}"
            yield pytest.param(source, sample, expected, False, id=test_id)
            # zip_packages tests removed, multiprocess is too slow


@pytest.mark.skipif(not IS_LINUX, reason="Disabled test")
@pytest.mark.skipif(
    sys.version_info[:2] >= (3, 14),
    reason="multiprocess does not support Python 3.14+",
)
@pytest.mark.xfail(
    IS_WINDOWS and IS_ARM_64,
    raises=ModuleNotFoundError,
    reason="multiprocess does not support Windows arm64",
    strict=True,
)
@pytest.mark.venv(scope="module")
@pytest.mark.parametrize(
    ("source", "sample", "expected", "zip_packages"), _parameters_data()
)
def test_multiprocess(
    tmp_package, source: str, sample: str, expected: str, zip_packages
) -> None:
    """Provides test cases for multiprocess."""
    tmp_package.create(source)
    if zip_packages:
        pyproject = tmp_package.path / "pyproject.toml"
        buf = pyproject.read_bytes().decode().splitlines()
        buf += ['zip_include_packages = "*"', 'zip_exclude_packages = ""']
        pyproject.write_bytes("\n".join(buf).encode("utf_8"))
    tmp_package.freeze()

    executable = tmp_package.executable(sample)
    assert executable.is_file()
    # use a higher timeout because when using dill it is up to 25x slower
    # sample3 using multiprocessing/pickler runs in 0,543s x 13,591s
    result = tmp_package.run(
        executable, cwd=executable.parent, timeout=TIMEOUT_ULTRA_VERY_SLOW
    )
    result.stdout.fnmatch_lines(expected)
