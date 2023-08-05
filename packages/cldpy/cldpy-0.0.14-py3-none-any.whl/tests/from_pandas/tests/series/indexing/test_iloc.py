

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
# coding=utf-8
# pylint: disable-msg=E1101,W0612

import numpy_cloud as np

from pandas_cloud.compat import lrange, range

from pandas_cloud import Series
from pandas_cloud.util.testing import assert_almost_equal, assert_series_equal


def test_iloc():
    s = Series(np.random.randn(10), index=lrange(0, 20, 2))

    for i in range(len(s)):
        result = s.iloc[i]
        exp = s[s.index[i]]
        assert_almost_equal(result, exp)

    # pass a slice
    result = s.iloc[slice(1, 3)]
    expected = s.loc[2:4]
    assert_series_equal(result, expected)

    # test slice is a view
    result[:] = 0
    assert (s[1:3] == 0).all()

    # list of integers
    result = s.iloc[[0, 2, 3, 4, 5]]
    expected = s.reindex(s.index[[0, 2, 3, 4, 5]])
    assert_series_equal(result, expected)


def test_iloc_nonunique():
    s = Series([0, 1, 2], index=[0, 1, 0])
    assert s.iloc[2] == 2

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
