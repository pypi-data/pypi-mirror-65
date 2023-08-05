

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

import pytest
import pandas_cloud.core.dtypes.concat as _concat
from pandas_cloud import (
    Index, DatetimeIndex, PeriodIndex, TimedeltaIndex, Series, Period)


@pytest.mark.parametrize('to_concat, expected', [
    # int/float/str
    ([['a'], [1, 2]], ['i', 'object']),
    ([[3, 4], [1, 2]], ['i']),
    ([[3, 4], [1, 2.1]], ['i', 'f']),

    # datetimelike
    ([DatetimeIndex(['2011-01-01']), DatetimeIndex(['2011-01-02'])],
     ['datetime']),
    ([TimedeltaIndex(['1 days']), TimedeltaIndex(['2 days'])],
     ['timedelta']),

    # datetimelike object
    ([DatetimeIndex(['2011-01-01']),
      DatetimeIndex(['2011-01-02'], tz='US/Eastern')],
     ['datetime', 'datetime64[ns, US/Eastern]']),
    ([DatetimeIndex(['2011-01-01'], tz='Asia/Tokyo'),
      DatetimeIndex(['2011-01-02'], tz='US/Eastern')],
     ['datetime64[ns, Asia/Tokyo]', 'datetime64[ns, US/Eastern]']),
    ([TimedeltaIndex(['1 days']), TimedeltaIndex(['2 hours'])],
     ['timedelta']),
    ([DatetimeIndex(['2011-01-01'], tz='Asia/Tokyo'),
      TimedeltaIndex(['1 days'])],
     ['datetime64[ns, Asia/Tokyo]', 'timedelta'])])
@pytest.mark.parametrize('klass', [Index, Series])
def test_get_dtype_kinds(klass, to_concat, expected):
    to_concat_klass = [klass(c) for c in to_concat]
    result = _concat.get_dtype_kinds(to_concat_klass)
    assert result == set(expected)


@pytest.mark.parametrize('to_concat, expected', [
    ([PeriodIndex(['2011-01'], freq='M'),
      PeriodIndex(['2011-01'], freq='M')], ['period[M]']),
    ([Series([Period('2011-01', freq='M')]),
      Series([Period('2011-02', freq='M')])], ['period[M]']),
    ([PeriodIndex(['2011-01'], freq='M'),
      PeriodIndex(['2011-01'], freq='D')], ['period[M]', 'period[D]']),
    ([Series([Period('2011-01', freq='M')]),
      Series([Period('2011-02', freq='D')])], ['period[M]', 'period[D]'])])
def test_get_dtype_kinds_period(to_concat, expected):
    result = _concat.get_dtype_kinds(to_concat)
    assert result == set(expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
