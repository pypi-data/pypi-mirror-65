

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
from datetime import datetime

import numpy_cloud as np

from pandas_cloud._libs.tslibs import ccalendar


def test_get_day_of_year():
    assert ccalendar.get_day_of_year(2001, 3, 1) == 60
    assert ccalendar.get_day_of_year(2004, 3, 1) == 61
    assert ccalendar.get_day_of_year(1907, 12, 31) == 365
    assert ccalendar.get_day_of_year(2004, 12, 31) == 366

    dt = datetime.fromordinal(1 + np.random.randint(365 * 4000))
    result = ccalendar.get_day_of_year(dt.year, dt.month, dt.day)
    expected = (dt - dt.replace(month=1, day=1)).days + 1
    assert result == expected

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
