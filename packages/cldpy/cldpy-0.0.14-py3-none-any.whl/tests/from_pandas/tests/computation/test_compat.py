

# -- snippet for {numpy|pandas}_cloud testing -- #
from test_util.util import CloudArrayTest
from test_util.util import start_if_not_running, stop_if_running

def setup_function(function):
    start_if_not_running()

def teardown_function(function):
    stop_if_running()

# TODO: use mock.patch() instead of the code below
from pandas.util import testing
def setup_module():
    global old_assert_series_equal
    old_assert_series_equal = testing.assert_series_equal
    def assert_series_equal(*args, **kwargs):
        kwargs['check_series_type'] = False
        return old_assert_series_equal(*args, **kwargs)
    testing.assert_series_equal = assert_series_equal

def teardown_module():
    global old_assert_series_equal
    testing.assert_series_equal = old_assert_series_equal

# -- end {numpy|pandas}_cloud snippet -- #
import pytest
from distutils.version import LooseVersion

import pandas_cloud as pd

from pandas_cloud.core.computation.engines import _engines
import pandas_cloud.core.computation.expr as expr
from pandas_cloud.core.computation.check import _MIN_NUMEXPR_VERSION


def test_compat():
    # test we have compat with our version of nu

    from pandas_cloud.core.computation.check import _NUMEXPR_INSTALLED
    try:
        import numexpr as ne
        ver = ne.__version__
        if LooseVersion(ver) < LooseVersion(_MIN_NUMEXPR_VERSION):
            assert not _NUMEXPR_INSTALLED
        else:
            assert _NUMEXPR_INSTALLED
    except ImportError:
        pytest.skip("not testing numexpr version compat")


@pytest.mark.parametrize('engine', _engines)
@pytest.mark.parametrize('parser', expr._parsers)
def test_invalid_numexpr_version(engine, parser):
    def testit():
        a, b = 1, 2  # noqa
        res = pd.eval('a + b', engine=engine, parser=parser)
        assert res == 3

    if engine == 'numexpr':
        try:
            import numexpr as ne
        except ImportError:
            pytest.skip("no numexpr")
        else:
            if (LooseVersion(ne.__version__) <
                    LooseVersion(_MIN_NUMEXPR_VERSION)):
                with pytest.raises(ImportError):
                    testit()
            else:
                testit()
    else:
        testit()

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
