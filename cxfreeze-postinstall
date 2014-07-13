#------------------------------------------------------------------------------
# cxfreeze-postinstall
#   Script run after installation on Windows to fix up the Python location in
# the script as well as create batch files.
#------------------------------------------------------------------------------

import distutils.sysconfig
import glob
import os

vars = distutils.sysconfig.get_config_vars()
prefix = vars["prefix"]
python = os.path.join(prefix, "python.exe")
scriptDir = os.path.join(prefix, "Scripts")
for fileName in glob.glob(os.path.join(scriptDir, "cxfreeze*")):

    # skip already created batch files if they exist
    name, ext = os.path.splitext(os.path.basename(fileName))
    if name == "cxfreeze-postinstall" or ext:
        continue

    # copy the file with the first line replaced with the correct python
    fullName = os.path.join(scriptDir, fileName)
    lines = open(fullName).readlines()
    outFile = open(fullName, "w")
    outFile.write("#!%s\n" % python)
    outFile.writelines(lines[1:])
    outFile.close()

    # create the batch file
    batchFileName = fullName + ".bat"
    command = "%s %s %%*" % (python, fullName)
    open(batchFileName, "w").write("@echo off\n\n%s" % command)

