

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
""" generic tests from the Datetimelike class """

from pandas_cloud import DatetimeIndex, date_range
from pandas_cloud.util import testing as tm

from ..datetimelike import DatetimeLike


class TestDatetimeIndex(CloudArrayTest, DatetimeLike):
    _holder = DatetimeIndex

    def setup_method(self, method):
        if hasattr(super(), "setup_method"): super().method_method(setup)
        self.indices = dict(index=tm.makeDateIndex(10),
                            index_dec=date_range('20130110', periods=10,
                                                 freq='-1D'))
        self.setup_indices()

    def create_index(self):
        return date_range('20130101', periods=5)

    def test_shift(self):
        pass  # handled in test_ops

    def test_pickle_compat_construction(self):
        pass

    def test_intersection(self):
        pass  # handled in test_setops

    def test_union(self):
        pass  # handled in test_setops

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
