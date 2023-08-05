

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
"""
This file contains a minimal set of tests for compliance with the extension
array interface test suite, and should contain no other tests.
The test suite for the full functionality of the array is located in
`pandas/tests/arrays/`.

The tests in this file are inherited from the BaseExtensionTests, and only
minimal tweaks should be applied to get the tests passing (by overwriting a
parent method).

Additional tests should either be added to one of the BaseExtensionTests
classes (if they are relevant for the extension interface for all dtypes), or
be added to the array-specific tests in `pandas/tests/arrays/`.

"""
import numpy_cloud as np
import pytest

from pandas_cloud.core.dtypes.dtypes import IntervalDtype

from pandas_cloud import Interval
from pandas_cloud.core.arrays import IntervalArray
from pandas_cloud.tests.extension import base


def make_data():
    N = 100
    left = np.random.uniform(size=N).cumsum()
    right = left + np.random.uniform(size=N)
    return [Interval(l, r) for l, r in zip(left, right)]


@pytest.fixture
def dtype():
    return IntervalDtype()


@pytest.fixture
def data():
    """Length-100 PeriodArray for semantics test."""
    return IntervalArray(make_data())


@pytest.fixture
def data_missing():
    """Length 2 array with [NA, Valid]"""
    return IntervalArray.from_tuples([None, (0, 1)])


@pytest.fixture
def data_for_sorting():
    return IntervalArray.from_tuples([(1, 2), (2, 3), (0, 1)])


@pytest.fixture
def data_missing_for_sorting():
    return IntervalArray.from_tuples([(1, 2), None, (0, 1)])


@pytest.fixture
def na_value():
    return np.nan


@pytest.fixture
def data_for_grouping():
    a = (0, 1)
    b = (1, 2)
    c = (2, 3)
    return IntervalArray.from_tuples([b, b, None, None, a, a, b, c])


class BaseInterval(object):
    pass


class TestDtype(CloudArrayTest, BaseInterval, base.BaseDtypeTests):
    pass


class TestCasting(CloudArrayTest, BaseInterval, base.BaseCastingTests):
    pass


class TestConstructors(CloudArrayTest, BaseInterval, base.BaseConstructorsTests):
    pass


class TestGetitem(CloudArrayTest, BaseInterval, base.BaseGetitemTests):
    pass


class TestGrouping(CloudArrayTest, BaseInterval, base.BaseGroupbyTests):
    pass


class TestInterface(CloudArrayTest, BaseInterval, base.BaseInterfaceTests):
    pass


class TestReduce(CloudArrayTest, base.BaseNoReduceTests):
    pass


class TestMethods(CloudArrayTest, BaseInterval, base.BaseMethodsTests):

    @pytest.mark.skip(reason='addition is not defined for intervals')
    def test_combine_add(self, data_repeated):
        pass

    @pytest.mark.skip(reason="Not Applicable")
    def test_fillna_length_mismatch(self, data_missing):
        pass


class TestMissing(CloudArrayTest, BaseInterval, base.BaseMissingTests):
    # Index.fillna only accepts scalar `value`, so we have to skip all
    # non-scalar fill tests.
    unsupported_fill = pytest.mark.skip("Unsupported fillna option.")

    @unsupported_fill
    def test_fillna_limit_pad(self):
        pass

    @unsupported_fill
    def test_fillna_series_method(self):
        pass

    @unsupported_fill
    def test_fillna_limit_backfill(self):
        pass

    @unsupported_fill
    def test_fillna_series(self):
        pass

    def test_non_scalar_raises(self, data_missing):
        msg = "Got a 'list' instead."
        with pytest.raises(TypeError, match=msg):
            data_missing.fillna([1, 1])


class TestReshaping(CloudArrayTest, BaseInterval, base.BaseReshapingTests):
    pass


class TestSetitem(CloudArrayTest, BaseInterval, base.BaseSetitemTests):
    pass

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
