"""Tests for multiprocessing."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, EXE_SUFFIX

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

SOURCE = """\
sample0.py
    from multiprocessing import Pool, freeze_support, set_start_method

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
    import multiprocessing

    def foo(q):
        q.put("Hello from cx_Freeze")

    if __name__ == "__main__":
        multiprocessing.freeze_support()
        multiprocessing.set_start_method('spawn')
        q = multiprocessing.SimpleQueue()
        p = multiprocessing.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()
sample2.py
    import multiprocessing

    def foo(q):
        q.put("Hello from cx_Freeze")

    if __name__ == "__main__":
        ctx = multiprocessing.get_context('spawn')
        ctx.freeze_support()
        q = ctx.Queue()
        p = ctx.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()
sample3.py
    if __name__ == "__main__":
        import multiprocessing, sys
        multiprocessing.freeze_support()
        multiprocessing.set_start_method('spawn')
        mgr = multiprocessing.Manager()
        var = [1] * 10000000
        print("creating dict", end="...")
        mgr_dict = mgr.dict({'test': var})
        print("done!")
setup.py
    from cx_Freeze import setup
    setup(
        name="test_multiprocessing",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=["sample0.py", "sample1.py", "sample2.py", "sample3.py"],
        options={
            "build_exe": {
                "excludes": ["tkinter"],
                "silent": True,
            }
        }
    )
"""
EXPECTED_OUTPUT = [
    "Hello from cx_Freeze #9",
    "Hello from cx_Freeze",
    "Hello from cx_Freeze",
    "creating dict...done!",
]


def _parameters_data() -> Iterator:
    import multiprocessing as mp

    methods = mp.get_all_start_methods()
    for method in methods:
        source = SOURCE.replace("('spawn')", f"('{method}')")
        for i, expected in enumerate(EXPECTED_OUTPUT):
            if method == "forkserver" and i != 3:
                continue  # only sample3 works with forkserver method
            sample = f"sample{i}"
            test_id = f"{sample}-{method}"
            yield pytest.param(source, sample, expected, id=test_id)


@pytest.mark.parametrize(("source", "sample", "expected"), _parameters_data())
def test_multiprocessing(
    tmp_path: Path, source: str, sample: str, expected: str
) -> None:
    """Provides test cases for multiprocessing."""
    create_package(tmp_path, source)
    output = run_command(tmp_path)
    target_dir = tmp_path / BUILD_EXE_DIR
    executable = target_dir / f"{sample}{EXE_SUFFIX}"
    assert executable.is_file()
    output = run_command(target_dir, executable, timeout=10)
    assert output.splitlines()[-1] == expected
