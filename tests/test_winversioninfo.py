"""Test winversioninfo"""

# pylint: disable=unused-import
from __future__ import annotations

import pytest  # noqa

from cx_Freeze.winversioninfo import Version, VersionInfo


class TestVersionInfo:
    """Test VersionInfo class."""

    def test___init__(self):
        """This method tests default value for the VersionInfo class"""
        input_version = "9.9.9.9"
        default_version = VersionInfo(input_version)
        assert default_version.version == Version(input_version)
        assert default_version.internal_name is None
        assert default_version.original_filename is None
        assert default_version.comments is None
        assert default_version.company is None
        assert default_version.description is None
        assert default_version.copyright is None
        assert default_version.trademarks is None
        assert default_version.product is None
        assert default_version.dll is None
        assert default_version.debug is None
        assert default_version.verbose is True

    def test___init__pads_short_versions(self):
        """This method tests that short versions get padded to the expected x4
        digit windows versions"""
        input_version = "9"
        default_version = VersionInfo(input_version)
        assert (
            default_version.version.base_version
            == Version(input_version).base_version
        )

    def test___init__with_kwargs(self):
        """This method tests keyword values for the VersionInfo class"""
        input_version = "9.9.9.9"
        input_internal_name = "Test Internal Name"
        input_original_filename = "TestTempFileName"
        input_comments = "TestComment"
        input_company = "TestCompany"
        input_description = "TestDescription"
        input_copyright = "TestCopyright"
        input_trademarks = "TestMark"
        input_product = object()
        input_dll = True
        input_debug = True
        input_verbose = False

        version_instance = VersionInfo(
            version=input_version,
            internal_name=input_internal_name,
            original_filename=input_original_filename,
            comments=input_comments,
            company=input_company,
            description=input_description,
            copyright=input_copyright,
            trademarks=input_trademarks,
            product=input_product,
            dll=input_dll,
            debug=input_debug,
            verbose=input_verbose,
        )

        assert version_instance.version == Version(input_version)
        assert version_instance.internal_name == input_internal_name
        assert version_instance.original_filename == input_original_filename
        assert version_instance.comments == input_comments
        assert version_instance.company == input_company
        assert version_instance.description == input_description
        assert version_instance.copyright == input_copyright
        assert version_instance.trademarks == input_trademarks
        assert version_instance.product == input_product
        assert version_instance.dll is input_dll
        assert version_instance.debug is input_debug
        assert version_instance.verbose is input_verbose
