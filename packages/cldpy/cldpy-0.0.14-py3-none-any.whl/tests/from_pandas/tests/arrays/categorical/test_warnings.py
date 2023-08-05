

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

import pandas_cloud.util.testing as tm


class TestCategoricalWarnings(CloudArrayTest, object):
    def test_tab_complete_warning(self, ip):
        # https://github.com/pandas-dev/pandas/issues/16409
        pytest.importorskip('IPython', minversion="6.0.0")
        from IPython.core.completer import provisionalcompleter

        code = "import pandas_cloud as pd; c = Categorical([])"
        ip.run_code(code)
        with tm.assert_produces_warning(None):
            with provisionalcompleter('ignore'):
                list(ip.Completer.completions('c.', 1))

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
