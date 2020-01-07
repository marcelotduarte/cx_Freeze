Frequently Asked Questions
==========================

Problems with running frozen programs
-------------------------------------

A common problem is that cx_Freeze hasn't automatically detected that a file
needs to be copied. Modules that your code imports are detected, but if they're
dynamically loaded - e.g. by a plugin system - you have to tell cx_Freeze about
them. This is easy using a :doc:`setup script <distutils>`:

* For Python code, specify the module names in the ``includes`` or ``packages``
  options.
* List compiled libraries (.dll or .so files) in the ``include_files`` option.
* Data files are a bit more complex - see :ref:`data_files`.

Windows command prompt appears briefly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If there's a problem with your frozen application, you may see a command prompt
window appear briefly when you try to run it, and then disappear again. This
happens when a console-mode executable exits quickly, usually if there's an
error as soon as it starts.

There are two ways to debug what's going on:

1. Freeze your application with the ``Win32GUI`` base (see :doc:`distutils` or
   :doc:`script`). This doesn't use a console window, and reports errors in a
   dialog box.
2. Alternatively, start a command prompt yourself and launch the frozen
   executable from the command line. This will let you see any error messages in
   the console.

Freezing for other platforms
----------------------------

cx_Freeze works on Windows, Mac and Linux, but on each platform it only makes
an executable that runs on that platform. So if you want to freeze your program
for Windows, freeze it on Windows; if you want to run it on Macs, freeze it on
a Mac.

At a pinch, you can try to make a Windows executable using
`Wine <http://www.winehq.org/>`_. Our experience is that you need to copy some
files in manually after cx_Freeze has run to make the executable work. We don't
recommend this option.

.. _data_files:

Using data files
----------------

Applications often need data files besides the code, such as icons. Using a
:ref:`setup script <distutils>`, you can list data files or directories in the
``include_files`` option to ``build_exe``. They'll be copied to the build
directory alongside the executable. Then to find them, use code like this::

    def find_data_file(filename):
        if getattr(sys, 'frozen', False):
            # The application is frozen
            datadir = os.path.dirname(sys.executable)
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            datadir = os.path.dirname(__file__)
        return os.path.join(datadir, filename)

An alternative is to embed data in code, for example by using `Qt's resource
system <http://developer.qt.nokia.com/doc/qt-4.8/resources.html>`_.

.. seealso:: `A tutorial covering resources in PyQt <http://lateral.netmanagers.com.ar/stories/BBS49.html>`_

Microsoft Visual C++ Redistributable Package
--------------------------------------------

Python 3.5-3.8 on Windows requires the Visual C++ Redistributable for Visual
Studio 2015 or 2017 (the redistributables are shared), and because of how this
is installed, cx_Freeze doesn't automatically copy it for your application.
It's also not clear whether everyone has the right to redistribute the DLLs.
You're responsible for checking the license conditions associated with the DLLs
you have installed.

* If your license allows you to distribute these files, specify the
  ``include_msvcr`` option to :ref:`distutils_build_exe` to have them
  distributed automatically.

* If not, your users or your installer will need to install the Microsoft
  Visual C++ Redistributable Package (a free download from Microsoft).
  It's not uncommon for this to already be present on modern computers, but
  it's not, as far as we know, part of a standard Windows installation.
  
  Download:

     * `for x86 (32 bit) Windows <https://aka.ms/vs/16/release/vc_redist.x86.exe>`__
     * `for x64 (64 bit) Windows <https://aka.ms/vs/16/release/vc_redist.x64.exe>`__

Single-file executables
-----------------------

cx_Freeze does not support building a single file exe, where all of the
libraries for your application are embedded in one executable file.

You can use `IExpress <http://en.wikipedia.org/wiki/IExpress>`_ to compress the
build directory from cx_Freeze into a self-extracting archive: an exe which
unpacks your application into a temporary directory and runs it. IExpress is a
utility that's included with Windows, intended for making installers, but it
works equally well if you tell it to run the cx_Freeze-built exe after
extraction.

Alternatively, you can create a `self extracting archive using 7zip
<http://7zip.bugaco.com/7zip/MANUAL/switches/sfx.htm>`_. This is a bit more
complex than using IExpress, but might provide more flexibility, and allows you
to build your application using only open source tools.
