import setuptools  # isort:skip
import distutils.core
import sys

distutils.core.run_setup("setup.py", ["build_exe"])

# This shows that modules have been imported (if the freeze succeeds)
print(sorted(sys.modules.keys()))
