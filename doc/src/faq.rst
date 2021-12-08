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
  normally be excluded (a common use is to include "libffi.so").
* Data files are a bit more complex - see :ref:`data_files`.

Specifying modules and packages
-------------------------------

The definitions of modules and packages are different. See python documentation.

* |modules_link|.
* |packages_link|.

.. |modules_link| raw:: html

   <a href="https://docs.python.org/3/tutorial/modules.html" target="_blank">Modules</a>

.. |packages_link| raw:: html

   <a href="https://docs.python.org/3/tutorial/modules.html#packages" target="_blank">Packages</a>

Windows command prompt appears briefly
--------------------------------------

If there's a problem with your frozen application, you may see a command prompt
window appear briefly when you try to run it, and then disappear again. This
happens when a console-mode executable exits quickly, usually if there's an
error as soon as it starts.

There are two ways to debug what's going on:

1. Freeze your application with the ``Win32GUI`` base (see :doc:`setup_script`
   or :doc:`script`). This doesn't use a console window, and reports errors in
   a dialog box.
2. Alternatively, start a command prompt yourself and launch the frozen
   executable from the command line. This will let you see any error messages
   in the console.

Freezing for other platforms
----------------------------

**cx_Freeze** works on Windows, Mac and Linux, but on each platform it only
makes an executable that runs on that platform. So if you want to freeze your
programs for Windows, freeze it on Windows; if you want to run it on Macs,
freeze it on a Mac.

At a pinch, you can try to make a Windows executable using |winehq_link|. Our
experience is that you need to copy some files in manually after **cx_Freeze**
has run to make the executable work. We don't recommend this option.

.. |winehq_link| raw:: html

   <a href="https://www.winehq.org/" target="_blank">Wine</a>

.. _data_files:

Using data files
----------------

Applications often need data files besides the code, such as icons. Using a
:ref:`setup script <setup_script>`, you can list data files or directories in the
``include_files`` option to ``build_exe``. They'll be copied to the build
directory alongside the executable. Then to find them, use code like this:

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

An alternative is to embed data in code, for example by using `Qt's resource
system <https://doc.qt.io/qt-5/resources.html>`_.

Microsoft Visual C++ Redistributable Package
--------------------------------------------

Python 3.6-3.10 on Windows requires the Visual C++ Redistributable for Visual
Studio 2015, 2017 or 2019 (the redistributables are shared), and because of how
this is installed, cx_Freeze doesn't automatically copy it for your application.

You're responsible for checking the license conditions associated with the DLLs
you have installed.

* If your license allows you to distribute these files, specify the
  ``include_msvcr`` option to :ref:`cx_freeze_build_exe` to have them
  distributed automatically.

* If not, your users or your installer will need to install the Microsoft
  Visual C++ Redistributable Package (a free download from Microsoft).
  It's not uncommon for this to already be present on modern computers, but
  it's not, as far as we know, part of a standard Windows installation.
  
  Download:

     * |vc_redist_32|
     * |vc_redist_64|

.. |vc_redist_32| raw:: html

   <a href="https://aka.ms/vs/16/release/vc_redist.x86.exe" target="_blank">for x86 (32 bit) Windows</a>

.. |vc_redist_64| raw:: html

   <a href="https://aka.ms/vs/16/release/vc_redist.x64.exe" target="_blank">for x64 (64 bit) Windows</a>

Single-file executables
-----------------------

**cx_Freeze** does not support building a single file exe, where all of the
libraries for your application are embedded in one executable file.

You can use other tools to compress the build directory from **cx_Freeze**
into a self-extracting archive:

* `IExpress <https://en.wikipedia.org/wiki/IExpress>`_

* `7zip sfx <https://7zip.bugaco.com/7zip/MANUAL/switches/sfx.htm>`_
