"""Implements the 'bdist_deb' command (create DEB binary distributions).

This is a simple wraper around 'alien'.
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess

from setuptools import Command

from cx_Freeze.exception import ExecError, PlatformError

__all__ = ["BdistDEB"]


class BdistDEB(Command):
    """Create an DEB distribution."""

    description = "create an DEB distribution"

    user_options = [
        (
            "bdist-base=",
            None,
            "base directory for creating built distributions",
        ),
        (
            "build-dir=",
            "b",
            "directory of built executables and dependent files",
        ),
        ("dist-dir=", "d", "directory to put final built distributions in"),
    ]

    def initialize_options(self):
        self.bdist_base = None
        self.build_dir = None
        self.dist_dir = None

    def finalize_options(self):
        if os.name != "posix":
            raise PlatformError(
                "don't know how to create DEB "
                f"distributions on platform {os.name}"
            )
        if not shutil.which("alien"):
            raise PlatformError("failed to find 'alien' for this platform.")
        if os.getuid() != 0 and not shutil.which("fakeroot"):
            raise PlatformError("failed to find 'fakeroot' for this platform.")

        self.set_undefined_options("bdist", ("bdist_base", "bdist_base"))
        self.set_undefined_options(
            "bdist",
            ("bdist_base", "bdist_base"),
            ("dist_dir", "dist_dir"),
        )

    def run(self):
        # make a binary RPM to convert
        bdist_rpm = self.reinitialize_command(
            "bdist_rpm", bdist_base=self.bdist_base, dist_dir=self.dist_dir
        )
        bdist_rpm.ensure_finalized()
        bdist_rpm.run()
        rpm_filename = None
        for command, _, filename in self.distribution.dist_files:
            if command == "bdist_rpm":
                rpm_filename = filename
                break
        if rpm_filename is None:
            raise ExecError("could not build rpm")

        # convert rpm to deb (by default in dist directory)
        logging.info("building DEB")
        cmd = ["alien", "--to-deb", os.path.basename(rpm_filename)]
        if os.getuid() != 0:
            cmd.insert(0, "fakeroot")
        if self.dry_run:
            self.spawn(cmd)
        else:
            logging.info(subprocess.list2cmdline(cmd))
            output = subprocess.check_output(cmd, text=True, cwd=self.dist_dir)
            logging.info(output)
            filename = output.splitlines()[0].split()[0]
            filename = os.path.join(self.dist_dir, filename)
            if not os.path.exists(filename):
                raise ExecError("could not build deb")
            self.distribution.dist_files.append(("bdist_deb", "any", filename))
