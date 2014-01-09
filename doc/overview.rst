
Using cx_Freeze
===============

There are three different ways to use cx_Freeze:

1. Use the included :ref:`cxfreeze script <script>`.
2. Create a :ref:`distutils setup script <distutils>`. This is useful if you
   need extra options when freezing your program, because you can save them in
   the script. Run ``cxfreeze-quickstart`` to generate a simple setup script.
3. Work directly with the classes and modules used internally by cx_Freeze. This
   should be reserved for complicated scripts or extending or embedding.

cx_Freeze normally produces a folder containing an executable file for your
program, along with the shared libraries (DLLs or .so files) needed to run it.
You can make a simple Windows installer using a :ref:`setup script <distutils>`
with the ``bdist_msi`` option, or a Mac disk image with ``bdist_dmg``. For a
more advanced Windows installer, use a separate tool like `Inno Setup
<http://www.jrsoftware.org/isinfo.php>`_ to package the files cx_Freeze collects.

Python modules for your executables are stored in zip files. These can go in
three different places:

* The default is to create a zip file called ``library.zip`` and place
  all modules in this zip file.
* Each executable can have a private zip file with the same name as the
  executable (except for the .zip extension).
* Each executable can have a zip file of modules appended to it. This was the
  default in earlier versions of cx_Freeze, but it doesn't work with for
  creating an RPM, since the RPM builder strips executables.
