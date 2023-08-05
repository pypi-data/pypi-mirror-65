import threading
import unittest
import pytest

import pandas_cloud as pdc
import numpy_cloud as npc
import pandas as pd
import numpy as np

from unittest import mock

from pandas.util.testing import assert_frame_equal

from pandas_cloud.compat import range, lrange, StringIO, OrderedDict, signature

from npc_internal.server.server import CloudArrayServer
from npc_internal.proxy_objects import get_proxy_id
from npc_internal.logger import logger


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


class TestCloudDataFrame(object):

    @classmethod
    def setup_class(cls):
        cls.patch_check_isinstance = mock.patch('pandas.util.testing._check_isinstance')
        cls.check_isinstance = cls.patch_check_isinstance.start()
        cls.check_isinstance.return_value = True

        # TODO: figure out why mock.patch() below is not working
        # def new_assert_series_equal(*args, **kwargs):
        #     raise Exception()
        #     kwargs['check_series_type'] = False
        #     return old_assert_series_equal(*args, **kwargs)
        # cls.patch_assert_series_equal = mock.patch('pandas.util.testing.assert_series_equal')
        # cls.patch_assert_series_equal.side_effect = new_assert_series_equal
        # cls.assert_series_equal = cls.patch_assert_series_equal.start()

    @classmethod
    def teardown_class(cls):
        cls.patch_check_isinstance.stop()
        # cls.patch_assert_series_equal.stop()

    def setup_method(self, method):
        self.server = CloudArrayServer('localhost', 9090)
        self.t = threading.Thread(target=self.server.serve)
        print('starting server')
        self.t.start()

    def teardown_method(self, method):
        self.server.force_stop()
        self.t.join()

    def test_iloc_name(self):
        records = [
            (1, 'one'),
            (2, 'two'),
        ]
        df = pd.DataFrame.from_records(records)
        dfc = pdc.DataFrame.from_records(records)
        iloc = df.iloc[:, 0]
        ilocc = dfc.iloc[:, 0]
        name = iloc.name
        namec = ilocc.name
        assert name == namec

    def test_make_dataframe_from_records(self):
        records = [
            (1, 'one'),
            (2, 'two'),
        ]
        df = pd.DataFrame.from_records(records)
        dfc = pdc.DataFrame.from_records(records)
        print('PXID %s' % (get_proxy_id(dfc)))
        assert str(df) == str(dfc)
        assert isinstance(dfc, pd.DataFrame)
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_make_dataframe_from_file(self):
        filename = 'sample_data/tips.csv'
        df = pd.read_csv(filename).head(10)
        dfc = pdc.read_csv(filename).head(10)
        print('PXID %s' % (get_proxy_id(dfc)))
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_columns_head(self):
        filename = 'sample_data/tips.csv'
        df = pd.read_csv(filename)[['total_bill', 'tip']].head(10)
        dfc = pdc.read_csv(filename)[['total_bill', 'tip']].head(10)
        print('PXID %s' % (get_proxy_id(dfc)))
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_filter(self):
        filename = 'sample_data/tips.csv'
        df = pd.read_csv(filename)
        df = df[df['time'] == 'Dinner'].head(10)
        dfc = pdc.read_csv(filename)
        dfc = dfc[dfc['time'] == 'Dinner'].head(10)
        print('PXID %s' % (get_proxy_id(dfc)))
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_isna(self):
        data = {'col1': ['A', 'B', np.NaN, 'C', 'D'], 'col2': ['F', np.NaN, 'G', 'H', 'I']}
        df = pd.DataFrame(data)
        df = df[df['col2'].isna()]
        dfc = pdc.DataFrame(data)
        dfc = dfc[dfc['col2'].isna()]
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_groupby_count(self):
        filename = 'sample_data/tips.csv'
        df = pd.read_csv(filename).groupby('sex').count()
        dfc = pdc.read_csv(filename).groupby('sex').count()
        print('PXID %s' % (get_proxy_id(dfc)))
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_groupby_agg(self):
        filename = 'sample_data/tips.csv'

        df = pd.read_csv(filename).agg({'tip': np.mean, 'day': np.size})
        dfc = pdc.read_csv(filename).agg({'tip': np.mean, 'day': np.size})
        assert_frame_equal(df, dfc, check_frame_type=False)

        df = pd.read_csv(filename).groupby('sex').agg({'tip': np.mean, 'day': np.size})
        dfc = pdc.read_csv(filename).groupby('sex').agg({'tip': np.mean, 'day': np.size})
        assert_frame_equal(df, dfc, check_frame_type=False)

        df = pd.read_csv(filename).groupby('sex').agg({'tip': [np.size, np.mean]})
        dfc = pdc.read_csv(filename).groupby('sex').agg({'tip': [np.size, np.mean]})
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_join(self):
        df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': np.arange(4)})
        df2 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': np.arange(4)})
        df = pd.merge(df1, df2, on='key')

        dfc1 = pdc.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': np.arange(4)})
        dfc2 = pdc.DataFrame({'key': ['A', 'B', 'C', 'D'], 'value': np.arange(4)})
        dfc = pdc.merge(dfc1, dfc2, on='key')
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_outer_join(self):
        df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D', 'E'], 'value': np.arange(5)})
        df2 = pd.DataFrame({'key': ['A', 'B', 'C', 'D', 'F'], 'value': np.arange(5)})
        df = pd.merge(df1, df2, on='key', how='outer')

        dfc1 = pdc.DataFrame({'key': ['A', 'B', 'C', 'D', 'E'], 'value': np.arange(5)})
        dfc2 = pdc.DataFrame({'key': ['A', 'B', 'C', 'D', 'F'], 'value': np.arange(5)})
        dfc = pdc.merge(dfc1, dfc2, on='key', how='outer')
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_concat(self):
        df1 = pd.DataFrame({'city': ['Chicago', 'San Francisco', 'New York City'], 'rank': range(1, 4)})
        df2 = pd.DataFrame({'city': ['Chicago', 'Boston', 'Los Angeles'], 'rank': [1, 4, 5]})
        df = pd.concat([df1, df2])
        dfc1 = pd.DataFrame({'city': ['Chicago', 'San Francisco', 'New York City'], 'rank': range(1, 4)})
        dfc2 = pd.DataFrame({'city': ['Chicago', 'Boston', 'Los Angeles'], 'rank': [1, 4, 5]})
        dfc = pd.concat([dfc1, dfc2])
        assert_frame_equal(df, dfc, check_frame_type=False)

        df = pd.concat([df1, df2]).drop_duplicates()
        dfc = pd.concat([dfc1, dfc2]).drop_duplicates()
        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_modify(self):
        filename = 'sample_data/tips.csv'
        df = pd.read_csv(filename).head(10)
        df.loc[df['tip'] < 2, 'tip'] *= 2
        df = df.loc[df['tip'] < 4]

        dfc = pd.read_csv(filename).head(10)
        dfc.loc[dfc['tip'] < 2, 'tip'] *= 2
        dfc = dfc.loc[dfc['tip'] < 4]

        assert_frame_equal(df, dfc, check_frame_type=False)

    def test_instance_method_proxy_id(self):
        records = [(1, 'one'), (2, 'two')]
        df = pd.DataFrame.from_records(records)
        f = df.count
        dfc = pdc.DataFrame.from_records(records)
        fc = dfc.count
        args_signature = pd.compat.signature(f).args
        args_signature_c = pdc.compat.signature(fc).args
        assert args_signature == args_signature_c

    def test_class_method_proxy_id(self):
        f = pd.DataFrame.from_records
        fc = pdc.DataFrame.from_records
        args_signature = pd.compat.signature(f).args
        args_signature_c = pdc.compat.signature(fc).args
        assert args_signature == args_signature_c

    def test_module_function_proxy_id(self):
        f = pd.read_csv
        fc = pdc.read_csv
        args_signature = pd.compat.signature(f).args
        args_signature_c = pdc.compat.signature(fc).args
        assert args_signature == args_signature_c

    @pytest.mark.skip(reason='TODO')
    def test_send_custom_method(self):
        # TODO: Fails beacuse fn cannot be serialized/pickled. Should
        # find a way to make this work.
        records = [(1, 'one'), (2, 'two')]
        df = pd.DataFrame.from_records(records)
        dfc = pdc.DataFrame.from_records(records)

        def fn(x):
            return np.sum(np.asarray(x))

        def fnc(x):
            return npc.sum(npc.asarray(x))

        r = df.apply(fn, axis=0)
        rc = dfc.apply(fnc, axis=0)
        assert r == rc

    def test_from_tutorial_recursive_args_serialization(self):
        df = pd.DataFrame({
            'A': 1.,
            'B': pd.Timestamp('20130102'),
            'C': pd.Series(1, index=list(range(4)), dtype='float32'),
            'D': np.array([3] * 4, dtype='int32'),
            'E': pd.Categorical(['test', 'train', 'test', 'train']),
            'F': 'foo',
        })
        dfc = pdc.DataFrame({
            'A': 1.,
            'B': pdc.Timestamp('20130102'),
            'C': pdc.Series(1, index=list(range(4)), dtype='float32'),
            'D': npc.array([3] * 4, dtype='int32'),
            'E': pdc.Categorical(['test', 'train', 'test', 'train']),
            'F': 'foo',
        })
        # assert str(df.dtypes) == str(dfc.dtypes)

        # print(dfc.index)
