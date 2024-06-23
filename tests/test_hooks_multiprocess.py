"""Tests for multiprocess."""

from __future__ import annotations

from sysconfig import get_platform, get_python_version
from typing import TYPE_CHECKING, Iterator

import pytest
from generate_samples import create_package, run_command

from cx_Freeze._compat import BUILD_EXE_DIR, IS_MINGW, IS_WINDOWS

if TYPE_CHECKING:
    from pathlib import Path

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
SUFFIX = ".exe" if (IS_MINGW or IS_WINDOWS) else ""

SOURCE = """\
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
setup.py
    from cx_Freeze import Executable, setup
    setup(
        name="test_multiprocess",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=[
            Executable("sample1.py"),
            Executable("sample2.py"),
            Executable("sample3.py"),
        ],
        options={
            "build_exe": {
                "excludes": ["tkinter"],
                "silent": True,
            }
        }
    )
"""
EXPECTED_OUTPUT = [
    "Hello from cx_Freeze",
    "Hello from cx_Freeze",
    "creating dict...done!",
]


def _parameters_data() -> Iterator:
    import multiprocess as mp

    methods = mp.get_all_start_methods()
    for method in methods:
        source = SOURCE.replace("('spawn')", f"('{method}')")
        for i, expected in enumerate(EXPECTED_OUTPUT, 1):
            if method == "forkserver" and i != 3:
                continue  # only sample3 works with forkserver method
            sample = f"sample{i}"
            test_id = f"{sample}-{method}"
            yield pytest.param(source, sample, expected, id=test_id)


@pytest.mark.parametrize(("source", "sample", "expected"), _parameters_data())
def test_multiprocess(
    tmp_path: Path, source: str, sample: str, expected: str
) -> None:
    """Provides test cases for multiprocess."""
    create_package(tmp_path, source)
    output = run_command(tmp_path)
    target_dir = tmp_path / BUILD_EXE_DIR
    executable = target_dir / f"{sample}{SUFFIX}"
    assert executable.is_file()
    output = run_command(target_dir, executable, timeout=10)
    assert output.splitlines()[-1] == expected
