

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
import pandas_cloud as pd
import pandas_cloud.util.testing as tm
from pandas_cloud import MultiIndex


def check_level_names(index, names):
    assert [level.name for level in index.levels] == list(names)


def test_slice_keep_name():
    x = MultiIndex.from_tuples([('a', 'b'), (1, 2), ('c', 'd')],
                               names=['x', 'y'])
    assert x[1:].names == x.names


def test_index_name_retained():
    # GH9857
    result = pd.DataFrame({'x': [1, 2, 6],
                           'y': [2, 2, 8],
                           'z': [-5, 0, 5]})
    result = result.set_index('z')
    result.loc[10] = [9, 10]
    df_expected = pd.DataFrame({'x': [1, 2, 6, 9],
                                'y': [2, 2, 8, 10],
                                'z': [-5, 0, 5, 10]})
    df_expected = df_expected.set_index('z')
    tm.assert_frame_equal(result, df_expected)


def test_changing_names(idx):

    # names should be applied to levels
    level_names = [level.name for level in idx.levels]
    check_level_names(idx, idx.names)

    view = idx.view()
    copy = idx.copy()
    shallow_copy = idx._shallow_copy()

    # changing names should change level names on object
    new_names = [name + "a" for name in idx.names]
    idx.names = new_names
    check_level_names(idx, new_names)

    # but not on copies
    check_level_names(view, level_names)
    check_level_names(copy, level_names)
    check_level_names(shallow_copy, level_names)

    # and copies shouldn't change original
    shallow_copy.names = [name + "c" for name in shallow_copy.names]
    check_level_names(idx, new_names)


def test_take_preserve_name(idx):
    taken = idx.take([3, 0, 1])
    assert taken.names == idx.names


def test_copy_names():
    # Check that adding a "names" parameter to the copy is honored
    # GH14302
    multi_idx = pd.Index([(1, 2), (3, 4)], names=['MyName1', 'MyName2'])
    multi_idx1 = multi_idx.copy()

    assert multi_idx.equals(multi_idx1)
    assert multi_idx.names == ['MyName1', 'MyName2']
    assert multi_idx1.names == ['MyName1', 'MyName2']

    multi_idx2 = multi_idx.copy(names=['NewName1', 'NewName2'])

    assert multi_idx.equals(multi_idx2)
    assert multi_idx.names == ['MyName1', 'MyName2']
    assert multi_idx2.names == ['NewName1', 'NewName2']

    multi_idx3 = multi_idx.copy(name=['NewName1', 'NewName2'])

    assert multi_idx.equals(multi_idx3)
    assert multi_idx.names == ['MyName1', 'MyName2']
    assert multi_idx3.names == ['NewName1', 'NewName2']


def test_names(idx, index_names):

    # names are assigned in setup
    names = index_names
    level_names = [level.name for level in idx.levels]
    assert names == level_names

    # setting bad names on existing
    index = idx
    with pytest.raises(ValueError, match="^Length of names"):
        setattr(index, "names", list(index.names) + ["third"])
    with pytest.raises(ValueError, match="^Length of names"):
        setattr(index, "names", [])

    # initializing with bad names (should always be equivalent)
    major_axis, minor_axis = idx.levels
    major_labels, minor_labels = idx.labels
    with pytest.raises(ValueError, match="^Length of names"):
        MultiIndex(levels=[major_axis, minor_axis],
                   labels=[major_labels, minor_labels],
                   names=['first'])
    with pytest.raises(ValueError, match="^Length of names"):
        MultiIndex(levels=[major_axis, minor_axis],
                   labels=[major_labels, minor_labels],
                   names=['first', 'second', 'third'])

    # names are assigned
    index.names = ["a", "b"]
    ind_names = list(index.names)
    level_names = [level.name for level in index.levels]
    assert ind_names == level_names


def test_duplicate_level_names_access_raises(idx):
    # GH19029
    idx.names = ['foo', 'foo']
    with pytest.raises(ValueError, match='name foo occurs multiple times'):
        idx._get_level_number('foo')

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
