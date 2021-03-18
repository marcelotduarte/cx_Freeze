"""
Module for the VersionInfo base class.
"""

__all__ = ["VersionInfo"]


class VersionInfo:
    def __init__(
        self,
        version,
        internalName=None,
        originalFileName=None,
        comments=None,
        company=None,
        description=None,
        copyright=None,
        trademarks=None,
        product=None,
        dll=False,
        debug=False,
        verbose=True,
    ):
        parts = version.split(".")
        while len(parts) < 4:
            parts.append("0")
        self.version = ".".join(parts)
        self.internal_name = internalName
        self.original_filename = originalFileName
        self.comments = comments
        self.company = company
        self.description = description
        self.copyright = copyright
        self.trademarks = trademarks
        self.product = product
        self.dll = dll
        self.debug = debug
        self.verbose = verbose
