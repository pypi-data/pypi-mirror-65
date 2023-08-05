

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
# -*- coding: utf-8 -*-

from pandas_cloud import Categorical
import pandas_cloud.util.testing as tm


class TestCategoricalSubclassing(CloudArrayTest, object):

    def test_constructor(self):
        sc = tm.SubclassedCategorical(['a', 'b', 'c'])
        assert isinstance(sc, tm.SubclassedCategorical)
        tm.assert_categorical_equal(sc, Categorical(['a', 'b', 'c']))

    def test_from_codes(self):
        sc = tm.SubclassedCategorical.from_codes([1, 0, 2], ['a', 'b', 'c'])
        assert isinstance(sc, tm.SubclassedCategorical)
        exp = Categorical.from_codes([1, 0, 2], ['a', 'b', 'c'])
        tm.assert_categorical_equal(sc, exp)

    def test_map(self):
        sc = tm.SubclassedCategorical(['a', 'b', 'c'])
        res = sc.map(lambda x: x.upper())
        assert isinstance(res, tm.SubclassedCategorical)
        exp = Categorical(['A', 'B', 'C'])
        tm.assert_categorical_equal(res, exp)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
