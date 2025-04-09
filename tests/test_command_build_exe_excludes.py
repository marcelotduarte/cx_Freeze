"""Tests for cx_Freeze.command.build_exe using the --excludes option in the
following situations:
    - use of a regular package
    - use of a namespace package.
"""

from __future__ import annotations

SOURCE = """
namespacepack/firstchildpack/__init__.py
namespacepack/firstchildpack/main.py
    from namespacepack.firstchildpack.utils import name

    def main():
        print(f'Hello, {name()}!')

    if __name__ == '__main__':
        main()
namespacepack/firstchildpack/utils.py
    def name():
        return 'firstchildpack'
namespacepack/firstchildpack/configs/conf.yaml
    test_key: 'firstchildpack'
namespacepack/firstchildpack/models/model.txt
    Some model of firstchildpack
namespacepack/secondchildpack/__init__.py
namespacepack/secondchildpack/main.py
    from namespacepack.secondchildpack.utils import name

    def main():
        print(f'Hello, {name()}!')

    if __name__ == '__main__':
        main()
namespacepack/secondchildpack/utils.py
    def name():
        return 'secondchildpack'
namespacepack/secondchildpack/configs/conf.yaml
    test_key: 'secondchildpack'
namespacepack/secondchildpack/models/model.txt
    Some model of secondchildpack
regularpack/__init__.py
regularpack/main.py
    from regularpack.utils import name

    def main():
        print(f'Hello, {name()}!')

    if __name__ == '__main__':
        main()
regularpack/utils.py
    def name():
        return 'regularpack'
regularpack/configs/conf.yaml
    test_key: 'regularpack'
regularpack/models/model.txt
    Some model of regularpack
pyproject.toml
    [project]
    name = "Test"
    version = "0.1.2.3"

    [[tool.cxfreeze.executables]]
    script = "regularpack/main.py"
    target_name = "regularpack"

    [[tool.cxfreeze.executables]]
    script = "namespacepack/firstchildpack/main.py"
    target_name = "firstchildpack"

    [[tool.cxfreeze.executables]]
    script = "namespacepack/secondchildpack/main.py"
    target_name = "secondchildpack"

    [tool.cxfreeze.build_exe]
    excludes = [
        "regularpack.configs",
        "regularpack.models",
        "namespacepack.firstchildpack.configs",
        "namespacepack.firstchildpack.models",
        "namespacepack.secondchildpack.configs",
        "namespacepack.secondchildpack.models",
    ]
    packages = [
        "regularpack",
        "namespacepack.firstchildpack",
        "namespacepack.secondchildpack",
    ]
    silent = true
command
    cxfreeze build_exe
"""


def test_excludes(tmp_package) -> None:
    """Test the build_exe excludes option."""
    tmp_package.create(SOURCE)
    output = tmp_package.run()
    for fullname in (
        "regularpack",
        "namespacepack.firstchildpack",
        "namespacepack.secondchildpack",
    ):
        name = fullname.split(".")[-1]
        executable = tmp_package.executable(name)
        assert executable.is_file()

        output = tmp_package.run(executable, timeout=10)
        lines = output.splitlines()
        assert lines[0].startswith(f"Hello, {name}")

        pkg_dir = executable.parent / "lib" / fullname.replace(".", "/")
        for fn in pkg_dir.glob("*"):
            print(fn)
        assert len(list(pkg_dir.glob("*"))) == 3
