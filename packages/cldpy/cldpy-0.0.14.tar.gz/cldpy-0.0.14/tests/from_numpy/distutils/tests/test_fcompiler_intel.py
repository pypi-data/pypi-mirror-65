from __future__ import division, absolute_import, print_function


# -- snippet for numpy_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()
# -- end numpy_cloud snippet -- #

import numpy_cloud.distutils.fcompiler
from numpy.testing import assert_


intel_32bit_version_strings = [
    ("Intel(R) Fortran Intel(R) 32-bit Compiler Professional for applications"
     "running on Intel(R) 32, Version 11.1", '11.1'),
]

intel_64bit_version_strings = [
    ("Intel(R) Fortran IA-64 Compiler Professional for applications"
     "running on IA-64, Version 11.0", '11.0'),
    ("Intel(R) Fortran Intel(R) 64 Compiler Professional for applications"
     "running on Intel(R) 64, Version 11.1", '11.1')
]

class TestIntelFCompilerVersions(CloudArrayTest):
    def test_32bit_version(self):
        fc = numpy.distutils.fcompiler.new_fcompiler(compiler='intel')
        for vs, version in intel_32bit_version_strings:
            v = fc.version_match(vs)
            assert_(v == version)


class TestIntelEM64TFCompilerVersions(CloudArrayTest):
    def test_64bit_version(self):
        fc = numpy.distutils.fcompiler.new_fcompiler(compiler='intelem')
        for vs, version in intel_64bit_version_strings:
            v = fc.version_match(vs)
            assert_(v == version)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
