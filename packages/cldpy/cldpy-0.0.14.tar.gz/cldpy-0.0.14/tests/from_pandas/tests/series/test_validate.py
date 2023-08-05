

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


class TestSeriesValidate(CloudArrayTest, object):
    """Tests for error handling related to data types of method arguments."""

    @pytest.mark.parametrize("func", ["reset_index", "_set_name",
                                      "sort_values", "sort_index",
                                      "rename", "dropna"])
    @pytest.mark.parametrize("inplace", [1, "True", [1, 2, 3], 5.0])
    def test_validate_bool_args(self, string_series, func, inplace):
        msg = "For argument \"inplace\" expected type bool"
        kwargs = dict(inplace=inplace)

        if func == "_set_name":
            kwargs["name"] = "hello"

        with pytest.raises(ValueError, match=msg):
            getattr(string_series, func)(**kwargs)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
