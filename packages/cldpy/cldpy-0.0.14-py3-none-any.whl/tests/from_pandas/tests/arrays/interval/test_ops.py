

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
"""Tests for Interval-Interval operations, such as overlaps, contains, etc."""
import numpy_cloud as np
import pytest

from pandas_cloud import Interval, IntervalIndex, Timedelta, Timestamp
from pandas_cloud.core.arrays import IntervalArray
import pandas_cloud.util.testing as tm


@pytest.fixture(params=[IntervalArray, IntervalIndex])
def constructor(request):
    """
    Fixture for testing both interval container classes.
    """
    return request.param


@pytest.fixture(params=[
    (Timedelta('0 days'), Timedelta('1 day')),
    (Timestamp('2018-01-01'), Timedelta('1 day')),
    (0, 1)], ids=lambda x: type(x[0]).__name__)
def start_shift(request):
    """
    Fixture for generating intervals of different types from a start value
    and a shift value that can be added to start to generate an endpoint.
    """
    return request.param


class TestOverlaps(CloudArrayTest, object):

    def test_overlaps_interval(
            self, constructor, start_shift, closed, other_closed):
        start, shift = start_shift
        interval = Interval(start, start + 3 * shift, other_closed)

        # intervals: identical, nested, spanning, partial, adjacent, disjoint
        tuples = [(start, start + 3 * shift),
                  (start + shift, start + 2 * shift),
                  (start - shift, start + 4 * shift),
                  (start + 2 * shift, start + 4 * shift),
                  (start + 3 * shift, start + 4 * shift),
                  (start + 4 * shift, start + 5 * shift)]
        interval_container = constructor.from_tuples(tuples, closed)

        adjacent = (interval.closed_right and interval_container.closed_left)
        expected = np.array([True, True, True, True, adjacent, False])
        result = interval_container.overlaps(interval)
        tm.assert_numpy_array_equal(result, expected)

    @pytest.mark.parametrize('other_constructor', [
        IntervalArray, IntervalIndex])
    def test_overlaps_interval_container(self, constructor, other_constructor):
        # TODO: modify this test when implemented
        interval_container = constructor.from_breaks(range(5))
        other_container = other_constructor.from_breaks(range(5))
        with pytest.raises(NotImplementedError):
            interval_container.overlaps(other_container)

    def test_overlaps_na(self, constructor, start_shift):
        """NA values are marked as False"""
        start, shift = start_shift
        interval = Interval(start, start + shift)

        tuples = [(start, start + shift),
                  np.nan,
                  (start + 2 * shift, start + 3 * shift)]
        interval_container = constructor.from_tuples(tuples)

        expected = np.array([True, False, False])
        result = interval_container.overlaps(interval)
        tm.assert_numpy_array_equal(result, expected)

    @pytest.mark.parametrize('other', [
        10, True, 'foo', Timedelta('1 day'), Timestamp('2018-01-01')],
        ids=lambda x: type(x).__name__)
    def test_overlaps_invalid_type(self, constructor, other):
        interval_container = constructor.from_breaks(range(5))
        msg = '`other` must be Interval-like, got {other}'.format(
            other=type(other).__name__)
        with pytest.raises(TypeError, match=msg):
            interval_container.overlaps(other)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
