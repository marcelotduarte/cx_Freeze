## Test Execution

To Execute the tests in this folder, do the following steps in the parent
directory:

1 - Install cx_Freeze in development mode using:

```
pip install -e.[test]
```

1.1 - Another method:

```
pip install -r requirements.txt --upgrade
pip install -r tests/requirements.txt --upgrade
pip install -e. --no-deps
```

2 - Call the tests (debuggable) with:

```
pytest -n0
```

2.1 - To speed up test runs using multiple CPUs: (uses pytest-xdist)

```
pytest --dist=loadfile -nauto
```

3 - Call the tests with coverage (not-debuggable) with:

```
coverage run
coverage combine
coverage report
coverage html
```

3.1 - To navigate to the coverage report:

```
python -m webbrowser -t ./build/coverage_html_report/index.html
```
