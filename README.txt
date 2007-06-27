WHAT?
cx_Freeze is a set of utilities for freezing Python scripts into executables
using many of the techniques found in Thomas Heller's py2exe, Gordon
McMillan's Installer and the Freeze utility that ships with Python itself.


WHY?
Why did I go to the trouble of creating another set of utilities when these
three utilities already existed?  The Freeze utility that comes with Python
itself requires a source distribution, a C compiler and linker which makes for
a complex environment for creating executables. In addition, this method is
very slow for creating executables as compared to the other methods. py2exe
is intended for development on Windows only and cx_Freeze is intended for
cross platform development. Installer uses an import hook which means that the
development environment and runtime environment are considerably different.


HOW?
How does it work? A base executable is created which contains code for
unpacking the list of frozen modules, starting up the Python interpreter and
passing control to the script which is being frozen. When a script is frozen,
the script is searched for all references to modules and these modules are then
byte compiled and written to the end of the base executable. If the modules
that are referenced are extensions written in C, these modules must be
included in the path in which the frozen executable is deployed.


BINARY INSTALLATION
Simply extract the archive into a directory. FreezePython searches for base
executables and initscripts relative to the directory in which FreezePython
is found. Note that it is important that the binary installation of cx_Freeze
is compatible with the installation of Python on your machine. If they are
not, you will get errors with respect to builtin modules not being found or
missing symbols. If this occurs, proceed to the source installation section.


SOURCE INSTALLATION
Extract the archive into a directory. In order to build cx_Freeze you need to
have gcc and Python development include files and libraries available. Run the
following commands.

python MakeFrozenBases.py
python FreezePython.py --no-copy-deps FreezePython.py

When these commands have completed successfully, the directory will be in the
same state as a binary installation. Note that on Windows these scripts assume
the presence of a mingw32 installation which can be acquired from
http://www.mingw.org.


FREEZING

Options and arguments to FreezePython can be seen by executing the command:

FreezePython --help

The default initscript is "Console" unless the --no-copy-deps/--keep-path
option is specified in which case the default is "ConsoleKeepPath". Each of
the initscripts is internally documented. You can add additional initscripts
by simply adding them to the "initscripts" directory. The initscript is
searched for modules as well as the script being frozen.

The default base executable is "Console". You can add additional base
executables by simply adding them to the "bases" directory.

The script specified on the command line is searched for modules by examining
the script for import statements. Each of those modules is then written to a
zip file and the zip file is appended to the base executable. Note that
imports done within extension modules and imports done with the __import__()
routine cannot be examined. In order to get these modules to be included in
the target executable, either add an explicit import in your script or use
the --include-modules command line option. You can examine the output of
FreezePython to determine which modules were actually included and where they
came from.


EXAMPLE

Assume that you have a script called "hello.py" containing the line
"print 'Hello World!'". To freeze this script you would issue the following
commands:

FreezePython --install-dir dist hello.py

This would create the following files (the exact number and names of files
will depend on the platform and version of Python that is used):

dist/hello
dist/pcre.so
dist/pwdmodule.so
dist/strop.so

These files can then be packaged in a zip or tar archive or RPM and
distributed to the target machine.


FEEDBACK
If you have any feedback, contact me at anthony.tuininga@gmail.com. In
particular, if any of the authors of the three other methods for freezing
executables wish to pool resources and merge technology, I am willing to
pursue that course.

