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
import pytest

from numpy.testing import assert_
from . import util


def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))


class TestAssumedShapeSumExample(CloudArrayTest):
    sources = [_path('src', 'assumed_shape', 'foo_free.f90'),
               _path('src', 'assumed_shape', 'foo_use.f90'),
               _path('src', 'assumed_shape', 'precision.f90'),
               _path('src', 'assumed_shape', 'foo_mod.f90'),
               ]

    @pytest.mark.slow
    def test_all(self):
        r = self.module.fsum([1, 2])
        assert_(r == 3, repr(r))
        r = self.module.sum([1, 2])
        assert_(r == 3, repr(r))
        r = self.module.sum_with_use([1, 2])
        assert_(r == 3, repr(r))

        r = self.module.mod.sum([1, 2])
        assert_(r == 3, repr(r))
        r = self.module.mod.fsum([1, 2])
        assert_(r == 3, repr(r))

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
