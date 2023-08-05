from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import textwrap
import sys
import pytest
from . import util

from numpy.testing import assert_equal

class TestBlockDocString(CloudArrayTest):
    code = """
      SUBROUTINE FOO()
      INTEGER BAR(2, 3)

      COMMON  /BLOCK/ BAR
      RETURN
      END
    """

    @pytest.mark.skipif(sys.platform=='win32',
                        reason='Fails with MinGW64 Gfortran (Issue #9673)')
    def test_block_docstring(self):
        expected = "'i'-array(2,3)\n"
        assert_equal(self.module.block.__doc__, expected)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
