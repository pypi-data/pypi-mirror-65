import inspect
import re
import sys
import traceback
import types

import numpy as np

from xmlrpc.client import ServerProxy

from npc_internal.logger import logger
from npc_internal.protocol import Request, Response
from npc_internal.proxy import (
    get_factory_singleton,
    create_proxy_class,
    ProxyFactory,
    ProxySpec,
    ProxyId,
)

from npc_internal.util import get_fullname
    

# TODO: refactor this class to separate module find/loading from runtime proxy management
class MonkeyPatch(object):

    def __init__(self, base_name, target_name, server_url, class_specs):
        global factory_singleton
        self.base_name = base_name
        self.target_name = target_name
        self.class_specs = class_specs
        # self.module_proxy_id = '%s:%s' % (self.target_name, uuid.uuid4())
        self.module_proxy_id = ProxyId.random_id(self.target_name, True)
        self.spec = ProxySpec(server_url, self.module_proxy_id, get_factory_singleton())
        self.server_url = server_url
        self.objects = {}

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.target_name):
            return self

        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        print('monkey patch "%s"' % fullname)

        stash = self._stash_modules(self.base_name)
        new_fullname = fullname.replace(self.target_name, self.base_name)
        modules_from_import, modules_from_fields = self._reimport(new_fullname)
        self._restore_stash(stash)

        modules_to_proxy = {}
        modules = {}
        modules.update(modules_from_import)
        modules.update(modules_from_fields)
        to_install = []
        from_local_modules = {}
        for name, module in modules.items():
            name_as_target = re.sub(
                r'^%s(\.|$)' % self.base_name, self.target_name + r'\1', name)

            # Try to pull from sys.modules to perserve equality for module
            # comparisons. This helps some test functions, and probably useful
            # elsewhere.
            modules_to_proxy[name_as_target] = sys.modules.get(name, module)

            if name in modules_from_import:
                to_install.append(name_as_target)

        proxy_modules = self._create_proxy_modules(modules_to_proxy)
        to_install_dict = {}
        install_modules = {}
        install_modules.update(from_local_modules)
        install_modules.update(proxy_modules)
        for name in to_install:
            to_install_dict[name] = install_modules[name]
        self._install_proxy_modules(to_install_dict)

        return sys.modules[fullname]

    def _stash_modules(self, base_name):
        stash = {}
        for name, module in sys.modules.items():
            if name.startswith(base_name + '.') or name == base_name:
                stash[name] = module
        for name, module in stash.items():
            del sys.modules[name]
        return stash

    def _get_module_fields(self, module):
        module_fields = {}
        for field_name in dir(module):
            field = getattr(module, field_name)
            if type(field) is types.ModuleType:
                if self._is_descendant(field):
                    module_fields[field_name] = field
        return module_fields

    def _reimport(self, fullname):
        meta_path = []
        for item in sys.meta_path:
            if not isinstance(item, MonkeyPatch):
                meta_path.append(item)
        old_meta_path = sys.meta_path
        sys.meta_path = meta_path
        __import__(fullname)
        sys.meta_path = old_meta_path

        modules_from_import = {}
        modules_from_fields = {}
        for name, module in sys.modules.items():
            if self._is_mine(name):
                modules_from_import[name] = module

                module_fields = self._get_module_fields(module)
                for field_name, module in module_fields.items():
                    full_module_field_name = name + '.' + field_name
                    modules_from_fields[full_module_field_name] = module

        self._unimport(modules_from_import.keys())
        return (modules_from_import, modules_from_fields)

    def _create_proxy_modules(self, modules):
        for proxy_name, base_module in modules.items():
            self.spec.factory.create_module(
                base_module, self, proxy_name, self.spec)

        for proxy_name, base_module in modules.items():
            self.spec.factory.populate_module(
                proxy_name, self.class_specs, self.base_name,
                self.target_name, self.spec)

        proxy_modules = self.spec.factory.modules
        return proxy_modules

    def _install_proxy_modules(self, proxy_modules):
        for name, module in proxy_modules.items():
            sys.modules[name] = module

    def _unimport(self, names):
        for name in names:
            del sys.modules[name]

    def _restore_stash(self, stash):
        for name, module in stash.items():
            if name in sys.modules:
                raise Exception('refusing to override %s' % name)
            sys.modules[name] = module

    def _is_descendant(self, module):
        return module.__name__.startswith(self.base_name + '.')

    def _is_mine(self, name):
        return name.startswith(self.base_name + '.') or name == self.base_name


def monkey_patch(base_name, target_name, server_url, proxy_classes):  
    meta_path = []
    for loader in sys.meta_path:
        if not isinstance(loader, MonkeyPatch):
            meta_path.append(loader)
    sys.meta_path = [MonkeyPatch(base_name, target_name, server_url, proxy_classes)] + meta_path
