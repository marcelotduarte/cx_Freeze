import os.path
import sys

from nose.tools import assert_raises

from cx_Freeze.common import process_path_specs
from cx_Freeze.exception import ConfigError


rootdir = "C:\\" if sys.platform == "win32" else "/"


def test_process_path_specs():
    inp = [
        os.path.join(rootdir, "foo", "bar"),
        (os.path.join(rootdir, "foo", "qux"), os.path.join("baz", "xyz")),
    ]
    outp = process_path_specs(inp)
    assert outp == [
        (os.path.join(rootdir, "foo", "bar"), "bar"),
        (os.path.join(rootdir, "foo", "qux"), os.path.join("baz", "xyz")),
    ]


def test_process_path_specs_bad():
    with assert_raises(ConfigError):
        process_path_specs(
            [(os.path.join(rootdir, "foo"), os.path.join(rootdir, "bar"))]
        )

    with assert_raises(ConfigError):
        process_path_specs([("a", "b", "c")])
