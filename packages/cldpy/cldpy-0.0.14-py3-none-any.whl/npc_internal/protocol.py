import base64
import cloudpickle as pickle
import inspect
import json
import uuid

from npc_internal.logger import logger
from npc_internal.proxy_objects import get_proxy_id, is_proxy
from npc_internal.util import get_fullname


class Request(object):

    def __init__(self, proxy_id, field_name, call_as, args, kwargs, meta=None):
        # TODO: put everything in "meta"
        self.proxy_id = proxy_id
        self.field_name = field_name
        self.call_as = call_as
        self.args = args
        self.kwargs = kwargs
        if meta is None:
            meta = {}
        self.meta = meta

    def __str__(self):
        return '<Request: %s, %s, %s>' % (self.proxy_id, self.field_name, self.call_as)

    @staticmethod
    def deserialize(serialized, lib):
        logger.debug('Deserializing request: %s', serialized)
        d = json.loads(serialized)
        args, kwargs = deserialize_args(d['ser_args'], lib)
        if d.get('proxy_id'):
            proxy_id = ProxyId.deserialize(d['proxy_id'])
        else:
            proxy_id = None
        return Request(
            proxy_id,
            d['field_name'],
            d['call_as'],
            args,
            kwargs,
            deserialize(d['meta']))

    def serialize(self):
        logger.debug('Serializing request: %s', self)
        ser_args = serialize_args(self.args, self.kwargs)
        if self.proxy_id:
            proxy_id_ser = self.proxy_id.serialize()
        else:
            proxy_id_ser = None
        m = serialize(self.meta)
        d = {
            'ser_args': ser_args,
            'proxy_id': proxy_id_ser,
            'field_name': self.field_name,
            'call_as': self.call_as,
            'meta': m,
        }
        return json.dumps(d)


class Response(object):

    def __init__(self, value, should_proxy, lib):
        if type(value) == tuple:
            # TODO: special casing 'tuple' types here. This won't
            # work for lists or dict's, or other collection return
            # types. If it turns out those need to be handled also,
            # the logic here should be generalized.
            self.type = 'tuple'
            r = []
            for item in value:
                if get_fullname(type(item)) in should_proxy:
                    item = lib.store(item)
                r.append(item)
            self.values = tuple(r)
            self.value = None
            self.proxy_id = None
        elif get_fullname(type(value)) in should_proxy:
            self.type = 'proxy'
            self.value = None
            self.proxy_id = lib.store(value)
            logger.debug('Making proxy response: %s' % (self))
        else:
            self.type = 'value'
            self.value = value
            self.proxy_id = None
            logger.debug('Making value response: %s' % (self))

    def __str__(self):
        return '<Response: %s, %s, %s>' % (self.type, self.value, self.proxy_id)

    @staticmethod
    def deserialize(serialized):
        return deserialize(serialized)

    def serialize(self):
        return serialize(self)

    def unpack(self, factory):
        if self.type == 'tuple':
            r = []
            for item in self.values:
                if isinstance(item, ProxyId):
                    item = factory.create_object(item)
                r.append(item)
            return tuple(r)
        elif self.type == 'proxy':
            return factory.create_object(self.proxy_id)
        elif self.type == 'value':
            if isinstance(self.value, Exception):
                if 'invalid type' in str(self.value):
                    import pdb ; pdb.set_trace()
                raise self.value
            else:
                return self.value
        else:
            raise Exception('unexpected type: %s' % self.type)


class ProxyId(object):

    def __init__(self, pxid, path=None, can_import=False, classname=None):
        if ':' in pxid:
            raise Exception('cannot have ":" in pxid')
        self.pxid = pxid
        self.path = path
        self.can_import = can_import
        self.classname = classname

    @staticmethod
    def random_id(path=None, can_import=False, classname=None):
        return ProxyId(str(uuid.uuid4()), path, can_import, classname)

    @staticmethod
    def deserialize(s):
        data = json.loads(s)
        return ProxyId(
            data.get('pxid'), data.get('path'), data.get('can_import'),
            data.get('classname'))

    def __str__(self):
        return self.pretty()

    def pretty(self):
        if self.path:
            s = '%s:%s' % (self.pxid, self.path)
        else:
            s = self.pxid
        if self.can_import:
            s += ':can_import'
        if self.classname:
            s += '[' + self.classname + ']'
        return s

    def serialize(self):
        return json.dumps({
            'pxid': self.pxid,
            'path': self.path,
            'can_import': self.can_import,
            'classname': self.classname,
        })

    def for_child(self, path):
        if self.path:
            prefix = self.path + '.'
        else:
            prefix = ''
        return ProxyId(self.pxid, prefix + path, self.can_import, self.classname)

    def get_target(self, lib):
        return lib.get(self)


class ClassStandIn(object):
    def __init__(self, clazz):
        self.module_name = clazz.__module__
        self.name = clazz.__name__

    @staticmethod
    def decode(obj):
        module = __import__(obj.module_name)
        return getattr(module, obj.name)


def serialize(value):
    return base64.b64encode(pickle.dumps(value)).decode(encoding='utf-8')


def deserialize(ser):
    s = str(ser)
    b = base64.b64decode(s)
    return pickle.loads(b)


def serialize_list(args):
    args_cp = []
    for arg in args:
        if isinstance(arg, list):
            args_cp.append(serialize_list(arg))
        elif isinstance(arg, dict):
            args_cp.append(serialize_dict(arg))
        elif (inspect.isclass(arg) and hasattr(arg, '_proxy_base_class')):
            # TODO: we may want to have different behavior for this depending on
            # if serialization is happening on client side or server side
            args_cp.append(ClassStandIn(arg._proxy_base_class))
        elif is_proxy(arg):
            args_cp.append(get_proxy_id(arg))
        else:
            args_cp.append(arg)
    return args_cp


def serialize_dict(kwargs):
    kwargs_cp = {}
    for key, val in kwargs.items():
        if is_proxy(val):
            kwargs_cp[key] = get_proxy_id(val)
        elif isinstance(val, list):
            kwargs_cp[key] = serialize_list(val)
        elif isinstance(val, dict):
            kwargs_cp[key] = serialize_dict(val)
        else:
            # print('  sending value')
            kwargs_cp[key] = val
    return kwargs_cp


def deserialize_list(args_ser, lib):
    args = []
    for arg in args_ser:
        if isinstance(arg, list):
            args.append(deserialize_list(arg, lib))
        elif isinstance(arg, dict):
            args.append(deserialize_dict(arg, lib))
        elif is_proxy(arg):
            args.append(lib.get(get_proxy_id(arg)))
        elif isinstance(arg, ProxyId):
            logger.debug('Deserialize proxy ID: %s' % arg)
            args.append(arg.get_target(lib))
        elif isinstance(arg, ClassStandIn):
            args.append(ClassStandIn.decode(arg))
        else:
            args.append(arg)

    return args


def deserialize_dict(kwargs_ser, lib):
    kwargs = {}
    for key, val in kwargs_ser.items():
        if isinstance(val, ProxyId):
            kwargs[key] = val.get_target(lib)
        elif isinstance(val, ClassStandIn):
            kwargs[key] = ClassStandIn.decode(val)
        elif isinstance(val, list):
            kwargs[key] = deserialize_list(val, lib)
        elif isinstance(val, dict):
            kwargs[key] = deserialize_dict(val, lib)
        elif is_proxy(val):
            kwargs[key] = lib.get(get_proxy_id(val))
        else:
            kwargs[key] = val
    return kwargs


def serialize_args(args, kwargs):
    args_cp = []
    if args:
        args_cp = serialize_list(args)
    kwargs_cp = {}
    if kwargs:
        kwargs_cp = serialize_dict(kwargs)
    args_data = {
        'args': args_cp,
        'kwargs': kwargs_cp,
    }

    # print('pickling args data:')
    # print(args_data)

    b = pickle.dumps(args_data)
    s = base64.b32encode(b).decode(encoding='utf-8')
    return s


def deserialize_args(ser_args_data, lib):
    s = ser_args_data
    b = base64.b32decode(s)
    args_data = pickle.loads(b)
    args = deserialize_list(args_data.get('args', []), lib)
    kwargs = deserialize_dict(args_data.get('kwargs', {}), lib)
    return args, kwargs
