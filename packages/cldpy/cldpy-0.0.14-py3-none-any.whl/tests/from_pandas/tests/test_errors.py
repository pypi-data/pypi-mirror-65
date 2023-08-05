

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

import pytest
import pandas_cloud  # noqa
import pandas_cloud as pd
from pandas_cloud.errors import AbstractMethodError


@pytest.mark.parametrize(
    "exc", ['UnsupportedFunctionCall', 'UnsortedIndexError',
            'OutOfBoundsDatetime',
            'ParserError', 'PerformanceWarning', 'DtypeWarning',
            'EmptyDataError', 'ParserWarning', 'MergeError'])
def test_exception_importable(exc):
    from pandas_cloud import errors
    e = getattr(errors, exc)
    assert e is not None

    # check that we can raise on them
    with pytest.raises(e):
        raise e()


def test_catch_oob():
    from pandas_cloud import errors

    try:
        pd.Timestamp('15000101')
    except errors.OutOfBoundsDatetime:
        pass


def test_error_rename():
    # see gh-12665
    from pandas_cloud.errors import ParserError
    from pandas_cloud.io.common import CParserError

    try:
        raise CParserError()
    except ParserError:
        pass

    try:
        raise ParserError()
    except CParserError:
        pass


class Foo(object):
    @classmethod
    def classmethod(cls):
        raise AbstractMethodError(cls, methodtype='classmethod')

    @property
    def property(self):
        raise AbstractMethodError(self, methodtype='property')

    def method(self):
        raise AbstractMethodError(self)


def test_AbstractMethodError_classmethod():
    xpr = "This classmethod must be defined in the concrete class Foo"
    with pytest.raises(AbstractMethodError, match=xpr):
        Foo.classmethod()

    xpr = "This property must be defined in the concrete class Foo"
    with pytest.raises(AbstractMethodError, match=xpr):
        Foo().property

    xpr = "This method must be defined in the concrete class Foo"
    with pytest.raises(AbstractMethodError, match=xpr):
        Foo().method()

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
