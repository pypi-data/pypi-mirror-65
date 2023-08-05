from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import re

import numpy_cloud as np
from numpy.testing import assert_


def test_valid_numpy_version():
    # Verify that the numpy version is a valid one (no .post suffix or other
    # nonsense).  See gh-6431 for an issue caused by an invalid version.
    version_pattern = r"^[0-9]+\.[0-9]+\.[0-9]+(|a[0-9]|b[0-9]|rc[0-9])"
    dev_suffix = r"(\.dev0\+([0-9a-f]{7}|Unknown))"
    if np.version.release:
        res = re.match(version_pattern, np.__version__)
    else:
        res = re.match(version_pattern + dev_suffix, np.__version__)

    assert_(res is not None, np.__version__)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
