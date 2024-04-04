Using cx_Freeze
===============

There are three different ways to use **cx_Freeze**:

1. Use the included :doc:`cxfreeze script <script>`.
2. Create a :doc:`setup script <setup_script>`. This is useful if you
   need extra options when freezing your program because you can save them in
   the script. Run ``cxfreeze-quickstart`` to generate a simple setup script.
3. Work directly with the classes and modules used internally by cx_Freeze.
   This should be reserved for complicated scripts or extending or embedding.

cx_Freeze normally produces a folder containing an executable file for your
program and the shared libraries (DLLs or .so files) needed to run it.
You can make a simple Windows installer using a :doc:`setup script <setup_script>`
with the ``bdist_msi`` option, or a Mac disk image with ``bdist_dmg``. For a
more advanced Windows installer, use a separate tool like `Inno Setup
<https://www.jrsoftware.org/isinfo.php>`_ to package the files that cx_Freeze
collects.

Python modules for your executables are stored in a zip file. Packages are
stored in the file system by default but can also be included in the zip file.
