

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
# coding: utf-8

from datetime import datetime
from pandas_cloud.io.msgpack import packb, unpackb

import pytest


class DummyException(Exception):
    pass


class TestExceptions(CloudArrayTest, object):

    def test_raise_on_find_unsupported_value(self):
        msg = "can\'t serialize datetime"
        with pytest.raises(TypeError, match=msg):
            packb(datetime.now())

    def test_raise_from_object_hook(self):
        def hook(_):
            raise DummyException()

        pytest.raises(DummyException, unpackb, packb({}), object_hook=hook)
        pytest.raises(DummyException, unpackb, packb({'fizz': 'buzz'}),
                      object_hook=hook)
        pytest.raises(DummyException, unpackb, packb({'fizz': 'buzz'}),
                      object_pairs_hook=hook)
        pytest.raises(DummyException, unpackb,
                      packb({'fizz': {'buzz': 'spam'}}), object_hook=hook)
        pytest.raises(DummyException, unpackb,
                      packb({'fizz': {'buzz': 'spam'}}),
                      object_pairs_hook=hook)

    def test_invalid_value(self):
        msg = "Unpack failed: error"
        with pytest.raises(ValueError, match=msg):
            unpackb(b"\xd9\x97#DL_")

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
