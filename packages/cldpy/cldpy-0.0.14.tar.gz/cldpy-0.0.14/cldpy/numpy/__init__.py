import sys

# This import should occur before cloud version
import numpy

from xmlrpc.client import ServerProxy

from npc_internal.proxy_objects import get_proxy_id
from npc_internal.protocol import Request, Response
from npc_internal.monkey_patch import monkey_patch
from npc_internal.config import SERVER_URL
from npc_internal.logger import logger


class NDArrayProxy(object):

    def pull(self):
        req = Request(get_proxy_id(self), '', '', [], {})
        with ServerProxy(SERVER_URL, allow_none=True) as server:
            resp = Response.deserialize(server.pull(req.serialize()))
        return resp.value


np_proxy_classes = {
    'numpy.ndarray': {'class': NDArrayProxy, 'base_is_superclass': True},
    'numpy.flatiter': {},
    'numpy.nditer': {},
    'numpy.flagsobj': {},
}

monkey_patch('numpy', 'cldpy.numpy', SERVER_URL, np_proxy_classes)
del sys.modules['cldpy.numpy']
__import__('cldpy.numpy')
