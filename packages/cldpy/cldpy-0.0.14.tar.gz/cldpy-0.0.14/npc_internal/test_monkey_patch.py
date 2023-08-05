import multiprocessing
import sys
import importlib
import inspect

from npc_internal import monkey_patch
from npc_internal.monkey_patch import MonkeyPatch

from npc_internal.server.server import CloudArrayServer

import numpy_cloud
import numpy


class TestMonkeyPatch(object):

    def get_module_names(self, target_name):
        names = []
        for name in sys.modules.keys():
            if name == target_name or name.startswith(target_name + '.'):
                names.append(name)
        return names

    def test_counts_match(self):
        npc_modules = self.get_module_names('numpy_cloud')
        np_modules = self.get_module_names('numpy')
        npc_modules = [x.replace('numpy_cloud', '') for x in npc_modules]
        np_modules = [x.replace('numpy', '') for x in np_modules]
        assert np_modules == npc_modules

        for name in sys.modules.keys():
            if name.startswith('numpy.'):
                npc_name = name.replace('numpy', 'numpy_cloud')
                assert npc_name in sys.modules

            if name.startswith('numpy_cloud.'):
                np_name = name.replace('numpy_cloud', 'numpy')
                assert np_name in sys.modules

    def test_dirs_match(self):
        npc_extras = set(['_id', '_server_url'])
        for name, module in sys.modules.items():
            if name.startswith('numpy_cloud'):
                np_name = name.replace('numpy_cloud', 'numpy')

                npc_dir = set(dir(module)) - npc_extras
                try:
                    np_module = sys.modules[np_name]
                except KeyError:
                    np_module = eval(np_name)
                np_dir = set(dir(np_module))

                for x in np_dir:
                    if x not in npc_dir:
                        print('not found', x)

                assert set(np_dir) == set(npc_dir)

    def test_dupes(self):
        assert (
            numpy_cloud._mat is
            sys.modules['numpy_cloud.matrixlib'])
        assert (
            numpy_cloud.polynomial.laguerre.la is
            sys.modules['numpy_cloud.linalg'])

    def test_classes(self):
        assert inspect.isclass(numpy_cloud.flatiter)
        assert set(numpy.flatiter.__dict__.keys()).issubset(set(numpy_cloud.flatiter.__dict__.keys()))
        assert numpy_cloud.ndarray.__base__ is numpy.ndarray
