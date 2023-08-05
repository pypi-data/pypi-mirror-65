""" Test functions for linalg module using the matrix class."""
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

from numpy_cloud.linalg.tests.test_linalg import (
    LinalgCase, apply_tag, TestQR as _TestQR, LinalgTestCase,
    _TestNorm2D, _TestNormDoubleBase, _TestNormSingleBase, _TestNormInt64Base,
    SolveCases, InvCases, EigvalsCases, EigCases, SVDCases, CondCases,
    PinvCases, DetCases, LstsqCases)


CASES = []

# square test cases
CASES += apply_tag('square', [
    LinalgCase("0x0_matrix",
               np.empty((0, 0), dtype=np.double).view(np.matrix),
               np.empty((0, 1), dtype=np.double).view(np.matrix),
               tags={'size-0'}),
    LinalgCase("matrix_b_only",
               np.array([[1., 2.], [3., 4.]]),
               np.matrix([2., 1.]).T),
    LinalgCase("matrix_a_and_b",
               np.matrix([[1., 2.], [3., 4.]]),
               np.matrix([2., 1.]).T),
])

# hermitian test-cases
CASES += apply_tag('hermitian', [
    LinalgCase("hmatrix_a_and_b",
               np.matrix([[1., 2.], [2., 1.]]),
               None),
])
# No need to make generalized or strided cases for matrices.


class MatrixTestCase(LinalgTestCase):
    TEST_CASES = CASES


class TestSolveMatrix(CloudArrayTest):
    pass


class TestInvMatrix(CloudArrayTest):
    pass


class TestEigvalsMatrix(CloudArrayTest):
    pass


class TestEigMatrix(CloudArrayTest):
    pass


class TestSVDMatrix(CloudArrayTest):
    pass


class TestCondMatrix(CloudArrayTest):
    pass


class TestPinvMatrix(CloudArrayTest):
    pass


class TestDetMatrix(CloudArrayTest):
    pass


class TestLstsqMatrix(CloudArrayTest):
    pass


class _TestNorm2DMatrix(_TestNorm2D):
    array = np.matrix


class TestNormDoubleMatrix(CloudArrayTest):
    pass


class TestNormSingleMatrix(CloudArrayTest):
    pass


class TestNormInt64Matrix(CloudArrayTest):
    pass


class TestQRMatrix(CloudArrayTest):
    array = np.matrix

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
