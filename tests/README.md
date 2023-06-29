## Test Execution
To Execute the tests in this folder do the following steps

1 - Install cx_Freeze in development mode using:

 ```
 pip install -e .[test]
 ```

1.1 - Another method:

 ```
 pip install -r requirements-dev.txt --upgrade
 python setup.py develop --no-deps
 ```

3 - Call the tests (debuggable) with:

 ```
 python -m pytest
 ```

3.1 - To speed up test runs using multiple CPUs: (uses pytest-xdist)

 ```
 python -m pytest -n auto
 ```

3.2 - With coverage (not-debuggable) with:

 ```
 python -m pytest --cov="cx_Freeze" --cov-report=html
 ```

3.2.1 - To speed up the coverage (not-debuggable) with:

 ```
 python -m pytest -n auto --cov="cx_Freeze" --cov-report=html
 ```

3.2.2 - To navigate to the coverage report:

 ```
 python -m webbrowser -t ./htmlcov/index.html
 ```
