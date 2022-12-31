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

or with coverage (not-debuggable) with:

  ```
  python -m pytest -m "not long" --cov="cx_Freeze" --cov-report=html
  ```

The coverage report will be saved into `./htmlcov` - open the `index.html` to
navigate the report
