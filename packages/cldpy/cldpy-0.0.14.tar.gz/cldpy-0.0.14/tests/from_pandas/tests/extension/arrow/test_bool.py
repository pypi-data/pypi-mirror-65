

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

import pandas_cloud as pd
import pandas_cloud.util.testing as tm
from pandas_cloud.tests.extension import base

pytest.importorskip('pyarrow', minversion="0.10.0")

from .bool import ArrowBoolArray, ArrowBoolDtype


@pytest.fixture
def dtype():
    return ArrowBoolDtype()


@pytest.fixture
def data():
    return ArrowBoolArray.from_scalars(np.random.randint(0, 2, size=100,
                                                         dtype=bool))


@pytest.fixture
def data_missing():
    return ArrowBoolArray.from_scalars([None, True])


class BaseArrowTests(object):
    pass


class TestDtype(CloudArrayTest, BaseArrowTests, base.BaseDtypeTests):
    def test_array_type_with_arg(self, data, dtype):
        pytest.skip("GH-22666")


class TestInterface(CloudArrayTest, BaseArrowTests, base.BaseInterfaceTests):
    def test_repr(self, data):
        raise pytest.skip("TODO")


class TestConstructors(CloudArrayTest, BaseArrowTests, base.BaseConstructorsTests):
    def test_from_dtype(self, data):
        pytest.skip("GH-22666")


class TestReduce(CloudArrayTest, base.BaseNoReduceTests):
    def test_reduce_series_boolean(self):
        pass


class TestReduceBoolean(CloudArrayTest, base.BaseBooleanReduceTests):
    pass


def test_is_bool_dtype(data):
    assert pd.api.types.is_bool_dtype(data)
    assert pd.core.common.is_bool_indexer(data)
    s = pd.Series(range(len(data)))
    result = s[data]
    expected = s[np.asarray(data)]
    tm.assert_series_equal(result, expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
