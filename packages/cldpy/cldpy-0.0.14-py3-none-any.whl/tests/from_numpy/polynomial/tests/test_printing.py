from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import numpy_cloud.polynomial as poly
from numpy.testing import assert_equal


class TestStr(CloudArrayTest):
    def test_polynomial_str(self):
        res = str(poly.Polynomial([0, 1]))
        tgt = 'poly([0. 1.])'
        assert_equal(res, tgt)

    def test_chebyshev_str(self):
        res = str(poly.Chebyshev([0, 1]))
        tgt = 'cheb([0. 1.])'
        assert_equal(res, tgt)

    def test_legendre_str(self):
        res = str(poly.Legendre([0, 1]))
        tgt = 'leg([0. 1.])'
        assert_equal(res, tgt)

    def test_hermite_str(self):
        res = str(poly.Hermite([0, 1]))
        tgt = 'herm([0. 1.])'
        assert_equal(res, tgt)

    def test_hermiteE_str(self):
        res = str(poly.HermiteE([0, 1]))
        tgt = 'herme([0. 1.])'
        assert_equal(res, tgt)

    def test_laguerre_str(self):
        res = str(poly.Laguerre([0, 1]))
        tgt = 'lag([0. 1.])'
        assert_equal(res, tgt)


class TestRepr(CloudArrayTest):
    def test_polynomial_str(self):
        res = repr(poly.Polynomial([0, 1]))
        tgt = 'Polynomial([0., 1.], domain=[-1,  1], window=[-1,  1])'
        assert_equal(res, tgt)

    def test_chebyshev_str(self):
        res = repr(poly.Chebyshev([0, 1]))
        tgt = 'Chebyshev([0., 1.], domain=[-1,  1], window=[-1,  1])'
        assert_equal(res, tgt)

    def test_legendre_repr(self):
        res = repr(poly.Legendre([0, 1]))
        tgt = 'Legendre([0., 1.], domain=[-1,  1], window=[-1,  1])'
        assert_equal(res, tgt)

    def test_hermite_repr(self):
        res = repr(poly.Hermite([0, 1]))
        tgt = 'Hermite([0., 1.], domain=[-1,  1], window=[-1,  1])'
        assert_equal(res, tgt)

    def test_hermiteE_repr(self):
        res = repr(poly.HermiteE([0, 1]))
        tgt = 'HermiteE([0., 1.], domain=[-1,  1], window=[-1,  1])'
        assert_equal(res, tgt)

    def test_laguerre_repr(self):
        res = repr(poly.Laguerre([0, 1]))
        tgt = 'Laguerre([0., 1.], domain=[0, 1], window=[0, 1])'
        assert_equal(res, tgt)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
