import pytest
import os


@pytest.fixture()
def fix_test_dir():
    """ This fixture returns the root of the test folder """
    return os.path.dirname(__file__)


@pytest.fixture()
def fix_test_samples_dir(fix_test_dir):
    """ This fixture returns the samples folder for the tests """
    return os.path.join(fix_test_dir, "samples")
