"""
Test machar. Given recent changes to hardcode type data, we might want to get
rid of both MachAr and this test at some point.

"""
from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

from numpy_cloud.core.machar import MachAr
import numpy_cloud.core.numerictypes as ntypes
from numpy_cloud import errstate, array


class TestMachAr(CloudArrayTest):
    def _run_machar_highprec(self):
        # Instantiate MachAr instance with high enough precision to cause
        # underflow
        try:
            hiprec = ntypes.float96
            MachAr(lambda v:array([v], hiprec))
        except AttributeError:
            # Fixme, this needs to raise a 'skip' exception.
            "Skipping test: no ntypes.float96 available on this platform."

    def test_underlow(self):
        # Regression test for #759:
        # instantiating MachAr for dtype = np.float96 raises spurious warning.
        with errstate(all='raise'):
            try:
                self._run_machar_highprec()
            except FloatingPointError as e:
                msg = "Caught %s exception, should not have been raised." % e
                raise AssertionError(msg)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
