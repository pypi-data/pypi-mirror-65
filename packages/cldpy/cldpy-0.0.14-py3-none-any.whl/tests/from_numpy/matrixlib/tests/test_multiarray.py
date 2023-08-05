from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import pytest

import numpy_cloud as np
from numpy.testing import assert_, assert_equal, assert_array_equal

class TestView(CloudArrayTest):
    def test_type(self):
        x = np.array([1, 2, 3])
        assert_(isinstance(x.view(np.matrix), np.matrix))

    def test_keywords(self):
        x = np.array([(1, 2)], dtype=[('a', np.int8), ('b', np.int8)])
        # We must be specific about the endianness here:
        y = x.view(dtype='<i2', type=np.matrix)
        assert_array_equal(y, [[513]])

        assert_(isinstance(y, np.matrix))
        assert_equal(y.dtype, np.dtype('<i2'))

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
