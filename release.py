"""
Script for creating all of the binaries that are released for the current
platform.
"""

import os
import sys

pythonVersions = sys.argv[1].split(",")
pythonFormat = os.environ["CX_FREEZE_PYTHON_FORMAT"]

minVersion = maxVersion = None
for argNum, argValue in enumerate(sys.argv[1:]):
    if argValue == "--min-version" and argNum + 2 < len(sys.argv):
        minVersion = tuple(int(s) for s in sys.argv[argNum + 2].split("."))
    elif argValue == "--max-version" and argNum + 2 < len(sys.argv):
        maxVersion = tuple(int(s) for s in sys.argv[argNum + 2].split("."))

for version in pythonVersions:
    majorVersion, minorVersion = [int(s) for s in version.split(".")]
    if minVersion is not None and (majorVersion, minorVersion) < minVersion:
        print "Skipping version (less than min)", version
        continue
    elif maxVersion is not None and (majorVersion, minorVersion) > maxVersion:
        print "Skipping version (greater than max)", version
        continue
    python = pythonFormat % (majorVersion, minorVersion)
    messageFragment = "for Python %s.%s" % (majorVersion, minorVersion)
    sys.stdout.write("Creating release %s.\n" % messageFragment)
    if sys.platform == "win32":
        command = "%s setup.py bdist_msi" % python
        sys.stdout.write("Running command %s\n" % command)
        if os.system(command) != 0:
            sys.exit("Stopping. Build %s failed.\n" % messageFragment)
    else:
        linkNames = ["python"]
        if majorVersion == 3:
            linkNames.append("python3")
        for linkName in linkNames:
            basePython = os.path.join(os.path.dirname(python), linkName)
            if os.path.exists(basePython):
                os.unlink(basePython)
            os.link(python, basePython)
        command = "%s setup.py bdist_rpm --no-autoreq" % python
        sys.stdout.write("Running command %s\n" % command)
        if os.system(command) != 0:
            sys.exit("Stopping. Build %s failed.\n" % messageFragment)

if sys.platform == "linux2":
    python = pythonFormat % (2, 6)
    basePython = os.path.join(os.path.dirname(python), "python")
    if os.path.exists(basePython):
        os.unlink(basePython)
    os.link(python, basePython)

