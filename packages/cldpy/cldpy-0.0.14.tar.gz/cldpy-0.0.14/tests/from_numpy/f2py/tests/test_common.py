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
import sys
import pytest

import numpy_cloud as np
from . import util

from numpy.testing import assert_array_equal

def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))

class TestCommonBlock(CloudArrayTest):
    sources = [_path('src', 'common', 'block.f')]

    @pytest.mark.skipif(sys.platform=='win32',
                        reason='Fails with MinGW64 Gfortran (Issue #9673)')
    def test_common_block(self):
        self.module.initcb()
        assert_array_equal(self.module.block.long_bn,
                           np.array(1.0, dtype=np.float64))
        assert_array_equal(self.module.block.string_bn,
                           np.array('2', dtype='|S1'))
        assert_array_equal(self.module.block.ok,
                           np.array(3, dtype=np.int32))

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
