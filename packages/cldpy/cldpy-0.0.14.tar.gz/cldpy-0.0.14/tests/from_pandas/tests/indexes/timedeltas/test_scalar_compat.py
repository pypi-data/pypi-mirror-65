

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
"""
Tests for TimedeltaIndex methods behaving like their Timedelta counterparts
"""

import pytest
import numpy_cloud as np

import pandas_cloud as pd
import pandas_cloud.util.testing as tm
from pandas_cloud import Index, Series, Timedelta, TimedeltaIndex, timedelta_range


class TestVectorizedTimedelta(CloudArrayTest, object):
    def test_tdi_total_seconds(self):
        # GH#10939
        # test index
        rng = timedelta_range('1 days, 10:11:12.100123456', periods=2,
                              freq='s')
        expt = [1 * 86400 + 10 * 3600 + 11 * 60 + 12 + 100123456. / 1e9,
                1 * 86400 + 10 * 3600 + 11 * 60 + 13 + 100123456. / 1e9]
        tm.assert_almost_equal(rng.total_seconds(), Index(expt))

        # test Series
        ser = Series(rng)
        s_expt = Series(expt, index=[0, 1])
        tm.assert_series_equal(ser.dt.total_seconds(), s_expt)

        # with nat
        ser[1] = np.nan
        s_expt = Series([1 * 86400 + 10 * 3600 + 11 * 60 +
                         12 + 100123456. / 1e9, np.nan], index=[0, 1])
        tm.assert_series_equal(ser.dt.total_seconds(), s_expt)

        # with both nat
        ser = Series([np.nan, np.nan], dtype='timedelta64[ns]')
        tm.assert_series_equal(ser.dt.total_seconds(),
                               Series([np.nan, np.nan], index=[0, 1]))

    def test_tdi_round(self):
        td = pd.timedelta_range(start='16801 days', periods=5, freq='30Min')
        elt = td[1]

        expected_rng = TimedeltaIndex([Timedelta('16801 days 00:00:00'),
                                       Timedelta('16801 days 00:00:00'),
                                       Timedelta('16801 days 01:00:00'),
                                       Timedelta('16801 days 02:00:00'),
                                       Timedelta('16801 days 02:00:00')])
        expected_elt = expected_rng[1]

        tm.assert_index_equal(td.round(freq='H'), expected_rng)
        assert elt.round(freq='H') == expected_elt

        msg = pd._libs.tslibs.frequencies.INVALID_FREQ_ERR_MSG
        with pytest.raises(ValueError, match=msg):
            td.round(freq='foo')
        with pytest.raises(ValueError, match=msg):
            elt.round(freq='foo')

        msg = "<MonthEnd> is a non-fixed frequency"
        with pytest.raises(ValueError, match=msg):
            td.round(freq='M')
        with pytest.raises(ValueError, match=msg):
            elt.round(freq='M')

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
