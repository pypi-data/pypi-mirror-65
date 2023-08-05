

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
import pytest

import pandas_cloud as pd
import pandas_cloud.util.testing as tm


class TestDatetimeIndex(CloudArrayTest, object):

    @pytest.mark.parametrize('tz', ['US/Eastern', 'Asia/Tokyo'])
    def test_fillna_datetime64(self, tz):
        # GH 11343
        idx = pd.DatetimeIndex(['2011-01-01 09:00', pd.NaT,
                                '2011-01-01 11:00'])

        exp = pd.DatetimeIndex(['2011-01-01 09:00', '2011-01-01 10:00',
                                '2011-01-01 11:00'])
        tm.assert_index_equal(
            idx.fillna(pd.Timestamp('2011-01-01 10:00')), exp)

        # tz mismatch
        exp = pd.Index([pd.Timestamp('2011-01-01 09:00'),
                        pd.Timestamp('2011-01-01 10:00', tz=tz),
                        pd.Timestamp('2011-01-01 11:00')], dtype=object)
        tm.assert_index_equal(
            idx.fillna(pd.Timestamp('2011-01-01 10:00', tz=tz)), exp)

        # object
        exp = pd.Index([pd.Timestamp('2011-01-01 09:00'), 'x',
                        pd.Timestamp('2011-01-01 11:00')], dtype=object)
        tm.assert_index_equal(idx.fillna('x'), exp)

        idx = pd.DatetimeIndex(['2011-01-01 09:00', pd.NaT,
                                '2011-01-01 11:00'], tz=tz)

        exp = pd.DatetimeIndex(['2011-01-01 09:00', '2011-01-01 10:00',
                                '2011-01-01 11:00'], tz=tz)
        tm.assert_index_equal(
            idx.fillna(pd.Timestamp('2011-01-01 10:00', tz=tz)), exp)

        exp = pd.Index([pd.Timestamp('2011-01-01 09:00', tz=tz),
                        pd.Timestamp('2011-01-01 10:00'),
                        pd.Timestamp('2011-01-01 11:00', tz=tz)],
                       dtype=object)
        tm.assert_index_equal(
            idx.fillna(pd.Timestamp('2011-01-01 10:00')), exp)

        # object
        exp = pd.Index([pd.Timestamp('2011-01-01 09:00', tz=tz),
                        'x',
                        pd.Timestamp('2011-01-01 11:00', tz=tz)],
                       dtype=object)
        tm.assert_index_equal(idx.fillna('x'), exp)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
