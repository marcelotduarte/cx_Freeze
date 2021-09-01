## Test Execution
To Execute the tests in this folder do the following steps

1 -  If you're using `pipenv` run `pipenv sync -d` to get developer dependancies - if not manually `pip` install the packages
listed in the `pipfile`

2 - First install the module in development ( as seen in `setup.py`'s doc string )

```
Use one of the following commands to use the development mode:
    pip install -e .
    python setup.py develop
```

3 - Call the tests with `nosetests nose`