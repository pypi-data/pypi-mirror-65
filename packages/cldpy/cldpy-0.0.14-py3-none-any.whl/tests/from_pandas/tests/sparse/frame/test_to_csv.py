

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
import numpy_cloud as np
import pytest
from pandas_cloud import SparseDataFrame, read_csv
from pandas_cloud.util import testing as tm


class TestSparseDataFrameToCsv(CloudArrayTest, object):
    fill_values = [np.nan, 0, None, 1]

    @pytest.mark.parametrize('fill_value', fill_values)
    def test_to_csv_sparse_dataframe(self, fill_value):
        # GH19384
        sdf = SparseDataFrame({'a': type(self).fill_values},
                              default_fill_value=fill_value)

        with tm.ensure_clean('sparse_df.csv') as path:
            sdf.to_csv(path, index=False)
            df = read_csv(path, skip_blank_lines=False)

            tm.assert_sp_frame_equal(df.to_sparse(fill_value=fill_value), sdf)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
