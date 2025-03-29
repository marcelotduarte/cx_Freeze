"""A collection of functions which are triggered automatically by finder when
multiprocess package is included.
"""

from __future__ import annotations

from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing as load_multiprocess,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_connection as load_multiprocess_connection,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_context as load_multiprocess_context,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_heap as load_multiprocess_heap,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_managers as load_multiprocess_managers,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_pool as load_multiprocess_pool,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_popen_spawn_win32 as load_multiprocess_popen_spawn_win32,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_reduction as load_multiprocess_reduction,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_resource_tracker as load_multiprocess_resource_tracker,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_shared_memory as load_multiprocess_shared_memory,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_sharedctypes as load_multiprocess_sharedctypes,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_spawn as load_multiprocess_spawn,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_synchronize as load_multiprocess_synchronize,
)
from cx_Freeze.hooks.multiprocessing import (
    load_multiprocessing_util as load_multiprocess_util,
)

__all__ = [
    "load_multiprocess",
    "load_multiprocess_connection",
    "load_multiprocess_context",
    "load_multiprocess_heap",
    "load_multiprocess_managers",
    "load_multiprocess_pool",
    "load_multiprocess_popen_spawn_win32",
    "load_multiprocess_reduction",
    "load_multiprocess_resource_tracker",
    "load_multiprocess_shared_memory",
    "load_multiprocess_sharedctypes",
    "load_multiprocess_spawn",
    "load_multiprocess_synchronize",
    "load_multiprocess_util",
]
