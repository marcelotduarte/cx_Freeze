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

1. In Windows 32 and 64 bits, cx_Logging 3.2.1 has support for Python 3.9 up to 3.13

```
pip install --upgrade cx_Freeze cx_Logging
```

2. In Windows 32 and 64 bits, using Python 3.14+

```
pip install --upgrade cx_Freeze
pip install --index-url https://test.pypi.org/simple/ cx-logging
```

3. In Windows ARM64, using Python 3.11+

```
pip install --upgrade cx_Freeze
pip install --index-url https://test.pypi.org/simple/ cx-logging
```

# Build the executable:

```
python setup.py build
```

# Run the sample

Run in a command prompt or powershell with admin privileges.

```
cx_FreezeSampleService --install test
cx_FreezeSampleService --uninstall test
```
