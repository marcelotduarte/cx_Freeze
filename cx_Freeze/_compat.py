import sys

if sys.version_info >= (3, 10):
    import importlib.metadata as importlib_metadata
else:
    try:
        import importlib_metadata
    except ImportError:
        import importlib.metadata as importlib_metadata

__all__ = ["importlib_metadata"]
