"""Module for the VersionInfo base class."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from struct import calcsize, pack

from ._compat import packaging

try:
    from win32verstamp import stamp as version_stamp
except ImportError:
    version_stamp = None

try:
    from cx_Freeze import util
except ImportError:
    util = None

__all__ = ["Version", "VersionInfo"]

# types
CHAR = "c"
DWORD = "L"
WCHAR = "H"
WORD = "H"

VS_FFI_SIGNATURE = 0xFEEF04BD
VS_FFI_STRUCVERSION = 0x00010000
VS_FFI_FILEFLAGSMASK = 0x0000003F
VOS_NT_WINDOWS32 = 0x00040004

KEY_VERSION_INFO = "VS_VERSION_INFO"
KEY_STRING_FILE_INFO = "StringFileInfo"
KEY_STRING_TABLE = "040904E4"
KEY_VAR_FILE_INFO = "VarFileInfo"

# To disable the experimental feature in Windows:
# set CX_FREEZE_STAMP=pywin32
# pip install -U pywin32
if os.environ.get("CX_FREEZE_STAMP", "") == "pywin32":
    CX_FREEZE_STAMP = "pywin32"
else:
    CX_FREEZE_STAMP = "internal"


class Version(packaging.version.Version):
    """A valid PEP440 version."""


class Structure:
    """Abstract base class for structures in native byte order. Concrete
    structure and union types must be created by subclassing one of these
    types, and at least define a _fields class variable.
    """

    def __init__(self, *args):
        if not hasattr(self, "_fields"):
            self._fields: list[tuple[str, str]] = []
        for i, (field, _) in enumerate(self._fields):
            setattr(self, field, args[i])

    def __str__(self):
        dump = json.dumps(self.as_dict(), indent=2)
        return self.__class__.__name__ + ": " + dump

    def as_dict(self):
        """Return the field values as dictionary."""
        fields = {}
        for fieldname, _ in self._fields:
            data = getattr(self, fieldname)
            if hasattr(data, "as_dict"):
                data = data.as_dict()
            elif isinstance(data, bytes):
                data = data.decode()
            fields[fieldname] = data
        return fields

    def to_buffer(self):
        """Return the field values to a buffer."""
        buffer = b""
        for fieldname, fmt in self._fields:
            data = getattr(self, fieldname)
            if hasattr(data, "to_buffer"):
                data = data.to_buffer()
            elif isinstance(data, str):
                data = data.encode("utf-16le")
            elif isinstance(fmt, str):
                data = pack(fmt, data)
            buffer += data
        return buffer


class VS_FIXEDFILEINFO(Structure):  # pylint: disable=invalid-name
    """Version information for a Win32 file."""

    _fields = [
        ("dwSignature", DWORD),
        ("dwStrucVersion", DWORD),
        ("dwFileVersionMS", DWORD),
        ("dwFileVersionLS", DWORD),
        ("dwProductVersionMS", DWORD),
        ("dwProductVersionLS", DWORD),
        ("dwFileFlagsMask", DWORD),
        ("dwFileFlags", DWORD),
        ("dwFileOS", DWORD),
        ("dwFileType", DWORD),
        ("dwFileSubtype", DWORD),
        ("dwFileDateMS", DWORD),
        ("dwFileDateLS", DWORD),
    ]


class String(Structure):
    """File version resource representation of the data."""

    def __init__(
        self, key: str, value: int | str | Structure | None = None
    ):  # pylint: disable=W0231
        key = key + "\0"
        key_len = len(key)
        fields = [
            ("wLength", WORD),
            ("wValueLength", WORD),
            ("wType", WORD),
            ("szKey", WCHAR * key_len),
        ]
        key_len = calcsize(WCHAR) * key_len
        pad_len = (4 - ((calcsize(WORD) * 3 + key_len) & 3)) & 3
        if 0 < pad_len < 4:
            fields.append(("Padding", f"{pad_len}s"))
        value_len = 0
        value_type = 1
        value_size = 1
        if isinstance(value, int):
            value_len = calcsize(DWORD)
            value_type = 0
            fields.append(("Value", DWORD))
        elif isinstance(value, str):
            value = value + "\0"
            value_len = len(value)
            value_size = calcsize(WCHAR)
            fields.append(("Value", WCHAR * value_len))
        elif hasattr(value, "wLength"):  # instance of String
            value_len = value.wLength
            fields.append(("Value", type(value)))
        elif isinstance(value, Structure):
            value_len = calcsize("".join([f[1] for f in value._fields]))
            value_type = 0
            fields.append(("Value", type(value)))

        # pylint: disable=invalid-name
        self._fields = fields
        self.wValueLength = value_len
        self.wType = value_type
        self.szKey = key
        self.Padding = b"\0" * pad_len
        self.Value = value
        self.wLength = (
            calcsize(WORD) * 3 + key_len + pad_len + value_size * value_len
        )
        self._children = 0

    def children(self, value: String):
        """Represents the child String object."""
        pad_len = 4 - (self.wLength & 3)
        if 0 < pad_len < 4:
            field = f"Padding{self._children}"
            self._fields.append((field, f"{pad_len}s"))
            setattr(self, field, b"\0" * pad_len)
            self.wLength += calcsize(CHAR) * pad_len
        field = f"Children{self._children}"
        self._fields.append((field, type(value)))
        setattr(self, field, value)
        self._children += 1
        self.wLength += value.wLength


class VersionInfo:
    """Organizes the version information (resource) data of a file."""

    def __init__(
        self,
        version: str,
        internal_name: str | None = None,
        original_filename: str | None = None,
        comments: str | None = None,
        company: str | None = None,
        description: str | None = None,
        copyright: str | None = None,  # noqa: A002
        trademarks: str | None = None,
        product: str | None = None,
        dll: bool | None = None,
        debug: bool | None = None,
        verbose: bool = True,
    ):
        self.version: Version = Version(version)
        self.internal_name: str | None = internal_name
        self.original_filename: str | None = original_filename
        self.comments: str | None = comments
        self.company: str | None = company
        self.description: str | None = description
        self.copyright: str | None = copyright
        self.trademarks: str | None = trademarks
        self.product: str | None = product
        self.dll: bool | None = dll
        self.debug: bool | None = debug
        self.verbose: bool = verbose

    def stamp(self, path: str | Path) -> None:
        """Stamp a Win32 binary with version information."""
        if isinstance(path, str):
            path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(path)

        if CX_FREEZE_STAMP == "pywin32":
            if version_stamp is None:
                raise RuntimeError("install pywin32 extensions first")

            options = self
            setattr(options, "version", str(self.version))  # noqa: B010
            version_stamp(os.fspath(path), options)
            return

        # internal
        string_version_info = self.version_info(path)
        if CX_FREEZE_STAMP == "internal":
            if util is None:
                raise RuntimeError("cx_Freeze.util extensions not found")
            handle = util.BeginUpdateResource(path, 0)
            util.UpdateResource(handle, 16, 1, string_version_info.to_buffer())
            util.EndUpdateResource(handle, 0)

        if self.verbose:
            print("Stamped:", path)

    def version_info(self, path: Path) -> String:
        """Returns the String version info used to stamp the version."""
        major = self.version.major
        minor = self.version.minor
        micro = self.version.micro
        build = 0
        file_flags = 0
        if self.debug is None or path.stem.lower().endswith("_d"):
            file_flags += 1
        if self.version.is_devrelease:
            file_flags += 8
            build = self.version.dev
        elif self.version.is_prerelease:
            file_flags += 2
            build = self.version.pre[1]
        elif self.version.is_postrelease:
            file_flags += 0x20
            build = self.version.post
        elif len(self.version.release) >= 4:
            build = self.version.release[3]

        data = {
            "Comments": self.comments or "",
            "CompanyName": self.company or "",
            "FileDescription": self.description or "",
            "FileVersion": self.version.base_version,
            "InternalName": self.internal_name or path.name,
            "LegalCopyright": self.copyright or "",
            "LegalTrademarks": self.trademarks or "",
            "OriginalFilename": self.original_filename or path.name,
            "ProductName": self.product or "",
            "ProductVersion": str(self.version),
        }
        is_dll = self.dll
        if is_dll is None:
            is_dll = path.suffix.lower() in (".dll", ".pyd")
        fixed_file_info = VS_FIXEDFILEINFO(
            VS_FFI_SIGNATURE,
            VS_FFI_STRUCVERSION,
            (major << 16) | minor,
            (micro << 16) | build,
            (major << 16) | minor,
            (micro << 16) | build,
            VS_FFI_FILEFLAGSMASK,
            file_flags,
            VOS_NT_WINDOWS32,
            2 if is_dll else 1,  # VFT_DLL or VFT_APP
            0,
            0,
            0,
        )

        # string table with its children
        string_table = String(KEY_STRING_TABLE)
        for key, value in data.items():
            string_table.children(String(key, value))

        # create string file info and add string table as child
        string_file_info = String(KEY_STRING_FILE_INFO)
        string_file_info.children(string_table)

        # var file info has a child
        var_file_info = String(KEY_VAR_FILE_INFO)
        var_file_info.children(String("Translation", 0x04E40409))  # 0x409,1252

        # VS_VERSION_INFO is the first key and has two children
        string_version_info = String(KEY_VERSION_INFO, fixed_file_info)
        string_version_info.children(string_file_info)
        string_version_info.children(var_file_info)
        return string_version_info


if __name__ == "__main__":
    # simple test
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename",
        nargs="?",
        metavar="NAME",
        help="the name of the file (.dll, .pyd or .exe) to test version stamp",
    )
    parser.add_argument(
        "--version",
        action="store",
        dest="version",
        default="0.1",
        help="version to set as test",
    )
    parser.add_argument(
        "--dict",
        action="store_true",
        dest="as_dict",
        help="show version info as dict",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        dest="as_raw",
        help="show version info as raw bytes",
    )
    test_args = parser.parse_args()
    if test_args.filename is None:
        parser.error("filename must be specified")
    else:
        test_filename = Path(test_args.filename)

    test_version = VersionInfo(
        test_args.version,
        comments="cx_Freeze comments",
        description="cx_Freeze description",
        company="cx_Freeze company",
        product="cx_Freeze product",
        copyright="(c) 2023, cx_Freeze",
        trademarks="cx_Freeze (TM)",
    )

    if test_args.as_dict:
        print(test_version.version_info(test_filename))
    if test_args.as_raw:
        print(test_version.version_info(test_filename).to_buffer().hex(":"))
    test_version.stamp(test_filename)
