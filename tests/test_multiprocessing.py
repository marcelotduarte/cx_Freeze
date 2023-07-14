"""Tests for multiprocessing."""

from __future__ import annotations

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
        executables=[Executable("sample1.py"), Executable("sample2.py")],
        options={
            "build_exe": {
                "excludes": ["tkinter"],
                "silent": True,
            }
        }
    )
"""
SOURCE_FORK = SOURCE.replace("('spawn')", "('fork')")
SOURCE_FORKSERVER = SOURCE.replace("('spawn')", "('forkserver')")
DONE = "creating dict...done!"
LINUX_ONLY = pytest.mark.skipif(sys.platform != "linux", reason="Linux tests")


@pytest.mark.parametrize(
    ("source", "number", "expected"),
    [
        (SOURCE, 1, "hello"),
        (SOURCE, 2, DONE),
        pytest.param(SOURCE_FORK, 1, "hello", marks=LINUX_ONLY),
        pytest.param(SOURCE_FORK, 2, DONE, marks=LINUX_ONLY),
        pytest.param(SOURCE_FORKSERVER, 1, "hello", marks=LINUX_ONLY),
        pytest.param(SOURCE_FORKSERVER, 2, DONE, marks=LINUX_ONLY),
    ],
    ids=["spawn1", "spawn2", "fork1", "fork2", "forkserver1", "forkserver2"],
)
def test_multiprocessing(
    tmp_path: Path, source: str, number: int, expected: str
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
    executable = tmp_path / BUILD_EXE_DIR / f"sample{number}{suffix}"
    assert executable.is_file()
    output = check_output(
        [os.fspath(executable)], text=True, timeout=10, cwd=os.fspath(tmp_path)
    )
    print(output)
    assert output.splitlines()[-1] == expected
