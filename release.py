"""
Script for creating all of the binaries that are released for the current
platform.
"""

import os
import sys

pythonVersions = [
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 0),
        (3, 1)
]

currentVersion = sys.version_info[:2]
pythonVersions.remove(currentVersion)
pythonVersions.append(currentVersion)

for majorVersion, minorVersion in pythonVersions:
    messageFragment = "for Python %s.%s" % (majorVersion, minorVersion)
    sys.stdout.write("Creating release %s.\n" % messageFragment)
    if sys.platform == "win32":
        python = "c:/python%s%s/python" % (majorVersion, minorVersion)
        if majorVersion == 2 and minorVersion == 4:
            subCommand = "bdist_wininst"
        else:
            subCommand = "bdist_msi"
        command = "%s setup.py %s" % (python, subCommand)
        sys.stdout.write("Running command %s\n" % command)
        if os.system(command) != 0:
            sys.exit("Stopping. Build %s failed.\n" % messageFragment)
    else:
        python = "python%s.%s" % (majorVersion, minorVersion)
        command = "%s setup.py bdist_rpm --no-autoreq --python %s" % \
                (python, python)
        sys.stdout.write("Running command %s\n" % command)
        if os.system(command) != 0:
            sys.exit("Stopping. Build %s failed.\n" % messageFragment)

