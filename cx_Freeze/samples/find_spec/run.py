import setuptools
import distutils.core
import sys

distutils.core.run_setup("setup.py", ["build_exe"])

print(
    sorted(sys.modules.keys())
)  # This shows that modules have been imported (if the freeze succeeds)
