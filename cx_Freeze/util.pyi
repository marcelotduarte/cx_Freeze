from pathlib import Path
from typing import List, Optional, Union

HANDLE = Optional[int]

class BindError(Exception):
    ...

def AddIcon(target_path: Union[str, Path], exe_icon: Union[str, Path]):
    ...

def BeginUpdateResource(
    path: Union[str, Path], delete_existing_resources: bool = True
) -> HANDLE:
    """Wrapper for BeginUpdateResource()."""
    ...

def UpdateResource(
    handle: HANDLE, resource_type: int, resource_id: int, resource_data: bytes
) -> None:
    """Wrapper for UpdateResource()."""
    ...

def EndUpdateResource(handle: HANDLE, discard_changes: bool):
    """Wrapper for EndUpdateResource()."""
    ...

def UpdateCheckSum(target_path: Union[str, Path]):
    ...

def GetSystemDir() -> str:
    ...

def GetWindowsDir() -> str:
    ...

def GetDependentFiles(path: Union[str, Path]) -> List[str]:
    ...
