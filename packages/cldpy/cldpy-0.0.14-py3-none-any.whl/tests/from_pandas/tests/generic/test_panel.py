

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
# pylint: disable-msg=E1101,W0612

from warnings import catch_warnings, simplefilter

from pandas_cloud import Panel
from pandas_cloud.util.testing import (assert_panel_equal,
                                 assert_almost_equal)

import pandas_cloud.util.testing as tm
# rewrite: omit test decoratores (td) import
from .test_generic import Generic


class TestPanel(CloudArrayTest, Generic):
    _typ = Panel
    _comparator = lambda self, x, y: assert_panel_equal(x, y, by_blocks=True)

# rewrite: omit @td...
    def test_to_xarray(self):
        from xarray import DataArray

        with catch_warnings(record=True):
            simplefilter("ignore", FutureWarning)
            p = tm.makePanel()

            result = p.to_xarray()
            assert isinstance(result, DataArray)
            assert len(result.coords) == 3
            assert_almost_equal(list(result.coords.keys()),
                                ['items', 'major_axis', 'minor_axis'])
            assert len(result.dims) == 3

            # idempotency
            assert_panel_equal(result.to_pandas(), p)


# run all the tests, but wrap each in a warning catcher
for t in ['test_rename', 'test_get_numeric_data',
          'test_get_default', 'test_nonzero',
          'test_downcast', 'test_constructor_compound_dtypes',
          'test_head_tail',
          'test_size_compat', 'test_split_compat',
          'test_unexpected_keyword',
          'test_stat_unexpected_keyword', 'test_api_compat',
          'test_stat_non_defaults_args',
          'test_truncate_out_of_bounds',
          'test_metadata_propagation', 'test_copy_and_deepcopy',
          'test_pct_change', 'test_sample']:

    def f():
        def tester(self):
            f = getattr(super(TestPanel, self), t)
            with catch_warnings(record=True):
                simplefilter("ignore", FutureWarning)
                f()
        return tester

    setattr(TestPanel, t, f())

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
