

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

import pandas_cloud as pd
import pandas_cloud.util.testing as tm


@pytest.fixture
def sparse_df():
    return pd.SparseDataFrame({0: {0: 1}, 1: {1: 1}, 2: {2: 1}})  # eye


@pytest.fixture
def multi_index3():
    return pd.MultiIndex.from_tuples([(0, 0), (1, 1), (2, 2)])


def test_sparse_frame_stack(sparse_df, multi_index3):
    ss = sparse_df.stack()
    expected = pd.SparseSeries(np.ones(3), index=multi_index3)
    tm.assert_sp_series_equal(ss, expected)


def test_sparse_frame_unstack(sparse_df):
    mi = pd.MultiIndex.from_tuples([(0, 0), (1, 0), (1, 2)])
    sparse_df.index = mi
    arr = np.array([[1, np.nan, np.nan],
                    [np.nan, 1, np.nan],
                    [np.nan, np.nan, 1]])
    unstacked_df = pd.DataFrame(arr, index=mi).unstack()
    unstacked_sdf = sparse_df.unstack()

    tm.assert_numpy_array_equal(unstacked_df.values, unstacked_sdf.values)


def test_sparse_series_unstack(sparse_df, multi_index3):
    frame = pd.SparseSeries(np.ones(3), index=multi_index3).unstack()
    tm.assert_sp_frame_equal(frame, sparse_df)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
