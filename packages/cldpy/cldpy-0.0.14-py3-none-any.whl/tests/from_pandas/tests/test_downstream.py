

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
# -*- coding: utf-8 -*-
"""
Testing that we work in the downstream packages
"""
import subprocess
import sys

import pytest
import numpy_cloud as np  # noqa
from pandas_cloud import DataFrame
from pandas_cloud.compat import PY36
from pandas_cloud.util import testing as tm
import importlib


def import_module(name):
    # we *only* want to skip if the module is truly not available
    # and NOT just an actual import error because of pandas changes

    if PY36:
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError:  # noqa
            pytest.skip("skipping as {} not available".format(name))

    else:
        try:
            return importlib.import_module(name)
        except ImportError as e:
            if "No module named" in str(e) and name in str(e):
                pytest.skip("skipping as {} not available".format(name))
            raise


@pytest.fixture
def df():
    return DataFrame({'A': [1, 2, 3]})


def test_dask(df):

    toolz = import_module('toolz')  # noqa
    dask = import_module('dask')  # noqa

    import dask.dataframe as dd

    ddf = dd.from_pandas(df, npartitions=3)
    assert ddf.A is not None
    assert ddf.compute() is not None


def test_xarray(df):

    xarray = import_module('xarray')  # noqa

    assert df.to_xarray() is not None


def test_oo_optimizable():
    # GH 21071
    subprocess.check_call([sys.executable, "-OO", "-c", "import pandas_cloud"])


@tm.network
# Cython import warning
@pytest.mark.filterwarnings("ignore:can't:ImportWarning")
def test_statsmodels():

    statsmodels = import_module('statsmodels')  # noqa
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    df = sm.datasets.get_rdataset("Guerry", "HistData").data
    smf.ols('Lottery ~ Literacy + np.log(Pop1831)', data=df).fit()


# Cython import warning
@pytest.mark.filterwarnings("ignore:can't:ImportWarning")
def test_scikit_learn(df):

    sklearn = import_module('sklearn')  # noqa
    from sklearn import svm, datasets

    digits = datasets.load_digits()
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(digits.data[:-1], digits.target[:-1])
    clf.predict(digits.data[-1:])


# Cython import warning and traitlets
@tm.network
@pytest.mark.filterwarnings("ignore")
def test_seaborn():

    seaborn = import_module('seaborn')
    tips = seaborn.load_dataset("tips")
    seaborn.stripplot(x="day", y="total_bill", data=tips)


def test_pandas_gbq(df):

    pandas_gbq = import_module('pandas_gbq')  # noqa


@pytest.mark.xfail(reason="0.7.0 pending", strict=True)
@tm.network
def test_pandas_datareader():

    pandas_datareader = import_module('pandas_datareader')  # noqa
    pandas_datareader.DataReader(
        'F', 'quandl', '2017-01-01', '2017-02-01')


# importing from pandas_cloud, Cython import warning
@pytest.mark.filterwarnings("ignore:The 'warn':DeprecationWarning")
@pytest.mark.filterwarnings("ignore:pandas.util:DeprecationWarning")
@pytest.mark.filterwarnings("ignore:can't resolve:ImportWarning")
def test_geopandas():

    geopandas = import_module('geopandas')  # noqa
    fp = geopandas.datasets.get_path('naturalearth_lowres')
    assert geopandas.read_file(fp) is not None


# Cython import warning
@pytest.mark.filterwarnings("ignore:can't resolve:ImportWarning")
def test_pyarrow(df):

    pyarrow = import_module('pyarrow')  # noqa
    table = pyarrow.Table.from_pandas(df)
    result = table.to_pandas()
    tm.assert_frame_equal(result, df)

HAS_REFCOUNT = False  # No refcount tests for numpy_cloud
