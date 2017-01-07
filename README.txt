Please see

http://cx_freeze.readthedocs.org

for documentation on how to use cx_Freeze.

To install:

python -m pip install cx_freeze

If you do not have pip installed or would prefer a more manual installation
process, the following steps also work once the source package has been
downloaded and extracted:

python setup.py build
python setup.py install

To build with MSVC versions after 9.0 use this trick:
  set VS100COMNTOOLS=%VS140COMNTOOLS%
