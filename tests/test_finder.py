"""Test ModuleFinder."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import pytest

from cx_Freeze import ConstantsModule, ModuleFinder

from .datatest import SCAN_CODE_TEST, SYNTAX_ERROR_TEST

SHARED_PACKAGE_DISTRIBUTIONS = """\
pkga/__init__.py
    import importlib.metadata
    __version__ = importlib.metadata.version("pkga")
pkga/extra/data.txt
    data
pkga-1.0.dist-info/METADATA
    Metadata-Version: 2.1
    Name: pkga
    Version: 1.0
pkga-1.0.dist-info/RECORD
    pkga/__init__.py,,
pkga_extra-1.0.dist-info/METADATA
    Metadata-Version: 2.1
    Name: pkga-extra
    Version: 1.0
pkga_extra-1.0.dist-info/RECORD
    pkga/extra/data.txt,,
test.py
    from cx_Freeze import ConstantsModule, ModuleFinder

    finder = ModuleFinder(ConstantsModule())
    print(finder.import_distributions["pkga"].name)
"""

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

    from tests.conftest import TempPackage


class TestModuleFinder:
    """Provides test cases for ModuleFinder class."""

    @pytest.fixture
    def fix_module_finder(self) -> ModuleFinder:
        constants = ConstantsModule()
        return ModuleFinder(constants_module=constants)

    def test_scan_code(
        self,
        tmp_package: TempPackage,
        fix_module_finder: ModuleFinder,
        mocker: MockerFixture,
    ) -> None:
        tmp_package.create(SCAN_CODE_TEST[4])
        any3 = (mocker.ANY,) * 3
        import_mock = mocker.patch.object(
            fix_module_finder, "_import_module", return_value=None
        )
        fix_module_finder.include_file_as_module(
            tmp_package.path / "imports_sample.py"
        )
        import_mock.assert_has_calls(
            [
                mocker.call("moda", *any3),
                mocker.call("modb", *any3),
                mocker.call("", *any3),
                mocker.call("modd", *any3),
                mocker.call("mode", *any3),
                mocker.call("modf", *any3),
                mocker.call("modg.submod", *any3),
                mocker.call("modh", *any3),
            ]
        )

    def test_invalid_syntax(
        self, tmp_package: TempPackage, fix_module_finder: ModuleFinder
    ) -> None:
        """Invalid syntax (e.g. Py2 only code) should not break freezing."""
        tmp_package.create(SYNTAX_ERROR_TEST[4])
        fix_module_finder.path.insert(0, os.fspath(tmp_package.path))
        # Threw SyntaxError before the bug was fixed
        module = fix_module_finder.include_module("invalid_syntax")
        assert module is not None
        assert module.error_msg == "SyntaxError: invalid syntax"


@pytest.mark.parametrize("hash_seed", ["1", "2", "3", "4", "5", "6"])
def test_import_distributions_shared_package(
    tmp_package: TempPackage, hash_seed: str
) -> None:
    """Prefer the distribution named after the import package (#3456)."""
    tmp_package.create(SHARED_PACKAGE_DISTRIBUTIONS)
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = hash_seed
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    result = tmp_package.run("python test.py", env=env)
    assert result.ret == 0, result.stderr
    assert result.outlines[-1] == "pkga"
