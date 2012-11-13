"""
Script for creating all of the binaries that are released for the current
platform.
"""

import os
import sys

pythonVersions = os.environ["CX_FREEZE_PYTHON_VERSIONS"].split(",")
pythonFormat = os.environ["CX_FREEZE_PYTHON_FORMAT"]

for version in pythonVersions:
    majorVersion, minorVersion = [int(s) for s in version.split(".")]
    python = pythonFormat % (majorVersion, minorVersion)
    messageFragment = "for Python %s.%s" % (majorVersion, minorVersion)
    sys.stdout.write("Creating release %s.\n" % messageFragment)
    if sys.platform == "win32":
        if majorVersion == 2 and minorVersion == 4:
            subCommand = "bdist_wininst"
        else:
            subCommand = "bdist_msi"
        command = "%s setup.py %s" % (python, subCommand)
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

