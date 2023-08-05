

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

from pandas_cloud.io.msgpack import packb, unpackb
from .common import frombytes


def test_unpack_buffer():
    from array import array
    buf = array('b')
    frombytes(buf, packb((b'foo', b'bar')))
    obj = unpackb(buf, use_list=1)
    assert [b'foo', b'bar'] == obj


def test_unpack_bytearray():
    buf = bytearray(packb(('foo', 'bar')))
    obj = unpackb(buf, use_list=1)
    assert [b'foo', b'bar'] == obj
    expected_type = bytes
    assert all(type(s) == expected_type for s in obj)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
