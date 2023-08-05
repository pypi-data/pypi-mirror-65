

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
import numpy_cloud as np
import pytest

from pandas_cloud.core.dtypes import dtypes
from pandas_cloud.core.dtypes.common import is_extension_array_dtype

import pandas_cloud as pd
from pandas_cloud.core.arrays import ExtensionArray
import pandas_cloud.util.testing as tm


class DummyDtype(dtypes.ExtensionDtype):
    pass


class DummyArray(ExtensionArray):

    def __init__(self, data):
        self.data = data

    def __array__(self, dtype):
        return self.data

    @property
    def dtype(self):
        return DummyDtype()

    def astype(self, dtype, copy=True):
        # we don't support anything but a single dtype
        if isinstance(dtype, DummyDtype):
            if copy:
                return type(self)(self.data)
            return self

        return np.array(self, dtype=dtype, copy=copy)


class TestExtensionArrayDtype(CloudArrayTest, object):

    @pytest.mark.parametrize('values', [
        pd.Categorical([]),
        pd.Categorical([]).dtype,
        pd.Series(pd.Categorical([])),
        DummyDtype(),
        DummyArray(np.array([1, 2])),
    ])
    def test_is_extension_array_dtype(self, values):
        assert is_extension_array_dtype(values)

    @pytest.mark.parametrize('values', [
        np.array([]),
        pd.Series(np.array([])),
    ])
    def test_is_not_extension_array_dtype(self, values):
        assert not is_extension_array_dtype(values)


def test_astype():

    arr = DummyArray(np.array([1, 2, 3]))
    expected = np.array([1, 2, 3], dtype=object)

    result = arr.astype(object)
    tm.assert_numpy_array_equal(result, expected)

    result = arr.astype('object')
    tm.assert_numpy_array_equal(result, expected)


def test_astype_no_copy():
    arr = DummyArray(np.array([1, 2, 3], dtype=np.int64))
    result = arr.astype(arr.dtype, copy=False)

    assert arr is result

    result = arr.astype(arr.dtype)
    assert arr is not result


@pytest.mark.parametrize('dtype', [
    dtypes.DatetimeTZDtype('ns', 'US/Central'),
])
def test_is_not_extension_array_dtype(dtype):
    assert not isinstance(dtype, dtypes.ExtensionDtype)
    assert not is_extension_array_dtype(dtype)


@pytest.mark.parametrize('dtype', [
    dtypes.CategoricalDtype(),
    dtypes.IntervalDtype(),
])
def test_is_extension_array_dtype(dtype):
    assert isinstance(dtype, dtypes.ExtensionDtype)
    assert is_extension_array_dtype(dtype)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
