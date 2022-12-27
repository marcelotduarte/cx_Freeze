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

        # build_exe is 'build/exe.platform-x.x'
        # examples:
        #   build/lib.linux-x86_64-3.10
        #   build/lib.win-amd64-3.11
        python_version = get_python_version()
        plat_spec = f".{cmd.plat_name}-{python_version}"
        wanted = os.path.join(cmd.build_base, "exe" + plat_spec)
        assert cmd.build_exe == wanted

        # executable is os.path.normpath(sys.executable)
        assert cmd.executable == os.path.normpath(sys.executable)
