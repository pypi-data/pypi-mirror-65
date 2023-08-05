from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

# As we are testing matrices, we ignore its PendingDeprecationWarnings
try:
    import pytest
    pytestmark = pytest.mark.filterwarnings(
        'ignore:the matrix subclass is not:PendingDeprecationWarning')
except ImportError:
    pass

import numpy_cloud as np
import numpy_cloud.matlib
from numpy.testing import assert_array_equal, assert_

def test_empty():
    x = numpy.matlib.empty((2,))
    assert_(isinstance(x, np.matrix))
    assert_(x.shape, (1, 2))

def test_ones():
    assert_array_equal(numpy.matlib.ones((2, 3)),
                       np.matrix([[ 1.,  1.,  1.],
                                 [ 1.,  1.,  1.]]))

    assert_array_equal(numpy.matlib.ones(2), np.matrix([[ 1.,  1.]]))

def test_zeros():
    assert_array_equal(numpy.matlib.zeros((2, 3)),
                       np.matrix([[ 0.,  0.,  0.],
                                 [ 0.,  0.,  0.]]))

    assert_array_equal(numpy.matlib.zeros(2), np.matrix([[ 0.,  0.]]))

def test_identity():
    x = numpy.matlib.identity(2, dtype=int)
    assert_array_equal(x, np.matrix([[1, 0], [0, 1]]))

def test_eye():
    xc = numpy.matlib.eye(3, k=1, dtype=int)
    assert_array_equal(xc, np.matrix([[ 0,  1,  0],
                                      [ 0,  0,  1],
                                      [ 0,  0,  0]]))
    assert xc.flags.c_contiguous
    assert not xc.flags.f_contiguous

    xf = numpy.matlib.eye(3, 4, dtype=int, order='F')
    assert_array_equal(xf, np.matrix([[ 1,  0,  0,  0],
                                      [ 0,  1,  0,  0],
                                      [ 0,  0,  1,  0]]))
    assert not xf.flags.c_contiguous
    assert xf.flags.f_contiguous

def test_rand():
    x = numpy.matlib.rand(3)
    # check matrix type, array would have shape (3,)
    assert_(x.ndim == 2)

def test_randn():
    x = np.matlib.randn(3)
    # check matrix type, array would have shape (3,)
    assert_(x.ndim == 2)

def test_repmat():
    a1 = np.arange(4)
    x = numpy.matlib.repmat(a1, 2, 2)
    y = np.array([[0, 1, 2, 3, 0, 1, 2, 3],
                  [0, 1, 2, 3, 0, 1, 2, 3]])
    assert_array_equal(x, y)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
