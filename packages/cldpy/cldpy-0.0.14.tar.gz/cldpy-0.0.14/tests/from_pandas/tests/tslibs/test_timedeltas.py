

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
import numpy_cloud as np
import pytest

from pandas_cloud._libs.tslibs.timedeltas import delta_to_nanoseconds

import pandas_cloud as pd


def test_delta_to_nanoseconds():
    obj = np.timedelta64(14, 'D')
    result = delta_to_nanoseconds(obj)
    assert result == 14 * 24 * 3600 * 1e9

    obj = pd.Timedelta(minutes=-7)
    result = delta_to_nanoseconds(obj)
    assert result == -7 * 60 * 1e9

    obj = pd.Timedelta(minutes=-7).to_pytimedelta()
    result = delta_to_nanoseconds(obj)
    assert result == -7 * 60 * 1e9

    obj = pd.offsets.Nano(125)
    result = delta_to_nanoseconds(obj)
    assert result == 125

    obj = 1
    result = delta_to_nanoseconds(obj)
    assert obj == 1

    obj = np.int64(2)
    result = delta_to_nanoseconds(obj)
    assert obj == 2

    obj = np.int32(3)
    result = delta_to_nanoseconds(obj)
    assert result == 3

    obj = np.array([123456789], dtype='m8[ns]')
    with pytest.raises(TypeError):
        delta_to_nanoseconds(obj)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
