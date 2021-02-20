from cx_Freeze import setup, Executable

setup(
    name="hello",
    version="0.1",
    description="Sample cx_Freeze script",
    executables=[Executable("hello.py")],
    options={
        "build_exe": {
            "zip_include_packages": ["*"],
            "zip_exclude_packages": ["to_exclude"],
        }
    },
)
