

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

import numpy_cloud as np
import pytest

from pandas_cloud.core.dtypes.dtypes import CategoricalDtype
from pandas_cloud.util.testing import assert_copy


def test_astype(idx):
    expected = idx.copy()
    actual = idx.astype('O')
    assert_copy(actual.levels, expected.levels)
    assert_copy(actual.labels, expected.labels)
    assert [level.name for level in actual.levels] == list(expected.names)

    with pytest.raises(TypeError, match="^Setting.*dtype.*object"):
        idx.astype(np.dtype(int))


@pytest.mark.parametrize('ordered', [True, False])
def test_astype_category(idx, ordered):
    # GH 18630
    msg = '> 1 ndim Categorical are not supported at this time'
    with pytest.raises(NotImplementedError, match=msg):
        idx.astype(CategoricalDtype(ordered=ordered))

    if ordered is False:
        # dtype='category' defaults to ordered=False, so only test once
        with pytest.raises(NotImplementedError, match=msg):
            idx.astype('category')

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
