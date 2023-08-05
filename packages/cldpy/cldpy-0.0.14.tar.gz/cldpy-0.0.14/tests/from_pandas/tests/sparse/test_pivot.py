

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
import pandas_cloud as pd
import pandas_cloud.util.testing as tm


class TestPivotTable(CloudArrayTest, object):

    def setup_method(self, method):
        if hasattr(super(), "setup_method"): super().method_method(setup)
        self.dense = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar',
                                         'foo', 'bar', 'foo', 'foo'],
                                   'B': ['one', 'one', 'two', 'three',
                                         'two', 'two', 'one', 'three'],
                                   'C': np.random.randn(8),
                                   'D': np.random.randn(8),
                                   'E': [np.nan, np.nan, 1, 2,
                                         np.nan, 1, np.nan, np.nan]})
        self.sparse = self.dense.to_sparse()

    def test_pivot_table(self):
        res_sparse = pd.pivot_table(self.sparse, index='A', columns='B',
                                    values='C')
        res_dense = pd.pivot_table(self.dense, index='A', columns='B',
                                   values='C')
        tm.assert_frame_equal(res_sparse, res_dense)

        res_sparse = pd.pivot_table(self.sparse, index='A', columns='B',
                                    values='E')
        res_dense = pd.pivot_table(self.dense, index='A', columns='B',
                                   values='E')
        tm.assert_frame_equal(res_sparse, res_dense)

        res_sparse = pd.pivot_table(self.sparse, index='A', columns='B',
                                    values='E', aggfunc='mean')
        res_dense = pd.pivot_table(self.dense, index='A', columns='B',
                                   values='E', aggfunc='mean')
        tm.assert_frame_equal(res_sparse, res_dense)

        # ToDo: sum doesn't handle nan properly
        # res_sparse = pd.pivot_table(self.sparse, index='A', columns='B',
        #                             values='E', aggfunc='sum')
        # res_dense = pd.pivot_table(self.dense, index='A', columns='B',
        #                            values='E', aggfunc='sum')
        # tm.assert_frame_equal(res_sparse, res_dense)

    def test_pivot_table_multi(self):
        res_sparse = pd.pivot_table(self.sparse, index='A', columns='B',
                                    values=['D', 'E'])
        res_dense = pd.pivot_table(self.dense, index='A', columns='B',
                                   values=['D', 'E'])
        res_dense = res_dense.apply(lambda x: x.astype("Sparse[float64]"))
        tm.assert_frame_equal(res_sparse, res_dense)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
