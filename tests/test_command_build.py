"""Tests for cx_Freeze.command.build."""

from __future__ import annotations

import os
import sys
from sysconfig import get_platform, get_python_version

from cx_Freeze.command.build import Build
from cx_Freeze.dist import Distribution


# pylint: disable=C0115,C0116
class TestBuild:
    def test_finalize_options(self):
        dist = Distribution(
            {"name": "foo", "version": "0.0", "script_name": "setup.py"}
        )
        cmd = Build(dist)
        cmd.finalize_options()

        # if not specified, plat_name gets the current platform
        assert cmd.plat_name == get_platform()

        # build_purelib is build + lib
        wanted = os.path.join(cmd.build_base, "lib")
        assert cmd.build_purelib == wanted

        # build_platlib is 'build/lib.platform-x.x[-pydebug]'
        # examples:
        #   build/lib.linux-x86_64-3.9
        #   build/lib.win-amd64-3.10
        python_version = get_python_version()
        plat_spec = f".{cmd.plat_name}-{python_version}"
        if hasattr(sys, "gettotalrefcount"):
            self.assertTrue(cmd.build_platlib.endswith("-pydebug"))
            plat_spec += "-pydebug"
        wanted = os.path.join(cmd.build_base, "lib" + plat_spec)
        assert cmd.build_platlib == wanted

        # by default, build_lib = build_purelib
        assert cmd.build_lib == cmd.build_purelib

        # build_temp is build/temp.<plat>
        wanted = os.path.join(cmd.build_base, "temp" + plat_spec)
        assert cmd.build_temp == wanted

        # build_scripts is build/scripts-x.x
        wanted = os.path.join(cmd.build_base, f"scripts-{python_version}")
        assert cmd.build_scripts == wanted

        # executable is os.path.normpath(sys.executable)
        assert cmd.executable == os.path.normpath(sys.executable)
