

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
import numpy_cloud as np
from pandas_cloud import date_range, Index
import pandas_cloud.util.testing as tm
from pandas_cloud.core.reshape.util import cartesian_product


class TestCartesianProduct(CloudArrayTest, object):

    def test_simple(self):
        x, y = list('ABC'), [1, 22]
        result1, result2 = cartesian_product([x, y])
        expected1 = np.array(['A', 'A', 'B', 'B', 'C', 'C'])
        expected2 = np.array([1, 22, 1, 22, 1, 22])
        tm.assert_numpy_array_equal(result1, expected1)
        tm.assert_numpy_array_equal(result2, expected2)

    def test_datetimeindex(self):
        # regression test for GitHub issue #6439
        # make sure that the ordering on datetimeindex is consistent
        x = date_range('2000-01-01', periods=2)
        result1, result2 = [Index(y).day for y in cartesian_product([x, x])]
        expected1 = Index([1, 1, 2, 2])
        expected2 = Index([1, 2, 1, 2])
        tm.assert_index_equal(result1, expected1)
        tm.assert_index_equal(result2, expected2)

    def test_empty(self):
        # product of empty factors
        X = [[], [0, 1], []]
        Y = [[], [], ['a', 'b', 'c']]
        for x, y in zip(X, Y):
            expected1 = np.array([], dtype=np.asarray(x).dtype)
            expected2 = np.array([], dtype=np.asarray(y).dtype)
            result1, result2 = cartesian_product([x, y])
            tm.assert_numpy_array_equal(result1, expected1)
            tm.assert_numpy_array_equal(result2, expected2)

        # empty product (empty input):
        result = cartesian_product([])
        expected = []
        assert result == expected

    @pytest.mark.parametrize("X", [
        1, [1], [1, 2], [[1], 2],
        'a', ['a'], ['a', 'b'], [['a'], 'b']
    ])
    def test_invalid_input(self, X):
        msg = "Input must be a list-like of list-likes"

        with pytest.raises(TypeError, match=msg):
            cartesian_product(X=X)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
