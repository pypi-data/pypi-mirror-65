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
import textwrap
import pytest

from numpy.testing import assert_, assert_equal
from . import util


def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))


class TestMixed(CloudArrayTest):
    sources = [_path('src', 'mixed', 'foo.f'),
               _path('src', 'mixed', 'foo_fixed.f90'),
               _path('src', 'mixed', 'foo_free.f90')]

    @pytest.mark.slow
    def test_all(self):
        assert_(self.module.bar11() == 11)
        assert_(self.module.foo_fixed.bar12() == 12)
        assert_(self.module.foo_free.bar13() == 13)

    @pytest.mark.slow
    def test_docstring(self):
        expected = """
        a = bar11()

        Wrapper for ``bar11``.

        Returns
        -------
        a : int
        """
        assert_equal(self.module.bar11.__doc__,
                     textwrap.dedent(expected).lstrip())

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
