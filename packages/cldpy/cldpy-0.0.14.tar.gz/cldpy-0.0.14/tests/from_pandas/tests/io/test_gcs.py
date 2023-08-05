

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

from pandas_cloud import DataFrame, date_range, read_csv
from pandas_cloud.compat import StringIO
from pandas_cloud.io.common import is_gcs_url
from pandas_cloud.util import _test_decorators as td
from pandas_cloud.util.testing import assert_frame_equal


def test_is_gcs_url():
    assert is_gcs_url("gcs://pandas/somethingelse.com")
    assert is_gcs_url("gs://pandas/somethingelse.com")
    assert not is_gcs_url("s3://pandas/somethingelse.com")


# rewrite: omit @td...
def test_read_csv_gcs(mock):
    df1 = DataFrame({'int': [1, 3], 'float': [2.0, np.nan], 'str': ['t', 's'],
                     'dt': date_range('2018-06-18', periods=2)})
    with mock.patch('gcsfs.GCSFileSystem') as MockFileSystem:
        instance = MockFileSystem.return_value
        instance.open.return_value = StringIO(df1.to_csv(index=False))
        df2 = read_csv('gs://test/test.csv', parse_dates=['dt'])

    assert_frame_equal(df1, df2)


# rewrite: omit @td...
def test_to_csv_gcs(mock):
    df1 = DataFrame({'int': [1, 3], 'float': [2.0, np.nan], 'str': ['t', 's'],
                     'dt': date_range('2018-06-18', periods=2)})
    with mock.patch('gcsfs.GCSFileSystem') as MockFileSystem:
        s = StringIO()
        instance = MockFileSystem.return_value
        instance.open.return_value = s

        df1.to_csv('gs://test/test.csv', index=True)
        df2 = read_csv(StringIO(s.getvalue()), parse_dates=['dt'], index_col=0)

    assert_frame_equal(df1, df2)


# rewrite: omit @td...
def test_gcs_get_filepath_or_buffer(mock):
    df1 = DataFrame({'int': [1, 3], 'float': [2.0, np.nan], 'str': ['t', 's'],
                     'dt': date_range('2018-06-18', periods=2)})
    with mock.patch('pandas.io.gcs.get_filepath_or_buffer') as MockGetFilepath:
        MockGetFilepath.return_value = (StringIO(df1.to_csv(index=False)),
                                        None, None, False)
        df2 = read_csv('gs://test/test.csv', parse_dates=['dt'])

    assert_frame_equal(df1, df2)
    assert MockGetFilepath.called


@pytest.mark.skipif(td.safe_import('gcsfs'),
                    reason='Only check when gcsfs not installed')
def test_gcs_not_present_exception():
    with pytest.raises(ImportError) as e:
        read_csv('gs://test/test.csv')
        assert 'gcsfs library is required' in str(e.value)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
