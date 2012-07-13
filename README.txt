Please see

http://cx_freeze.readthedocs.org

for documentation on how to use cx_Freeze.

To build:

python setup.py build
python setup.py install

NOTE: as of Python 3.3, the file importlib.h from the source used to build
Python is required in order to build cx_Freeze. Copy or link it so that the
compiler is able to include it.

