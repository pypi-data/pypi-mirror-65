

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
import pandas_cloud as pd
import pandas_cloud.util.testing as tm


def test_getitem_callable():
    # GH 12533
    s = pd.Series(4, index=list('ABCD'))
    result = s[lambda x: 'A']
    assert result == s.loc['A']

    result = s[lambda x: ['A', 'B']]
    tm.assert_series_equal(result, s.loc[['A', 'B']])

    result = s[lambda x: [True, False, True, True]]
    tm.assert_series_equal(result, s.iloc[[0, 2, 3]])


def test_setitem_callable():
    # GH 12533
    s = pd.Series([1, 2, 3, 4], index=list('ABCD'))
    s[lambda x: 'A'] = -1
    tm.assert_series_equal(s, pd.Series([-1, 2, 3, 4], index=list('ABCD')))


def test_setitem_other_callable():
    # GH 13299
    inc = lambda x: x + 1

    s = pd.Series([1, 2, -1, 4])
    s[s < 0] = inc

    expected = pd.Series([1, 2, inc, 4])
    tm.assert_series_equal(s, expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
