"""Source of samples to tests."""

from pathlib import Path

# Each test description is a list of 5 items:
#
# 1. a module name that will be imported by ModuleFinder
# 2. a list of module names that ModuleFinder is required to find
# 3. a list of module names that ModuleFinder should complain
#    about because they are not found
# 4. a list of module names that ModuleFinder should complain
#    about because they MAY be not found
# 5. a string specifying packages to create; the format is obvious imo.

maybe_test = [
    "a.module",
    ["a", "a.module", "sys", "b"],
    ["c"],
    ["b.something"],
    """\
a/__init__.py
a/module.py
    from b import something
    from c import something
b/__init__.py
    from sys import *
""",
]

maybe_test_new = [
    "a.module",
    ["a", "a.module", "sys", "b", "__future__"],
    ["c"],
    ["b.something"],
    """\
a/__init__.py
a/module.py
    from b import something
    from c import something
b/__init__.py
    from __future__ import absolute_import
    from sys import *
""",
]

package_test = [
    "a.module",
    ["a", "a.b", "a.c", "a.module", "mymodule", "sys"],
    ["blahblah", "c"],
    [],
    """\
mymodule.py
a/__init__.py
    import blahblah
    from a import b
    import c
a/module.py
    import sys
    from a import b as x
    from a.c import sillyname
a/b.py
a/c.py
    from a.module import x
    import mymodule as sillyname
    from sys import version_info
""",
]

absolute_import_test = [
    "a.module",
    ["a", "a.module", "b", "b.x", "b.y", "b.z", "__future__", "sys", "gc"],
    ["blahblah", "z"],
    [],
    """\
mymodule.py
a/__init__.py
a/module.py
    from __future__ import absolute_import
    import sys # sys
    import blahblah # fails
    import gc # gc
    import b.x # b.x
    from b import y # b.y
    from b.z import * # b.z.*
a/gc.py
a/sys.py
    import mymodule
a/b/__init__.py
a/b/x.py
a/b/y.py
a/b/z.py
b/__init__.py
    import z
b/unused.py
b/x.py
b/y.py
b/z.py
""",
]

relative_import_test = [
    "a.module",
    [
        "__future__",
        "a",
        "a.module",
        "a.b",
        "a.b.y",
        "a.b.z",
        "a.b.c",
        "a.b.c.moduleC",
        "a.b.c.d",
        "a.b.c.e",
        "a.b.x",
        "gc",
    ],
    [],
    [],
    """\
mymodule.py
a/__init__.py
    from .b import y, z # a.b.y, a.b.z
a/module.py
    from __future__ import absolute_import # __future__
    import gc # gc
a/gc.py
a/sys.py
a/b/__init__.py
    from ..b import x # a.b.x
    #from a.b.c import moduleC
    from .c import moduleC # a.b.moduleC
a/b/x.py
a/b/y.py
a/b/z.py
a/b/g.py
a/b/c/__init__.py
    from ..c import e # a.b.c.e
a/b/c/moduleC.py
    from ..c import d # a.b.c.d
a/b/c/d.py
a/b/c/e.py
a/b/c/x.py
""",
]

relative_import_test_2 = [
    "a.module",
    [
        "a",
        "a.module",
        "a.sys",
        "a.b",
        "a.b.y",
        "a.b.z",
        "a.b.c",
        "a.b.c.d",
        "a.b.c.e",
        "a.b.c.moduleC",
        "a.b.c.f",
        "a.b.x",
        "a.another",
    ],
    [],
    [],
    """\
mymodule.py
a/__init__.py
    from . import sys # a.sys
a/another.py
a/module.py
    from .b import y, z # a.b.y, a.b.z
a/gc.py
a/sys.py
a/b/__init__.py
    from .c import moduleC # a.b.c.moduleC
    from .c import d # a.b.c.d
a/b/x.py
a/b/y.py
a/b/z.py
a/b/c/__init__.py
    from . import e # a.b.c.e
a/b/c/moduleC.py
    #
    from . import f   # a.b.c.f
    from .. import x  # a.b.x
    from ... import another # a.another
a/b/c/d.py
a/b/c/e.py
a/b/c/f.py
""",
]

relative_import_test_3 = [
    "a.module",
    ["a", "a.module"],
    ["a.bar"],
    [],
    """\
a/__init__.py
    def foo(): pass
a/module.py
    from . import foo
    from . import bar
""",
]

relative_import_test_4 = [
    "a.module",
    ["a", "a.module"],
    [],
    [],
    """\
a/__init__.py
    def foo(): pass
a/module.py
    from . import *
""",
]

bytecode_test = ["a", ["a"], [], [], ""]

syntax_error_test = [
    "a.module",
    ["a", "a.module", "b"],
    ["b.module"],
    [],
    """\
a/__init__.py
a/module.py
    import b.module
b/__init__.py
b/module.py
    ?  # SyntaxError: invalid syntax
""",
]


same_name_as_bad_test = [
    "a.module",
    ["a", "a.module", "b", "b.c"],
    ["c"],
    [],
    """\
a/__init__.py
a/module.py
    import c
    from b import c
b/__init__.py
b/c.py
""",
]

extended_opargs_test = [
    "a",
    ["a", "b"],
    [],
    [],
    f"""\
a.py
    {list(range(2**16))!r}
    import b
b.py
""",
]  # 2**16 constants

coding_default_utf8_test = [
    "a_utf8",
    ["a_utf8", "b_utf8"],
    [],
    [],
    """\
a_utf8.py
    # use the default of utf8
    print('Unicode test A code point 2090 \u2090 that is not valid in cp1252')
    import b_utf8
b_utf8.py
    # use the default of utf8
    print('Unicode test B code point 2090 \u2090 that is not valid in cp1252')
""",
]

coding_explicit_utf8_test = [
    "a_utf8",
    ["a_utf8", "b_utf8"],
    [],
    [],
    """\
a_utf8.py
    # coding=utf8
    print('Unicode test A code point 2090 \u2090 that is not valid in cp1252')
    import b_utf8
b_utf8.py
    # use the default of utf8
    print('Unicode test B code point 2090 \u2090 that is not valid in cp1252')
""",
]

coding_explicit_cp1252_test = [
    "a_cp1252",
    ["a_cp1252", "b_utf8"],
    [],
    [],
    b"""\
a_cp1252.py
    # coding=cp1252
    # 0xe2 is not allowed in utf8
    print('CP1252 test P\xe2t\xe9')
    import b_utf8
"""
    + """\
b_utf8.py
    # use the default of utf8
    print('Unicode test A code point 2090 \u2090 that is not valid in cp1252')
""".encode(),
]

sub_package_test = [
    "main",
    ["p", "p.p1", "p.q", "p.q.q1", "main"],
    [],
    [],
    """\
main.py
    import p.p1
    import p.q.q1
p/__init__.py
p/p1.py
    print('This is p.p1')
p/q/__init__.py
p/q/q1.py
    print('This is p.q.q1')
setup.py
    from cx_Freeze import Executable, setup
    setup(
        name="test",
        version="0.1",
        description="Sample for test with cx_Freeze",
        executables=[Executable("main.py")],
    )
""",
]


def create_package(test_dir: Path, source: str):
    """Create package in test_dir, based on source."""
    ofi = None
    try:
        for line in source.splitlines():
            if not isinstance(line, bytes):
                line = line.encode("utf-8")  # noqa: PLW2901
            if line.startswith((b" ", b"\t")):
                ofi.write(line.strip() + b"\n")
            else:
                if ofi:
                    ofi.close()
                if isinstance(line, bytes):
                    line = line.decode("utf-8")  # noqa: PLW2901
                path = test_dir / line.strip()
                path.parent.mkdir(parents=True, exist_ok=True)
                ofi = path.open("wb")
    finally:
        if ofi:
            ofi.close()
