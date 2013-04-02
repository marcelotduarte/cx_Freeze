Frequently Asked Questions
==========================

Problems with running frozen programs
-------------------------------------

A common problem is that cx_Freeze hasn't automatically detected that a file
needs to be copied. Modules that your code imports are detected, but if they're
dynamically loaded - e.g. by a plugin system - you have to tell cx_Freeze about
them. This is easy using a :doc:`setup script <distutils>`:

* For Python code, specify the module names in the ``packages`` option.
* List compiled libraries (.dll or .so files) in the ``include-files`` option.
* Data files are a bit more complex - see :ref:`data_files`.

Freezing for other platforms
----------------------------

cx_Freeze works on Windows, Mac and Linux, but on each platform it only makes an
executable that runs on that platform. So if you want to freeze your program for
Windows, freeze it on Windows; if you want to run it on Macs, freeze it on a Mac.

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

Python on Windows requires the Microsoft Visual C++ Redistributable Package.
Its DLLs are stored in a different way from most DLLs,
and cx_Freeze doesn't currently automatically copy them, (for technical
details, see `this mailing list thread
<http://www.mail-archive.com/cx-freeze-users@lists.sourceforge.net/msg00087.html>`_).
You have two options to deal with this:

1. Get your users to install the Microsoft Visual C++ Redistributable
   Package (a free download from Microsoft). 
   It's not uncommon for this to already be present on modern computers, but
   it's not (as far as we know) part of a standard Windows installation. Note
   that the "SP1" version of this *does not* work -- it has to exactly match
   the version which Python itself is compiled with.
      * 2008 (Python 2.6-3.2) `for x86 (32 bit) Windows <http://www.microsoft.com/download/en/details.aspx?id=29>`_
        or `for x64 (64 bit) Windows <http://www.microsoft.com/download/en/details.aspx?id=15336>`_
      * 2010 (Python 3.3) `for x86 (32 bit) Windows <http://www.microsoft.com/en-gb/download/details.aspx?id=5555>`_
        or `for x64 (64 bit) Windows <http://www.microsoft.com/en-us/download/details.aspx?id=14632>`_

2. Copy the following files from your system to the directory where cx_Freeze
   has assembled your files. You are responsible for making sure that you have
   the right to redistribute them::

    C:\WINDOWS\WinSxS\Manifests\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375.manifest
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcm90.dll
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcp90.dll
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcr90.dll
    
   .. note:: These locations are for the 2008 version. The 2010 version will be
      in a similarly named directory.

