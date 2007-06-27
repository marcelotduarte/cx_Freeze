"""Make the frozen base executables."""

import distutils.sysconfig
import os
import sys

CC = os.environ.get("CC", "gcc")

# define function for building a base executable
def BuildBase(name, linkerFlags = "", sharedLib = False):
    vars = distutils.sysconfig.get_config_vars()
    sourceName = name + ".c"
    objectName = name + ".o"
    targetName = name
    if sharedLib:
        if sys.platform == "win32":
            targetName += ".dll"
        else:
            targetName += vars["SO"]
        linkerFlags = "-shared %s" % linkerFlags
    else:
        targetName += vars["EXE"]
    compilerFlags = "-c -I. -I%s -I%s" % \
            (distutils.sysconfig.get_python_inc(),
             distutils.sysconfig.get_python_inc(1))
    linkerFlags += " -s"
    if sys.platform == "win32":
        import win32api
        linkerFlags += " " + win32api.GetModuleFileName(sys.dllhandle)
    else:
        linkerFlags += " %s %s %s/%s" % \
                (vars["LDFLAGS"], vars["LINKFORSHARED"], vars["LIBPL"],
                 vars["INSTSONAME"])
        if sys.platform == "hp-ux11":
            linkerFlags += " -lcl"
        linkerFlags += " %s %s %s %s" % \
                (vars["LIBS"], vars["LIBM"], vars["LOCALMODLIBS"],
                 vars["BASEMODLIBS"])
    command = "%s %s -o %s %s" % (CC, compilerFlags, objectName, sourceName)
    print command
    if os.system(command) != 0:
        raise "Failed to compile %s" % sourceName
    command = "%s -o %s %s %s" % \
            (CC, os.path.join("bases", targetName), objectName, linkerFlags)
    print command
    if os.system(command) != 0:
        raise "Failed to link %s" % sourceName
    os.unlink(objectName)

# create the directory, if necessary
if not os.path.exists("bases"):
    os.mkdir("bases")

# build the base executables
BuildBase("Console")
BuildBase("ConsoleKeepPath")
if sys.platform == "win32":
    BuildBase("Win32GUI", "-mwindows")

