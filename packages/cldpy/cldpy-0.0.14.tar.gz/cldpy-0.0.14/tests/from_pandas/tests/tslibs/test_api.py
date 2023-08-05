

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
"""Tests that the tslibs API is locked down"""

from pandas_cloud._libs import tslibs


def test_namespace():

    submodules = ['ccalendar',
                  'conversion',
                  'fields',
                  'frequencies',
                  'nattype',
                  'np_datetime',
                  'offsets',
                  'parsing',
                  'period',
                  'resolution',
                  'strptime',
                  'timedeltas',
                  'timestamps',
                  'timezones']

    api = ['NaT',
           'iNaT',
           'OutOfBoundsDatetime',
           'Period',
           'IncompatibleFrequency',
           'Timedelta',
           'Timestamp',
           'delta_to_nanoseconds',
           'ints_to_pytimedelta',
           'localize_pydatetime',
           'normalize_date',
           'tz_convert_single']

    expected = set(submodules + api)
    names = [x for x in dir(tslibs) if not x.startswith('__')]
    assert set(names) == expected

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
