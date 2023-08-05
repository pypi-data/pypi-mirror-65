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
from numpy.testing import assert_equal

class TestDot(CloudArrayTest):
    def test_matscalar(self):
        b1 = np.matrix(np.ones((3, 3), dtype=complex))
        assert_equal(b1*1.0, b1)


def test_diagonal():
    b1 = np.matrix([[1,2],[3,4]])
    diag_b1 = np.matrix([[1, 4]])
    array_b1 = np.array([1, 4])

    assert_equal(b1.diagonal(), diag_b1)
    assert_equal(np.diagonal(b1), array_b1)
    assert_equal(np.diag(b1), array_b1)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
