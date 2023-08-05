import sys
import threading
import multiprocessing

from types import ModuleType

from npc_internal.server.server import CloudArrayServer
from npc_internal.util import get_fullname


server = CloudArrayServer('localhost', 9090)
s = multiprocessing.Process(target=server.serve, daemon=True)
print('starting server')
s.start()
print('done')

import numpy_cloud as npc
# npc.drop_in()

def swap_modules(test_module):
    print('swap modules in', test_module)
    for field_name in dir(test_module):
        field = getattr(test_module, field_name)
        print('-', field, type(field))
        if type(field) is ModuleType:
            # fullname = get_fullname(field.__class__)
            # print('->', field_name)
            # if field_name == 'np':
            #     import pdb ; pdb.set_trace()
            name = field.__name__
            if name == 'numpy' or name.startswith('numpy.'):
                new_name = name.replace('numpy', 'numpy_cloud')
                print('swap %s, %s' % (name, new_name))
                setattr(test_module, field_name, sys.modules[new_name])


import numpy.core.tests.test_multiarray
swap_modules(numpy.core.tests.test_multiarray)
import pdb ; pdb.set_trace()
from numpy.core.tests.test_multiarray import TestStats
