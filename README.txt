Please see

http://cx_freeze.readthedocs.org

for documentation on how to use cx_Freeze.

To build:

python setup.py build
python setup.py install

To build with MSVC versions after 9.0 use this trick:
  set VS100COMNTOOLS=%VS140COMNTOOLS%
