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
from numpy_cloud.f2py.crackfortran import (
    _selected_int_kind_func as selected_int_kind,
    _selected_real_kind_func as selected_real_kind
    )
from . import util


def _path(*a):
    return os.path.join(*((os.path.dirname(__file__),) + a))


class TestKind(CloudArrayTest):
    sources = [_path('src', 'kind', 'foo.f90')]

    @pytest.mark.slow
    def test_all(self):
        selectedrealkind = self.module.selectedrealkind
        selectedintkind = self.module.selectedintkind

        for i in range(40):
            assert_(selectedintkind(i) in [selected_int_kind(i), -1],
                    'selectedintkind(%s): expected %r but got %r' %
                    (i, selected_int_kind(i), selectedintkind(i)))

        for i in range(20):
            assert_(selectedrealkind(i) in [selected_real_kind(i), -1],
                    'selectedrealkind(%s): expected %r but got %r' %
                    (i, selected_real_kind(i), selectedrealkind(i)))

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
