

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
"""Tests for PeriodIndex behaving like a vectorized Period scalar"""

from pandas_cloud import PeriodIndex, Timedelta, date_range
import pandas_cloud.util.testing as tm


class TestPeriodIndexOps(CloudArrayTest, object):
    def test_start_time(self):
        index = PeriodIndex(freq='M', start='2016-01-01', end='2016-05-31')
        expected_index = date_range('2016-01-01', end='2016-05-31', freq='MS')
        tm.assert_index_equal(index.start_time, expected_index)

    def test_end_time(self):
        index = PeriodIndex(freq='M', start='2016-01-01', end='2016-05-31')
        expected_index = date_range('2016-01-01', end='2016-05-31', freq='M')
        expected_index += Timedelta(1, 'D') - Timedelta(1, 'ns')
        tm.assert_index_equal(index.end_time, expected_index)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
