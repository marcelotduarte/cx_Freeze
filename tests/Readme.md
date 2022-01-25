## Test Execution
To Execute the tests in this folder do the following steps

1 - Install the `dev-requirements` dependencies using:

 `pip install -r dev-requirements.txt`

2 - Then install the module in development mode ( as seen in `setup.py`'s doc string )

```
Use one of the following commands to use the development mode:
    pip install -e .
    python setup.py develop -U
```

3 - Call the tests (debuggable) with:
```
python -m pytest
```

or with coverage (not-debuggable) with:
```
python -m pytest -m "not long" --cov="cx_Freeze" --cov-report=html
```
The coverage report will be saved into `./htmlcov` - open the `index.html` to navigate the report
