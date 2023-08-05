import inspect
import json
import types

from xmlrpc.client import ServerProxy

from npc_internal.proxy_objects import get_proxy_id, set_proxy_id
from npc_internal.protocol import Request, Response, ProxyId
from npc_internal.logger import logger
from npc_internal.util import get_fullname


# TODO: refactor so this isn't needed? currently used if pandas_cloud and
# numpy_cloud are both used, so that they share proxy classes.
factory_singleton = None

def get_factory_singleton():
    global factory_singleton
    if not factory_singleton:
        factory_singleton = ProxyFactory()
    return factory_singleton


def remote_init(server_url, base_classname, args, kwargs):
    req = Request(None, '', 'init', args, kwargs, {'class': base_classname})
    with ServerProxy(server_url, allow_none=True) as server:
        proxy_id = ProxyId.deserialize(server.init(req.serialize()))
    return proxy_id


class ProxySpec(object):

    def __init__(self, server_url, module_proxy_id, factory):
        self.server_url = server_url
        self.module_proxy_id = module_proxy_id
        self.factory = factory


class ProxyFactory(object):

    def __init__(self):
        self.classes = {}
        self.modules = {}
        self._modules_to_proxy = {}
        self.objects = {}

    def has_class(self, name):
        return name in self.classes

    def add_class(self, name, cls):
        if self.has_class(name):
            raise Exception("won't override %s with %s" % (name, cls))
        self.classes[name] = cls

    def get_class(self, name):
        return self.classes[name]

    def has_module(self, name):
        return name in self.modules

    def add_module(self, name, cls):
        if self.has_module(name):
            raise Exception("won't override %s with %s" % (name, cls))
        self.modules[name] = cls

    def get_module(self, name):
        return self.modules[name]

    def create_object(self, proxy_id):
        # TODO: thread safety
        # TODO: this logic should probably be in proxy_objects module, or vice-versa
        if proxy_id.pretty() in self.objects:
            return self.objects[proxy_id.pretty()]
        cls = self.get_class(proxy_id.classname)
        # TODO: This check is a hack, fix it
        if cls.__name__ == 'NDArrayProxy':
            obj = cls((1,), proxy_id=proxy_id)
        elif cls.__name__ == 'Int64Index_proxy':
            obj = cls([], proxy_id=proxy_id)
        else:
            obj = cls(proxy_id=proxy_id)
        self.objects[proxy_id.pretty()] = obj
        return obj

    def create_module(self, base_module, loader, proxy_fullname, spec):
        if proxy_fullname in self.modules:
            raise Exception('already created module with name %s' % proxy_fullname)

        if base_module in self._modules_to_proxy:
            proxy_module = self._modules_to_proxy[base_module]
            self.modules[proxy_fullname] = proxy_module
            return proxy_module

        super_classes = (types.ModuleType,)
        context = {}
        context['__module__'] = proxy_fullname
        context['__loader__'] = loader
        is_package = base_module.__loader__.is_package(base_module.__name__)
        if is_package:
            context['__package__'] = proxy_fullname
        else:
            context['__package__'] = proxy_fullname.rpartition('.')[0]

        proxy_module_class = type(proxy_fullname, super_classes, context)
        proxy_module = proxy_module_class(proxy_fullname)
        proxy_module.__file__ = 'proxy:%s' % base_module.__name__
        if is_package:
            proxy_module.__path__ = []
        proxy_module._server_url = spec.server_url

        self.modules[proxy_fullname] = proxy_module
        self._modules_to_proxy[base_module] = proxy_module

        return proxy_module

    def populate_module(self, proxy_fullname, class_specs, base_name, target_name, spec):
        proxy_module = self.modules[proxy_fullname]
        base_module = None
        for _base_module, _proxy_module in self._modules_to_proxy.items():
            if proxy_module == _proxy_module:
                base_module = _base_module
        if not base_module:
            raise Exception("didn't find base module for %s, %s" % (
                proxy_module, proxy_fullname))

        # print('proxy_fullname:', proxy_fullname)

        for field_name in dir(base_module):
            # print('-', field_name)

            field = getattr(base_module, field_name)
            full_field_name = proxy_module.__name__ + '.' + field_name

            ok = False
            if type(field) is types.ModuleType:
                # Check if we already made this module with a different name
                proxy_name = field.__name__.replace(base_name, target_name)
                if proxy_name in self.modules:
                    proxy_field = self.modules[proxy_name]
                    ok = True
            # print('ok?', ok)
            if not ok:

                # if proxy_fullname == 'pandas_cloud.core.computation.expr' and field_name == 'Expr':
                #     import pdb ; pdb.set_trace()

                # if inspect.isclass(field):
                #     print('FOUND A CLASS: %s %s' % (proxy_fullname, field_name))

                field_name = full_field_name.rpartition('.')[2]
                if field_name in ['__name__']:
                    proxy_field = full_field_name.rpartition('.')[0]
                    ok = True
                elif field_name in [
                        '__loader__',
                        '__spec__',
                        '__file__',
                        '__path__',
                        '__package__',
                        '__module__',
                        # '__all__',
                ]:
                    proxy_field = None
                    ok =False
                elif inspect.isclass(field) and get_fullname(field) in class_specs:
                    full_classname = get_fullname(field)
                    # print('found a class: %s' % (full_classname))
                    if not self.has_class(full_classname):
                        clazz = create_proxy_class(field, class_specs, spec)
                        self.add_class(full_classname, clazz)
                    proxy_field = self.get_class(full_classname)
                    ok = True
                else:
                    like_method = any([
                        inspect.ismethod(field),
                        inspect.isfunction(field),
                        inspect.ismethoddescriptor(field),
                        inspect.isbuiltin(field)])
                    use_field_name = full_field_name.partition('.')[2]

                    if like_method:
                        call_as = 'method'
                        fn = ProxyFunction(base_module, field_name, spec)
                        # print('FOUND A FUNCTION: %s %s' % (proxy_fullname, field_name))
                    else:
                        # TODO: should probably proxy these as well
                        call_as = 'attr'
                        fn = field

                    proxy_field = fn
                    ok = True
            if ok:
                setattr(proxy_module, field_name, proxy_field)

        return proxy_module


class ProxyAttribute(object):

    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

    def _req(self, obj, remote_method, remote_args):
        # proxy_id = obj._proxy_id
        proxy_id = get_proxy_id(obj)
        req = Request(proxy_id, remote_method, 'method', remote_args, {})
        logger.debug('Sending property request: %s', req)
        with ServerProxy(self.spec.server_url, allow_none=True) as server:
            resp = Response.deserialize(server.proxy(req.serialize()))
        return resp.unpack(self.spec.factory)

    def __get__(self, obj, objtype=None):
        # import pdb ; pdb.set_trace()
        return self._req(obj, '__getattribute__', [self.name])

    def __set__(self, obj, value):
        return self._req(obj, '__setattr__', [self.name, value])

    def __delete__(self, obj):
        return self._req(obj, '__delattr__', [self.name])


class ProxyAttributeGetter(object):

    def __init__(self, spec, local, should_proxy):
        def fn(self, name):
            proxy_id = get_proxy_id(self)
            if name in local or name == '_x':
                logger.debug('Proxy attr getter: return "%s" from local' % name)
                val = object.__getattribute__(self, name)
                # if name in should_proxy and proxy_id and not get_proxy_id(val):
                #     logger.debug('%s has an existing proxy id: %s' % (type(self), proxy_id))
                #     attr_proxy_id = proxy_id.for_child(name)
                #     set_proxy_id(val, attr_proxy_id)
                return val

            proxy_id = get_proxy_id(self)
            req = Request(proxy_id, '__getattribute__', 'method', [name], {})
            logger.debug('Sending attribute getter: %s', req)
            with ServerProxy(spec.server_url, allow_none=True) as server:
                resp = Response.deserialize(server.proxy(req.serialize()))
                logger.debug('Response: %s', resp)
            return resp.unpack(spec.factory)

        self.fn = fn

    def __get__(self, obj, objtype=None):
        return self.fn.__get__(obj, objtype)


class ProxyInstanceMethod(object):

    def __init__(self, name, spec):
        def fn(self, *args, **kwargs):
            # if name == 'apply':
            #     import pdb ; pdb.set_trace()
            proxy_id = get_proxy_id(self)
            req = Request(proxy_id, name, 'method', args, kwargs)
            logger.debug('Sending instance method %s', req)
            with ServerProxy(spec.server_url, allow_none=True) as server:
                resp = Response.deserialize(server.proxy(req.serialize()))
                logger.debug('Got response %s', resp)
            return resp.unpack(spec.factory)

        self.fn = fn
        self.name = name

    def __get__(self, obj, objtype=None):
        logger.debug('__get__ in ProxyInstanceMethod %s', self.name)
        if obj is None:
            return self.fn
        bound_fn = self.fn.__get__(obj, objtype)
        can_assign_proxy_id = bool(get_proxy_id(obj))
        fn_proxy_id = get_proxy_id(bound_fn)
        if can_assign_proxy_id and not fn_proxy_id:
            proxy_id = get_proxy_id(obj)
            set_proxy_id(bound_fn, proxy_id.for_child(self.name))
        return bound_fn


class ProxyStaticMethod(object):

    def __init__(self, base_class, name, spec):
        # Raise an exception for static methods as I wasn't able to find any
        # while testing on 'numpy' and 'pandas'. If a static method comes up
        # in a later module, make sure to test the behavior before using.
        # In particular, test that the set_proxy_id behavior.
        raise Exception('unexpected; test this before using')

        def fn(*args, **kwargs):
            proxy_id = spec.module_proxy_id
            req = Request(proxy_id, name, 'method', args, kwargs)
            logger.debug('Sending static method %s', req)
            with ServerProxy(spec.server_url, allow_none=True) as server:
                resp = Response.deserialize(server.proxy(req.serialize()))
                logger.debug('Got response %s', resp)
            return resp.unpack(spec.factory)

        self.fn = fn
        self.name = name

        fullname = get_fullname(base_class) + '.' + name
        path = fullname.partition('.')[2]
        proxy_id = spec.module_proxy_id.for_child(path)
        set_proxy_id(self.fn, proxy_id)

    def __get__(self, obj, objtype=None):
        return self.fn


class ProxyClassMethod(object):

    def __init__(self, base_class, name, spec):
        def fn(*args, **kwargs):
            logger.debug('executing ProxyClassMethod!!')
            proxy_id = spec.module_proxy_id
            req = Request(proxy_id, name, 'classmethod', args, kwargs)
            logger.debug('Sending class method %s', req)
            with ServerProxy(spec.server_url, allow_none=True) as server:
                resp = Response.deserialize(server.proxy(req.serialize()))
                logger.debug('Got response %s', resp)
            return resp.unpack(spec.factory)

        self.spec = spec
        self.fn = classmethod(fn)
        self.name = name
        self.fullname = get_fullname(base_class) + '.' + name

    def __get__(self, obj, objtype=None):
        bound_fn = self.fn.__get__(obj, objtype)
        path = self.fullname.partition('.')[2]
        proxy_id = self.spec.module_proxy_id.for_child(path)
        set_proxy_id(bound_fn, proxy_id)
        return bound_fn


class ProxyFunction(object):

    def __init__(self, base_module, name, spec):
        fullname = base_module.__name__
        prefix = fullname.partition('.')[2]
        self.spec = spec
        self.name = name
        if prefix:
            path = prefix + '.' + name
        else:
            path = name
        self.proxy_id = self.spec.module_proxy_id.for_child(path)
        set_proxy_id(self, self.proxy_id)

    def __call__(self, *args, **kwargs):
        req = Request(self.proxy_id, None, 'method', args, kwargs)
        logger.debug('Sending method %s', req)
        with ServerProxy(self.spec.server_url, allow_none=True) as server:
            resp = Response.deserialize(server.proxy(req.serialize()))
            logger.debug('Got response %s', resp)
        return resp.unpack(self.spec.factory)


class ProxyClassMeta(type):
    def __new__(cls, name, parents, dct):
        return super(ProxyClassMeta, cls).__new__(cls, name, parents, dct)

    def __call__(cls, *args, **kwargs):
        logger.debug('ProxyClassMeta making new class %s with: %s and %s' % (
            cls.__name__, args, kwargs))
        server_url = cls._proxy_server_url
        if 'proxy_id' in kwargs:
            proxy_id = kwargs['proxy_id']
            del kwargs['proxy_id']
        else:
            name = get_fullname(cls._proxy_base_class)
            proxy_id = remote_init(server_url, name, args, kwargs)

        obj = cls.__new__(cls, *args, **kwargs)
        obj.__init__(*args, **kwargs)
        set_proxy_id(obj, proxy_id)

        return obj


class ProxyEmpty(object):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(*args, **kwargs):
        pass


def create_proxy_class(base_class, class_specs, spec):
    name = get_fullname(base_class)
    if spec.factory.has_class(name):
        raise Exception('already have proxy for %s' % base_class)

    class_spec = class_specs[name]
    if class_spec.get('class'):
        clazz = class_spec['class']
        classname = clazz.__name__
        context = dict(clazz.__dict__)
    else:
        classname = '%s_proxy' % base_class.__name__
        context = {}

    if class_spec.get('base_is_superclass'):
        super_classes = (base_class,)
    else:
        super_classes = (ProxyEmpty,)

    clazz = clazz = ProxyClassMeta(classname, super_classes, context)
    clazz._proxy_server_url = spec.server_url
    clazz._proxy_base_class = base_class

    method_attrs = []

    for field_name in dir(base_class):
        field = getattr(base_class, field_name)

        if type(field) is types.ModuleType:
            raise Exception('unexpected')

        if field_name in clazz.__dict__:
            pass
        elif field_name in [
                '__class__',
                '__dict__',
                '__init__',
                '__new__',
                '__getattribute__',
                '__getattr__',
                '__setattr__',
                '__init_subclass__',
                '__subclasshook__',
                '__dir__',
                '__doc__',
                '__array_finalize__',
        ]:
            # TODO: take a closer look at the list above
            pass
        elif field_name in ['__name__']:
            setattr(clazz, field_name, 'proxy for %s' % base_class.__name__)
        else:
            typ = type(field)
            if typ == staticmethod:
                call_as = 'staticmethod'
            elif typ == types.MethodType:
                call_as = 'classmethod'
            else:
                like_method = any([
                    inspect.ismethod(field),
                    inspect.isfunction(field),
                    inspect.ismethoddescriptor(field),
                    inspect.isbuiltin(field)])
                if like_method:
                    call_as = 'method'
                else:
                    call_as = 'attr'
                    # TODO: be more explicit here, raise exception on
                    # unhandled types

            if call_as != 'attr':
                method_attrs.append(field_name)

            if call_as == 'attr':
                fn = ProxyAttribute(field_name, spec)
            elif call_as == 'method':
                fn = ProxyInstanceMethod(field_name, spec)
            elif call_as == 'staticmethod':
                fn = ProxyStaticMethod(base_class, field_name, spec)
            elif call_as == 'classmethod':
                fn = ProxyClassMethod(base_class, field_name, spec)

            # logger.debug('%s, %s, %s' % (base_class.__name__, field_name, call_as))

            setattr(clazz, field_name, fn)

    local = frozenset(dir(clazz))
    clazz.__getattribute__ = ProxyAttributeGetter(spec, local, method_attrs)

    return clazz
