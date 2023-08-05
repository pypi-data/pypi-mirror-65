

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
from pandas_cloud import SparseDataFrame, DataFrame, SparseSeries
from pandas_cloud.util import testing as tm


@pytest.mark.xfail(reason='Wrong SparseBlock initialization (GH#17386)',
                   strict=True)
def test_quantile():
    # GH 17386
    data = [[1, 1], [2, 10], [3, 100], [np.nan, np.nan]]
    q = 0.1

    sparse_df = SparseDataFrame(data)
    result = sparse_df.quantile(q)

    dense_df = DataFrame(data)
    dense_expected = dense_df.quantile(q)
    sparse_expected = SparseSeries(dense_expected)

    tm.assert_series_equal(result, dense_expected)
    tm.assert_sp_series_equal(result, sparse_expected)


@pytest.mark.xfail(reason='Wrong SparseBlock initialization (GH#17386)',
                   strict=True)
def test_quantile_multi():
    # GH 17386
    data = [[1, 1], [2, 10], [3, 100], [np.nan, np.nan]]
    q = [0.1, 0.5]

    sparse_df = SparseDataFrame(data)
    result = sparse_df.quantile(q)

    dense_df = DataFrame(data)
    dense_expected = dense_df.quantile(q)
    sparse_expected = SparseDataFrame(dense_expected)

    tm.assert_frame_equal(result, dense_expected)
    tm.assert_sp_frame_equal(result, sparse_expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
