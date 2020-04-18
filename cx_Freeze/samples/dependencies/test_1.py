"""Use getdependentfiles.py in a batch of tests"""

# This sample uses the getdependentfiles.py script to try to get the
# dependents of some predetermined files.

import os
import sys

try:
    import cx_Freeze
except ImportError:
    sys.stderr.write('Please install a cx-freeze package to test')
    sys.exit(-1)

program = '%s getdependentfiles.py' % sys.executable
dlls = os.path.join(sys.base_prefix, 'DLLs')
scripts = os.path.join(sys.base_prefix, 'Scripts')
cx_Freeze_dir = os.path.dirname(cx_Freeze.__file__)

dependencies_to_check = [
    os.path.join(sys.base_prefix, 'python.exe'),
    os.path.join(sys.base_prefix, "python%s%s.dll" % sys.version_info[:2]),
    sys.executable,
    os.path.join(dlls, '_ctypes.pyd'),
    os.path.join(dlls, '_sqlite3.pyd'),
    os.path.join(dlls, '_ssl.pyd'),
    os.path.join(scripts, 'pip.exe'),
    os.path.join(cx_Freeze_dir, 'bases', 'Console.exe'),
    ]

print('testing with default PATH environ')
cmdline = program + ' ' + ' '.join(dependencies_to_check)
for line in os.popen(cmdline):
    print(line, end='')
print()

print('testing with sys.path into PATH environ')
os.environ['PATH'] = os.pathsep.join(sys.path) + os.pathsep + os.environ['PATH']
cmdline = program + ' ' + ' '.join(dependencies_to_check)
for line in os.popen(cmdline):
    print(line, end='')
print()
