import os.path
import sys
import tempfile
from nose.tools import assert_raises

from cx_Freeze.common import process_path_specs
from cx_Freeze.exception import ConfigError


rootdir = "C:\\" if sys.platform == "win32" else "/"


def test_process_path_specs():
    with tempfile.TemporaryDirectory() as tempdir:
        foo_bar_path = os.path.join(tempdir, "foo", "bar").replace("\\", "/")
        os.makedirs(foo_bar_path)
        foo_qux_path = os.path.join(tempdir, "foo", "qux").replace("\\", "/")
        os.makedirs(foo_qux_path)
        input_paths = [foo_bar_path, foo_qux_path]
        suffix_paths = ["bar", "baz/xyz"]
        inp = [
            foo_bar_path,
            (foo_qux_path, os.path.join("baz", "xyz").replace("\\", "/")),
        ]
        outp = process_path_specs(inp)
        assert isinstance(outp, list)
        assert len(outp) == len(inp)
        for o in outp:
            assert isinstance(o, tuple)
            assert len(o) == 2
            assert o[0].as_posix() in input_paths
            assert o[1].as_posix() in suffix_paths


def test_process_path_specs_bad():
    with assert_raises(ConfigError):
        process_path_specs(
            [(os.path.join(rootdir, "foo"), os.path.join(rootdir, "bar"))]
        )

    with assert_raises(ConfigError):
        process_path_specs([("a", "b", "c")])
