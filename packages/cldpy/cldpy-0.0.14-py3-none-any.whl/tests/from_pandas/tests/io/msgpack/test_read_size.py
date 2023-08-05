

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
"""Test Unpacker's read_array_header and read_map_header methods"""
from pandas_cloud.io.msgpack import packb, Unpacker, OutOfData
UnexpectedTypeException = ValueError


def test_read_array_header():
    unpacker = Unpacker()
    unpacker.feed(packb(['a', 'b', 'c']))
    assert unpacker.read_array_header() == 3
    assert unpacker.unpack() == b'a'
    assert unpacker.unpack() == b'b'
    assert unpacker.unpack() == b'c'
    try:
        unpacker.unpack()
        assert 0, 'should raise exception'
    except OutOfData:
        assert 1, 'okay'


def test_read_map_header():
    unpacker = Unpacker()
    unpacker.feed(packb({'a': 'A'}))
    assert unpacker.read_map_header() == 1
    assert unpacker.unpack() == B'a'
    assert unpacker.unpack() == B'A'
    try:
        unpacker.unpack()
        assert 0, 'should raise exception'
    except OutOfData:
        assert 1, 'okay'


def test_incorrect_type_array():
    unpacker = Unpacker()
    unpacker.feed(packb(1))
    try:
        unpacker.read_array_header()
        assert 0, 'should raise exception'
    except UnexpectedTypeException:
        assert 1, 'okay'


def test_incorrect_type_map():
    unpacker = Unpacker()
    unpacker.feed(packb(1))
    try:
        unpacker.read_map_header()
        assert 0, 'should raise exception'
    except UnexpectedTypeException:
        assert 1, 'okay'


def test_correct_type_nested_array():
    unpacker = Unpacker()
    unpacker.feed(packb({'a': ['b', 'c', 'd']}))
    try:
        unpacker.read_array_header()
        assert 0, 'should raise exception'
    except UnexpectedTypeException:
        assert 1, 'okay'


def test_incorrect_type_nested_map():
    unpacker = Unpacker()
    unpacker.feed(packb([{'a': 'b'}]))
    try:
        unpacker.read_map_header()
        assert 0, 'should raise exception'
    except UnexpectedTypeException:
        assert 1, 'okay'

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
