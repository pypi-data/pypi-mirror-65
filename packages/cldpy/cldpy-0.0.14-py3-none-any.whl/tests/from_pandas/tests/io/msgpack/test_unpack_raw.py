

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
"""Tests for cases where the user seeks to obtain packed msgpack objects"""

import io
from pandas_cloud.io.msgpack import Unpacker, packb


def test_write_bytes():
    unpacker = Unpacker()
    unpacker.feed(b'abc')
    f = io.BytesIO()
    assert unpacker.unpack(f.write) == ord('a')
    assert f.getvalue() == b'a'
    f = io.BytesIO()
    assert unpacker.skip(f.write) is None
    assert f.getvalue() == b'b'
    f = io.BytesIO()
    assert unpacker.skip() is None
    assert f.getvalue() == b''


def test_write_bytes_multi_buffer():
    long_val = (5) * 100
    expected = packb(long_val)
    unpacker = Unpacker(io.BytesIO(expected), read_size=3, max_buffer_size=3)

    f = io.BytesIO()
    unpacked = unpacker.unpack(f.write)
    assert unpacked == long_val
    assert f.getvalue() == expected

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
