import os

def _norm_path(path: str) -> str:
    """Returns a normalized version of the specified path."""
    return os.path.normcase(os.path.realpath(path))
