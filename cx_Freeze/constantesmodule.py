"""
Module for the ConstantsModule base class.
"""

import datetime
from keyword import iskeyword
import os
import socket
import tempfile
from typing import Dict, List, Optional
import uuid

from .exception import ConfigError
from .finder import ModuleFinder, Module

__all__ = ["ConstantsModule"]


class ConstantsModule:
    """
    Base ConstantsModule class.
    """

    def __init__(
        self,
        release_string: Optional[str] = None,
        copyright_string: Optional[str] = None,
        module_name: str = "BUILD_CONSTANTS",
        time_format: str = "%B %d, %Y %H:%M:%S",
        constants: Optional[List[str]] = None,
    ):
        self.module_name: str = module_name
        self.time_format: str = time_format
        self.values: Dict[str, str] = {}
        self.values["BUILD_RELEASE_STRING"] = release_string
        self.values["BUILD_COPYRIGHT"] = copyright_string
        if constants:
            for constant in constants:
                parts = constant.split("=", maxsplit=1)
                if len(parts) == 1:
                    name = constant
                    value = None
                else:
                    name, string_value = parts
                    value = eval(string_value)
                if (not name.isidentifier()) or iskeyword(name):
                    raise ConfigError(
                        f"Invalid constant name in ConstantsModule ({name!r})"
                    )
                self.values[name] = value

    def create(self, finder: ModuleFinder) -> Module:
        """Create the module which consists of declaration statements for each
        of the values."""
        today = datetime.datetime.today()
        source_timestamp = 0
        for module in finder.modules:
            if module.file is None:
                continue
            if module.source_is_zip_file:
                continue
            if not os.path.exists(module.file):
                raise ConfigError(
                    f"No file named {module.file} (for module {module.name})"
                )
            timestamp = os.stat(module.file).st_mtime
            source_timestamp = max(source_timestamp, timestamp)
        stamp = datetime.datetime.fromtimestamp(source_timestamp)
        self.values["BUILD_TIMESTAMP"] = today.strftime(self.time_format)
        self.values["BUILD_HOST"] = socket.gethostname().split(".")[0]
        self.values["SOURCE_TIMESTAMP"] = stamp.strftime(self.time_format)
        source_parts = []
        names = list(self.values.keys())
        names.sort()
        for name in names:
            value = self.values[name]
            source_parts.append(f"{name} = {value!r}")
        filename = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.py")
        with open(filename, "w") as file:
            file.write("\n".join(source_parts))
        module = finder.IncludeFile(filename, self.module_name)
        os.remove(filename)
        return module
