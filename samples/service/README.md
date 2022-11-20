# Service sample

A simple setup script for creating a Windows service.
See the comments in the Config.py and ServiceHandler.py files for more
information on how to set this up.

Installing the service is done with the option --install <Name> and
uninstalling the service is done with the option --uninstall <Name>. The
value for <Name> is intended to differentiate between different invocations
of the same service code -- for example for accessing different databases or
using different configuration files.


# Installation and requirements:

In a virtual environment, install by issuing the command:

```
pip install --upgrade cx_Freeze cx_Logging
```

cx_Logging 3.1 has support for Python 3.7 up to 3.11.

# Build the executable:

```
python setup.py build
```

# Run the sample

Run in a command prompt or powershell with admin priviliges.

```
cx_FreezeSampleService --install test
cx_FreezeSampleService --uninstall test
```
