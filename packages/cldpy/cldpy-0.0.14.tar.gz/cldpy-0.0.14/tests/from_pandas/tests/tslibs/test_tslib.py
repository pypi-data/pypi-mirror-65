

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
"""Tests for functions from pandas_cloud._libs.tslibs"""

from datetime import date, datetime

from pandas_cloud._libs import tslibs


def test_normalize_date():
    value = date(2012, 9, 7)

    result = tslibs.normalize_date(value)
    assert (result == datetime(2012, 9, 7))

    value = datetime(2012, 9, 7, 12)

    result = tslibs.normalize_date(value)
    assert (result == datetime(2012, 9, 7))

    value = datetime(2007, 10, 1, 1, 12, 5, 10)

    actual = tslibs.normalize_date(value)
    assert actual == datetime(2007, 10, 1)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
