
Using cx_Freeze
===============

There are three different ways to use cx_Freeze. The first is to use the
included :ref:`cxfreeze script <script>`, which works well for simple scripts.
The second is to create a :ref:`distutils setup script <distutils>`, which can
be used for more complicated configuration or to retain the configuration for
future use. The third method involves working directly with the classes and
modules used internally by cx_Freeze, and should be reserved for complicated
scripts or extending or embedding.

There are three different options for producing executables as well. The first,
and the only option in earlier versions of cx_Freeze, is to append the zip file
of modules to the executable itself. The second option is creating a private
zip file with the same name as the executable but with the extension .zip. The
final, default option is to create a zip file called ``library.zip`` and place
all modules in this zip file. The final two options are necessary when creating
an RPM since the RPM builder automatically strips executables.

cx_Freeze normally produces a folder containing an executable file for your
program, along with the shared libraries (DLLs or .so files) needed to run it.
To make a simple Windows installer, use a :ref:`setup script <distutils>` with
the ``bdist_msi`` option. For a more advanced installer, use a separate tool
like `Inno Setup <http://www.jrsoftware.org/isinfo.php>`_ to package the files
cx_Freeze collects.

Using data files
----------------

Applications often need data files besides the code, such as icons. Using a
:ref:`setup script <distutils>`, you can list data files or directories in the
``include_files`` option to ``build_exe``. They'll be copied to the build
directory alongside the executable. Then to find them, your code can do::

    appdir = os.path.dirname(sys.argv[0])
    data_file_name = os.path.join(appdir, "some_data_directory",
            "some_file.dat")

An alternative is to embed data in code, for example by using `Qt's resource
system <http://developer.qt.nokia.com/doc/qt-4.8/resources.html>`_.

.. seealso:: `A tutorial covering resources in PyQt <http://lateral.netmanagers.com.ar/stories/BBS49.html>`_

Microsoft Visual C++ 2008 Redistributable Package
-------------------------------------------------

Since Python 2.6, Python on Windows requires the Microsoft Visual C++ 2008
Redistributable Package. Its DLLs are stored in a different way from most DLLs,
and cx_Freeze doesn't currently automatically copy them, (for technical
details, see `this mailing list thread
<http://www.mail-archive.com/cx-freeze-users@lists.sourceforge.net/msg00087.html>`_).
You have two options to deal with this:

1. Get your users to install the Microsoft Visual C++ 2008 Redistributable
   Package (free download, `for x86 (32 bit) Windows 
   <http://www.microsoft.com/download/en/details.aspx?displaylang=en&id=29>`_
   or `for x64 (64 bit) Windows
   <http://www.microsoft.com/download/en/details.aspx?displaylang=en&id=15336>`_).
   It's not uncommon for this to already be present on modern computers, but
   it's not (as far as we know) part of a standard Windows installation. Note
   that the "SP1" version of this *does not* work -- it has to exactly match
   the version which Python itself is compiled with.

2. Copy the following files from your system to the directory where cx_Freeze
   has assembled your files. You are responsible for making sure that you have
   the right to redistribute them::

    C:\WINDOWS\WinSxS\Manifests\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375.manifest
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcm90.dll
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcp90.dll
    C:\WINDOWS\WinSxS\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375\msvcr90.dll
