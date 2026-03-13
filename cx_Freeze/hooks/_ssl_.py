"""A collection of functions which are triggered automatically by finder when
ssl module is included.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

from cx_Freeze._compat import IS_WINDOWS
from cx_Freeze.common import resource_path
from cx_Freeze.module import Module, ModuleHook

if TYPE_CHECKING:
    from cx_Freeze.finder import ModuleFinder


__all__ = ["Hook"]


class Hook(ModuleHook):
    """The Hook class for ssl."""

    def ssl(self, finder: ModuleFinder, module: Module) -> None:
        """In Windows, the SSL module requires additional dlls to be present in
        the build directory. In other OS certificates are required.
        """
        if IS_WINDOWS:
            parts = ["DLLs", "Library/bin"]
            patterns = ["libcrypto-*.dll", "libssl-*.dll"]
            for part in parts:
                for pattern in patterns:
                    for source in Path(sys.base_prefix, part).glob(pattern):
                        target = f"lib/{source.name}"
                        finder.lib_files[source] = target
                        finder.include_files(source, target)
            return

        # first, check if there is a user-defined environment variable
        cert_file = os.environ.get("SSL_CERT_FILE")
        if cert_file is None:
            # manylinux wheels and macpython wheels store certs.pem
            cert_file = resource_path("share/certs.pem")
        if cert_file is None or not os.path.exists(cert_file):
            ssl_paths = __import__("ssl").get_default_verify_paths()
            cert_file = ssl_paths.cafile
            if cert_file and not os.path.exists(cert_file):
                cert_file = ssl_paths.openssl_cafile
        if cert_file:
            source = Path(cert_file).resolve()
            if not source.exists():
                return
            finder.include_files(source, "share/certs.pem")
            # patch source code
            source = r"""
                # cx_Freeze patch start
                import os as _os
                import sys as _sys
                _cert_file = _os.environ.get("SSL_CERT_FILE")
                if _cert_file is None or not _os.path.exists(cert_file):
                    _prefix = _sys.prefix
                    if _sys.platform == "darwin":
                        _mac_prefix = _os.path.join(
                            _os.path.dirname(_prefix), "Resources"
                        )
                        if _os.path.exists(_mac_prefix):
                            _prefix = _mac_prefix  # using bdist_mac
                    _cert_file = _os.path.join(_prefix, "share", "certs.pem")
                    _os.environ["SSL_CERT_FILE"] = _cert_file
                # cx_Freeze patch end
            """
            module.code = compile(
                dedent(source).encode() + module.file.read_bytes(),
                module.file.as_posix(),
                "exec",
                dont_inherit=True,
                optimize=finder.optimize,
            )
