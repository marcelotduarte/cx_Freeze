"""Tests for multiprocessing."""
from __future__ import annotations

import multiprocessing as mp
import os
import sys
from pathlib import Path
from subprocess import check_output
from sysconfig import get_platform, get_python_version

import pytest
from generate_samples import create_package

PLATFORM = get_platform()
PYTHON_VERSION = get_python_version()
BUILD_EXE_DIR = f"build/exe.{PLATFORM}-{PYTHON_VERSION}"

SOURCE = """\
sample1.py
    import multiprocessing

    def foo(q):
        q.put('hello')

    if __name__ == '__main__':
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
        q.put('hello')

    if __name__ == '__main__':
        ctx = multiprocessing.get_context('spawn')
        ctx.freeze_support()
        q = ctx.Queue()
        p = ctx.Process(target=foo, args=(q,))
        p.start()
        print(q.get())
        p.join()
sample3.py
    if __name__ ==  "__main__":
        import multiprocessing
        multiprocessing.freeze_support()
        multiprocessing.set_start_method('spawn')
        mgr = multiprocessing.Manager()
        var = [1] * 10000000
        print("creating dict", end="...")
        mgr_dict = mgr.dict({'test': var})
        print("done!")
setup.py
    from cx_Freeze import Executable, setup
    setup(
        name="test_multiprocessing",
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
EXPECTED_OUTPUT = ["hello", "hello", "creating dict...done!"]


def _parameters_data():
    methods = mp.get_all_start_methods()
    for method in methods:
        source = SOURCE.replace("('spawn')", f"('{method}')")
        for i, expected in enumerate(EXPECTED_OUTPUT):
            sample = f"sample{i+1}"
            test_id = f"{sample},{method}"
            yield pytest.param(source, sample, expected, id=test_id)


@pytest.mark.parametrize(("source", "sample", "expected"), _parameters_data())
def test_multiprocessing(
    tmp_path: Path, source: str, sample: str, expected: str
):
    """Provides test cases for multiprocessing."""
    create_package(tmp_path, source)
    output = check_output(
        [sys.executable, "setup.py", "build_exe"],
        text=True,
        cwd=os.fspath(tmp_path),
    )
    print(output)
    suffix = ".exe" if sys.platform == "win32" else ""
    executable = tmp_path / BUILD_EXE_DIR / f"{sample}{suffix}"
    assert executable.is_file()
    output = check_output(
        [os.fspath(executable)], text=True, timeout=10, cwd=os.fspath(tmp_path)
    )
    print(output)
    assert output.splitlines()[-1] == expected
