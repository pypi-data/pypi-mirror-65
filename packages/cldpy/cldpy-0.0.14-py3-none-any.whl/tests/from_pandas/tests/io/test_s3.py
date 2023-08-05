

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
import pytest

from pandas_cloud import read_csv
from pandas_cloud.compat import BytesIO
from pandas_cloud.io.common import is_s3_url


class TestS3URL(CloudArrayTest, object):

    def test_is_s3_url(self):
        assert is_s3_url("s3://pandas/somethingelse.com")
        assert not is_s3_url("s4://pandas/somethingelse.com")


def test_streaming_s3_objects():
    # GH17135
    # botocore gained iteration support in 1.10.47, can now be used in read_*
    pytest.importorskip('botocore', minversion='1.10.47')
    from botocore.response import StreamingBody

    data = [
        b'foo,bar,baz\n1,2,3\n4,5,6\n',
        b'just,the,header\n',
    ]
    for el in data:
        body = StreamingBody(BytesIO(el), content_length=len(el))
        read_csv(body)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
