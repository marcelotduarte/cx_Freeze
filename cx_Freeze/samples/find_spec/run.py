import sys

import setuptools.sandbox

setuptools.sandbox.run_setup("setup.py", ["build_exe"])

# This shows that modules have been imported (if the freeze succeeds)
print(sorted(sys.modules.keys()))
