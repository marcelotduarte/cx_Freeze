Frequently Asked Questions
==========================

Problems with running frozen programs
-------------------------------------

A common problem is that **cx_Freeze** hasn't automatically detected that a
file needs to be copied. Modules that your code imports are detected, but if
they're dynamically loaded - e.g. by a plugin system - you have to tell
**cx_Freeze** about them. This is easy using a :doc:`setup_script`:

* For Python code, specify the module names in the :option:`includes` or
  :option:`packages` options.
* List the module's compiled libraries (.dll or .so files) in the
  :option:`include_files` option.
* Use :option:`bin_includes` to include dependencies of binary files that would
  normally be excluded (common use is to include "libffi.so").
* Data files are a bit more complex - see :ref:`data_files`.

Problems with freezing programs
-------------------------------

To determine which packages need to be copied with your application,
**cx_Freeze** follows the imports. If your installation contains a lot of
packages, this may lead to undesired behavior, such as **cx_Freeze**
encountering a recursion error when trying to compute the list of dependencies,
or the `lib` folder of the frozen application containing many unnecessary
packages.
In this case, use **cx_Freeze** in a virtualenv. Alternatively, the
`setup_script` also offers the :option:`excludes` option to explicitly
exclude dependencies that would otherwise be included.

Specifying modules and packages
-------------------------------

The definitions of modules and packages are different. See Python documentation.

* :pythondocs:`Modules <tutorial/modules.html>`.
* :pythondocs:`Packages <tutorial/modules.html#packages>`.

Windows command prompt appears briefly
--------------------------------------

If there's a problem with your frozen application, you may see a command prompt
window appear briefly when you try to run it, and then disappear again. This
happens when a console-mode executable exits quickly, usually if there's an
error as soon as it starts.

There are two ways to debug what's going on:

1. Freeze your application with the ``gui`` base (see :doc:`setup_script`
   or :doc:`script`). This doesn't use a console window and reports errors in
   a dialog box.
2. Alternatively, start a command prompt yourself and launch the frozen
   executable from the command line. This will let you see any error messages
   in the console.

Freezing for other platforms
----------------------------

**cx_Freeze** works on Windows, Mac, and Linux, but on each platform, it only
makes an executable that runs on that platform. So if you want to freeze your
programs for Windows, freeze it on Windows; if you want to run it on Macs,
freeze it on a Mac.

At a pinch, you can try to make a Windows executable using `Wine
<https://www.winehq.org/>`_. Our experience is that you need to copy some files
manually after **cx_Freeze** has run to make the executable work. We don't
recommend this option.

.. _data_files:

Using data files
----------------

Applications often need data files besides the code, such as icons. Using a
:doc:`setup script <setup_script>`, you can list data files or directories in
the :option:`include_files` option to :ref:`cx_freeze_build_exe`. They'll be
copied to the build directory alongside the executable. Then to find them,
use code like this:

  .. code-block:: python

    def find_data_file(filename):
        if getattr(sys, "frozen", False):
            # The application is frozen
            datadir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, filename)

Microsoft Visual C++ Redistributable Package
--------------------------------------------

Python 3.9-3.13 on Windows requires the `Microsoft Visual C++ Redistributable
<https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist>`_,
and because of how this is installed, **cx_Freeze** by default does NOT
automatically copy it for your application, however this can be changed,
but note that:

* You're responsible for checking the license conditions associated with the
  DLLs you have installed.

* If your license allows you to distribute these files, specify the
  :option:`include_msvcr` option or :option:`include_msvcr_version` option to
  :ref:`cx_freeze_build_exe` to have them distributed automatically.

* If not, your users or installers must install the Microsoft Visual C++
  Redistributable Package.
  It's not uncommon for this to already be present on modern computers, but,
  as far as we know, it's not part of a standard Windows installation.
  Download the `latest version <https://learn.microsoft.com/en-US/cpp/windows/
  latest-supported-vc-redist?view=msvc-170#
  latest-microsoft-visual-c-redistributable-version>`_ or use the `Winget tool
  <https://learn.microsoft.com/en-us/windows/package-manager/winget/>`_ on
  Windows 10 (build 16299 or later) or Windows 11 computers, using one of the
  following commands:

  .. code-block:: console

    winget upgrade Microsoft.VCRedist.2015+.x64
    winget upgrade Microsoft.VCRedist.2015+.x86

* If you are using an older Windows version than Windows 10 and the latest
  system updates are not installed, `Universal C Runtime
  <https://support.microsoft.com/en-us/help/2999226/
  update-for-universal-c-runtime-in-windows>`_ might also be required.
  You can set :option:`include_msvcr_version` option to 15
  (version 15 includes UCRT for Windows 8.1 and below). See more note-worthy
  information at `Distributing Software that uses the Universal CRT
  <https://devblogs.microsoft.com/cppblog/introducing-the-universal-crt/
  #distributing-software-that-uses-the-universal-crt>`_.

Removing the MAX_PATH Limitation
--------------------------------

Windows historically has limited path lengths to 260 characters. This meant
that paths longer than this would not resolve and errors would result.

Support for long paths is enabled for executables built in **cx_Freeze** as
long as the administrator activates the "Enable Win32 long paths" group policy
or sets ``LongPathsEnabled`` to ``1`` in the registry key
``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem``.

After changing the above option, no further configuration is required.

.. seealso:: `Enable Long Paths in Windows 10, Version 1607, and Later
   <https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#enable-long-paths-in-windows-10-version-1607-and-later>`_

Single-file executables
-----------------------

Recently, the :doc:`bdist_appimage` command was introduced for Linux,
which supports the construction of a single exe file, where all your
application's libraries are incorporated into an executable file.

On other systems, this is not supported by **cx_Freeze**, however, for
distribution, on Windows, you can use :doc:`bdist_msi`, and on macOS,
you can use :doc:`bdist_dmg`.

Also, you can use other tools to compress the build directory from
**cx_Freeze** into a self-extracting archive:

* `IExpress <https://en.wikipedia.org/wiki/IExpress>`_

* `7zip sfx <https://7zip.bugaco.com/7zip/MANUAL/switches/sfx.htm>`_

License for frozen programs
---------------------------

When a python script is frozen with **cx_Freeze**, a small amount of **cx_Freeze**
code is incorporated into the frozen program.  That code is used to configure
and start Python, running the script when the frozen program is launched.
The incorporated **cx_Freeze** code is covered by the terms of the
**cx_Freeze** :doc:`license`, which requires a copy of the license to be
included with the frozen program.

In order to make it easy to comply with this requirement, **cx_Freeze** will
automatically include a copy of the license, as a text file, as part of
the frozen program.

.. _patchelf:

How to install Patchelf
-----------------------

Patchelf is used in Linux and Unix-like systems (FreeBSD, etc, except macOS).
In Linux, cx_Freeze 6.10+ installs it using :pypi:`Patchelf <patchelf>` wheels.

If you have any trouble with it, because your platform is not supported by
binary wheels, please install it using the system package manager or from
sources.

 To install patchelf in debian-based:

  .. code-block:: console

    sudo apt-get install patchelf

 To install patchelf in fedora:

  .. code-block:: console

    dnf install patchelf

 Or install patchelf from `sources
 <https://github.com/NixOS/patchelf#compiling-and-testing>`_.


Multiprocessing support
-----------------------

On Linux, macOS, and Windows, :pythondocs:`multiprocessing
<library/multiprocessing.html>` support is managed by **cx_Freeze**,
including support for PyTorch
`torch.multiprocessing <https://pytorch.org/docs/stable/multiprocessing.html>`_
and `multiprocess <https://multiprocess.readthedocs.io/en/latest>`_.

Depending on the platform, multiprocessing supports three ways to start a
process. These start methods are: spawn, fork, and forkserver.

However, to produce an executable, you must use
`multiprocessing.freeze_support()`.

One needs to call this function straight after the
``if __name__ == "__main__"`` line of the main module. For example:

  .. code-block:: python

    from multiprocessing import Process, freeze_support


    def f():
        print("Hello from cx_Freeze")


    if __name__ == "__main__":
        freeze_support()
        Process(target=f).start()

If the `freeze_support()` line is omitted, then running the frozen executable
will raise RuntimeError on Windows. On Linux and macOS a similar message is
shown but cx_Freeze tries to run the program by injecting a `freeze_support`.
In addition, if the module is being run normally by the Python interpreter on
any OS (the program has not been frozen), then `freeze_support()` has no
effect.

To hide the runtime warning message, on Linux and macOS, specify in the
:ref:`cx_freeze_build_exe` command, the :option:`constants` option with the
value 'ignore_freeze_support_message=1'. For example, using the command line:

  .. code-block:: console

    cxfreeze --script test.py build_exe --constants='ignore_freeze_support_message=1'

.. note::

  Contrary to what the Python docs may state, you MUST use
  `multiprocessing.freeze_support()` on Linux, macOS, and Windows.
  On Linux and macOS, cx_Freeze patches the call to also handle
  `multiprocessing.spawn.freeze_support()` when needed.
