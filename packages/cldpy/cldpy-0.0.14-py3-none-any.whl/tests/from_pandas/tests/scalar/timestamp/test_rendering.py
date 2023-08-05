

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

from distutils.version import LooseVersion
import pprint

import dateutil
import pytest
import pytz  # noqa  # a test below uses pytz but only inside a `eval` call

from pandas_cloud import Timestamp


class TestTimestampRendering(CloudArrayTest, object):

    # dateutil zone change (only matters for repr)
    if LooseVersion(dateutil.__version__) >= LooseVersion('2.6.0'):
        timezones = ['UTC', 'Asia/Tokyo', 'US/Eastern',
                     'dateutil/US/Pacific']
    else:
        timezones = ['UTC', 'Asia/Tokyo', 'US/Eastern',
                     'dateutil/America/Los_Angeles']

    @pytest.mark.parametrize('tz', timezones)
    @pytest.mark.parametrize('freq', ['D', 'M', 'S', 'N'])
    @pytest.mark.parametrize('date', ['2014-03-07', '2014-01-01 09:00',
                                      '2014-01-01 00:00:00.000000001'])
    def test_repr(self, date, freq, tz):
        # avoid to match with timezone name
        freq_repr = "'{0}'".format(freq)
        if tz.startswith('dateutil'):
            tz_repr = tz.replace('dateutil', '')
        else:
            tz_repr = tz

        date_only = Timestamp(date)
        assert date in repr(date_only)
        assert tz_repr not in repr(date_only)
        assert freq_repr not in repr(date_only)
        assert date_only == eval(repr(date_only))

        date_tz = Timestamp(date, tz=tz)
        assert date in repr(date_tz)
        assert tz_repr in repr(date_tz)
        assert freq_repr not in repr(date_tz)
        assert date_tz == eval(repr(date_tz))

        date_freq = Timestamp(date, freq=freq)
        assert date in repr(date_freq)
        assert tz_repr not in repr(date_freq)
        assert freq_repr in repr(date_freq)
        assert date_freq == eval(repr(date_freq))

        date_tz_freq = Timestamp(date, tz=tz, freq=freq)
        assert date in repr(date_tz_freq)
        assert tz_repr in repr(date_tz_freq)
        assert freq_repr in repr(date_tz_freq)
        assert date_tz_freq == eval(repr(date_tz_freq))

    def test_repr_utcoffset(self):
        # This can cause the tz field to be populated, but it's redundant to
        # include this information in the date-string.
        date_with_utc_offset = Timestamp('2014-03-13 00:00:00-0400', tz=None)
        assert '2014-03-13 00:00:00-0400' in repr(date_with_utc_offset)
        assert 'tzoffset' not in repr(date_with_utc_offset)
        assert 'pytz.FixedOffset(-240)' in repr(date_with_utc_offset)
        expr = repr(date_with_utc_offset).replace("'pytz.FixedOffset(-240)'",
                                                  'pytz.FixedOffset(-240)')
        assert date_with_utc_offset == eval(expr)

    def test_timestamp_repr_pre1900(self):
        # pre-1900
        stamp = Timestamp('1850-01-01', tz='US/Eastern')
        repr(stamp)

        iso8601 = '1850-01-01 01:23:45.012345'
        stamp = Timestamp(iso8601, tz='US/Eastern')
        result = repr(stamp)
        assert iso8601 in result

    def test_pprint(self):
        # GH#12622
        nested_obj = {'foo': 1,
                      'bar': [{'w': {'a': Timestamp('2011-01-01')}}] * 10}
        result = pprint.pformat(nested_obj, width=50)
        expected = r"""{'bar': [{'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}},
         {'w': {'a': Timestamp('2011-01-01 00:00:00')}}],
 'foo': 1}"""
        assert result == expected

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
