import multiprocessing
import threading

import pandas

from unittest import mock

from npc_internal.server.server import CloudArrayServer


_server = None
_server_thread = None


def start_if_not_running():
    global _server
    global _server_thread
    if _server is not None:
        stop_if_running()
        # raise Exception('server already running')
    _server = CloudArrayServer('localhost', 9090)
    _server_thread = threading.Thread(target=_server.serve)
    _server_thread.start()


def stop_if_running():
    global _server
    global _server_thread
    if _server is None:
        return
        # raise Exception('no server running')
    _server.force_stop()
    _server_thread.join()
    _server = None
    _server_thread = None
    


class CloudArrayTest(object):

    @classmethod
    def setup_class(cls):
        cls.patch_check_isinstance = mock.patch('pandas.util.testing._check_isinstance')
        cls.check_isinstance = cls.patch_check_isinstance.start()
        cls.check_isinstance.return_value = True

        for base in cls.__bases__:
            if base == CloudArrayTest:
                continue
            if not hasattr(base, 'setup_class'):
                continue
            base.setup_class(cls)

    @classmethod
    def teardown_class(cls):
        cls.patch_check_isinstance.stop()

        for base in cls.__bases__:
            if base == CloudArrayTest:
                continue
            if not hasattr(base, 'teardown_class'):
                continue
            base.teardown_class(cls)

    def setup_method(self, method):
        self.server = CloudArrayServer('localhost', 9090)
        self.t = threading.Thread(target=self.server.serve)
        self.t.start()

        for base in self.__class__.__bases__:
            if base == CloudArrayTest:
                continue
            if not hasattr(base, 'setup_method'):
                continue
            base.setup_method(self, method)

    def teardown_method(self, method):
        self.server.force_stop()
        self.t.join()

        for base in self.__class__.__bases__:
            if base == CloudArrayTest:
                continue
            if not hasattr(base, 'teardown_method'):
                continue
            base.teardown_method(self, method)
