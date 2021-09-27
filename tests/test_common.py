import os
import sys
import pytest
from pathlib import Path
from cx_Freeze.common import process_path_specs
from cx_Freeze.exception import ConfigError


class TestProcessPathSpecsWithConvertedNoseTests:
    """ This class provides test cases that are conversions of the old NoseTests in `test_misc`
    that predated usage of the PyTest Framework"""

    def test_process_path_specs(self, tmpdir):
        foo_path = tmpdir.mkdir("foo")
        foo_bar_path = foo_path.mkdir("bar")
        foo_qux_path = foo_path.mkdir("qux")
        input_paths = [Path(foo_bar_path).as_posix(), Path(foo_qux_path).as_posix()]
        suffix_paths = ["bar", "baz/xyz"]
        inp = [
            foo_bar_path, (foo_qux_path, os.path.join("baz", "xyz").replace("\\", "/")),
        ]
        outp = process_path_specs(inp)
        assert isinstance(outp, list)
        assert len(outp) == len(inp)
        for o in outp:
            assert isinstance(o, tuple)
            assert len(o) == 2
            assert o[0].as_posix() in input_paths
            assert o[1].as_posix() in suffix_paths

    def test_process_path_specs_bad(self):
        rootdir = "C:\\" if sys.platform == "win32" else "/"
        with pytest.raises(ConfigError):
            process_path_specs(
                [(os.path.join(rootdir, "foo"), os.path.join(rootdir, "bar"))]
            )
        with pytest.raises(ConfigError):
            process_path_specs([("a", "b", "c")])
