## Test Execution
To Execute the tests in this folder, do the following steps in the parent
directory:

1 - Install cx_Freeze in development mode using:

 ```
 pip install -e .[test]
 ```

1.1 - Another method:

 ```
 pip install -r tests/requirements.txt --upgrade
 python setup.py develop --no-deps
 ```

2 - Call the tests (debuggable) with:

 ```
 python -m pytest -n0 --no-cov
 ```

2.1 - To speed up test runs using multiple CPUs: (uses pytest-xdist)

 ```
 python -m pytest -nauto --no-cov
 ```

3 - Call the tests with coverage (not-debuggable) with:

 ```
 python -m pytest -nauto --cov="cx_Freeze" --cov-report=html
 ```

3.1 - To navigate to the coverage report:

 ```
 python -m webbrowser -t ./build/coverage/index.html
 ```
