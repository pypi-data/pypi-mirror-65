

# -- snippet for {numpy|pandas}_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()

# TODO: use mock.patch() instead of the code below
from pandas.util import testing
def setup_module():
    global old_assert_series_equal
    old_assert_series_equal = testing.assert_series_equal
    def assert_series_equal(*args, **kwargs):
        kwargs['check_series_type'] = False
        return old_assert_series_equal(*args, **kwargs)
    testing.assert_series_equal = assert_series_equal

def teardown_module():
    global old_assert_series_equal
    testing.assert_series_equal = old_assert_series_equal

# -- end {numpy|pandas}_cloud snippet -- #
import pytest

from pandas_cloud.compat import StringIO
from pandas_cloud import read_sas


class TestSas(CloudArrayTest, object):

    def test_sas_buffer_format(self):
        # see gh-14947
        b = StringIO("")

        msg = ("If this is a buffer object rather than a string "
               "name, you must specify a format string")
        with pytest.raises(ValueError, match=msg):
            read_sas(b)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
