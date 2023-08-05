from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import os
import math
import pytest

import numpy_cloud as np
from numpy.testing import assert_raises, assert_equal

from . import util


def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))


class TestIntentInOut(CloudArrayTest):
    # Check that intent(in out) translates as intent(inout)
    sources = [_path('src', 'regression', 'inout.f90')]

    @pytest.mark.slow
    def test_inout(self):
        # non-contiguous should raise error
        x = np.arange(6, dtype=np.float32)[::2]
        assert_raises(ValueError, self.module.foo, x)

        # check values with contiguous array
        x = np.arange(3, dtype=np.float32)
        self.module.foo(x)
        assert_equal(x, [3, 1, 2])

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
