from pathlib import Path
from typing import List, Union

class BindError(Exception):
    ...

def AddIcon(target_path: Union[str, Path], exe_icon: Union[str, Path]):
    ...

def UpdateCheckSum(target_path: Union[str, Path]):
    ...

def GetSystemDir() -> str:
    ...

def GetWindowsDir() -> str:
    ...

def GetDependentFiles(path: Union[str, Path]) -> List[str]:
    ...
