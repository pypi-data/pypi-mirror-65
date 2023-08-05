import threading
import unittest
import pytest

import numpy_cloud as npc
import numpy as np

from npc_internal.server.server import CloudArrayServer
from npc_internal import protocol


class TestCloudArray(unittest.TestCase):

    def setUp(self):
        self.server = CloudArrayServer('localhost', 9090)
        self.t = threading.Thread(target=self.server.serve)
        print('starting server')
        self.t.start()

        self.modules = [np, npc]

    def tearDown(self):
        self.server.force_stop()
        self.t.join()

    def assertAllSame(self, results):
        # print('checking if all these are the same:', results)
        r = results[0]
        for r2 in results[1:]:
            self.assertEqual(r, r2)

    def assertAllSameArrays(self, results):
        self.assertTrue(len(results) == 2)  # This should be true in all cases
        self.assertTrue(np.array_equal(results[0], results[1].pull()))

    def test_pi(self):
        assert np.pi == npc.pi

    def test_constructor(self):
        l = 10
        arrs = []
        means = []
        for np_module in self.modules:
            arr = np_module.ndarray((l,))
            for i in range(l):
                arr[i] = 2 * i
            arrs.append(arr)
            means.append(arr.mean())
        self.assertAllSame(means)
        self.assertAllSameArrays(arrs)

    def test_flat(self):
        arr = npc.arange(15)
        f = arr.flat
        vals = [val for val in f]
        out = ','.join([str(val) for val in vals])
        self.assertEqual('0,1,2,3,4,5,6,7,8,9,10,11,12,13,14', out)

    @pytest.mark.skip(reason='TODO')
    def test_resize(self):
        d = np.ones(100)
        old = sys.getsizeof(d)
        d.resize(50)
        assert_(old > sys.getsizeof(d))
        d.resize(150)
        assert_(old < sys.getsizeof(d))

    @pytest.mark.skip(reason='TODO')
    def test_serialize_ndarray_proxy_class(self):
        from numpy_cloud.testing import assert_equal
        arr = npc.ndarray((10,))
        assert_equal(npc.ndarray, type(arr))

    @pytest.mark.skip(reason='TODO')
    def test_serialize_array_like_class(self):
        # Similar failure occurs in test_indexing.py
        class ArrayLike(object):
            def __array__(self):
                return npc.array(0)

        protocol.serialize_args([ArrayLike()], {})

    def test_mean(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.mean())
        self.assertAllSame(result)

    def test_out(self):
        arr = npc.arange(10).reshape(2,5)
        # out1 = arr.mean(axis=1)
        out2 = npc.zeros(2)
        arr.mean(axis=1, out=out2)
        print(out2)

    def test_mean_axis(self):
        result = []
        for np_module in self.modules:
            print('==== test mean axis %s ====' % np_module)
            arr = np_module.arange(15).reshape(5, 3)
            v = arr.mean(axis=1)
            print('---- got a response ----')
            result.append(v)
        self.assertAllSameArrays(result)

    def test_median(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            print('got arr, now lets call median')
            result.append(np_module.median(arr))
        self.assertAllSame(result)

    def test_min(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.min())
        self.assertAllSame(result)

    def test_max(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.max())
        self.assertAllSame(result)

    def test_arange(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(2, 15, 2, dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_reshape(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            print('arange done')
            arr = arr.reshape(5, 3)
            print('reshape done')
            print('arr', arr)
            result.append(arr)
        self.assertAllSameArrays(result)

    def test_zeros(self):
        result = []
        for np_module in self.modules:
            arr = np_module.zeros((10, 10), dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_ones(self):
        result = []
        for np_module in self.modules:
            arr = np_module.ones((10, 10), dtype=np.uint8)
            mean = arr.mean()
            result.append(mean)
        self.assertAllSame(result)

    def test_add(self):
        result = []
        for np_module in self.modules:
            arr1 = np_module.arange(15)
            arr2 = np_module.arange(15)
            arr_sum = arr1 + arr2
            result.append(arr_sum.mean())
        self.assertAllSame(result)

    def test_rshift(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            arr = arr << 3
            result.append(arr.mean())
        self.assertAllSame(result)

    def test_all(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.all())
        self.assertAllSame(result)

    def test_any(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.any())
        self.assertAllSame(result)

    def test_argmax(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15).reshape(3, 5)
            am = arr.argmax(axis=1)
            print('AM', am)
            result.append(am)
        self.assertAllSameArrays(result)

    def test_argmin(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.argmin())
        self.assertAllSame(result)

    def test_argpartition(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            result.append(arr.argpartition(3))
        self.assertAllSameArrays(result)

    def test_dot(self):
        result = []
        for np_module in self.modules:
            arr1 = np_module.arange(15)
            arr2 = np_module.arange(15) * 2
            result.append(np_module.dot(arr1, arr2))
        self.assertAllSame(result)

    def test_linalg_multi_dot(self):
        result = []
        for np_module in [npc]:
            arr1 = np_module.arange(15)
            arr2 = np_module.arange(15) * 2
            result.append(np_module.linalg.multi_dot([arr1, arr2]))
        self.assertAllSame(result)

    def test_submodule_import(self):
        result = []
        from numpy_cloud.linalg import multi_dot
        arr1 = npc.arange(15)
        arr2 = npc.arange(15) * 2
        result = multi_dot([arr1, arr2])
        self.assertEqual(2030, result)

    def test_to_string(self):
        result = []
        arr = npc.arange(15)
        arr = arr.reshape(3, 5)
        print(arr)
        local_arr = np.asarray(arr)
        print(local_arr)

    @pytest.mark.filterwarnings('ignore:UPDATEIFCOPY deprecated, use WRITEBACKIFCOPY instead')
    def test_flags(self):
        attrs = [
            'C_CONTIGUOUS',
            'F_CONTIGUOUS',
            'OWNDATA',
            'WRITEABLE',
            'ALIGNED',
            'WRITEBACKIFCOPY',
            'UPDATEIFCOPY',
        ]

        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            f = arr.flags
            vals = []
            for attr in attrs:
                print('attr', attr)
                vals.append(f[attr])
            result.append(','.join([str(v) for v in vals]))
        self.assertAllSame(result)

    @pytest.mark.skip(reason='TODO')
    def test_flags_str(self):
        result = []
        for np_module in self.modules:
            arr = np_module.arange(15)
            f = arr.flags
            result.append(str(f))
        self.assertAllSame(result)
