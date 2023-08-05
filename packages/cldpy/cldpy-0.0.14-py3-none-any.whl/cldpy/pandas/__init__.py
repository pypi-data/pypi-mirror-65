# These imports should occur before cloud versions
import pandas
import numpy

import sys
import os
import math

import requests
import humanize

from xmlrpc.client import ServerProxy

from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from npc_internal.monkey_patch import monkey_patch
from npc_internal.config import SERVER_URL
from npc_internal.util import get_fullname, sha256_file
from npc_internal.proxy import get_factory_singleton
from npc_internal.protocol import Request, Response

import cldpy.numpy


_internal_names_set = []
_internal_names = []
_metadata = ['_npc_proxy_id']

class SeriesProxy(object):

    _internal_names_set = _internal_names_set
    _internal_names = _internal_names
    _metadata = _metadata

    def __init__(self, *args, **kwargs):
        pass

    @property
    def _constructor(self):
        return SeriesProxy

    @property
    def _constructor_expanddim(self):
        return DataFrameProxy


class DataFrameProxy(object):

    _internal_names_set = _internal_names_set
    _internal_names = _internal_names
    _metadata = _metadata

    def __init__(self, *args, **kwargs):
        pass

    @property
    def _constructor(self):
        return DataFrameProxy

    @property
    def _constructor_sliced(self):
        return SeriesProxy

    @property
    def _constructor_expanddim(self):
        return PanelProxy


class PanelProxy(object):

    _internal_names_set = _internal_names_set
    _internal_names = _internal_names
    _metadata = _metadata

    def __init__(self, *args, **kwargs):
        pass

    @property
    def _constructor(self):
        return PanelProxy

    @property
    def _constructor_sliced(self):
        return DataFrameProxy


class ProxyStandIn(object):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls.__base__)

    def __init__(self, *args, **kwargs):
        pass


proxy_classes = {
    'pandas.core.series.Series': {'class': SeriesProxy, 'base_is_superclass': True},
    'pandas.core.frame.DataFrame': {'class': DataFrameProxy, 'base_is_superclass': True},
    'pandas.core.panel.Panel': {'class': PanelProxy, 'base_is_superclass': True},

    'pandas.core.groupby.groupby.DataFrameGroupBy': {},
    'pandas.core.indexes.base.Index': {},
    'pandas.core.indexes.multi.MultiIndex': {},
    'pandas.core.indexes.numeric.Int64Index': {},
    'pandas.core.indexing._iLocIndexer': {},
    'pandas.core.internals.BlockManager': {},
}

monkey_patch('pandas', 'cldpy.pandas', SERVER_URL, proxy_classes)
del sys.modules['cldpy.pandas']
__import__('cldpy.pandas')


class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                ratio = self.readsofar / self.totalsize
                percent = ratio * 100
                _, filename_tail = os.path.split(self.filename)
                l = 20
                full = math.ceil(ratio * l)
                full_str = '=' * full
                empty_str = ' ' * (l - full)
                if full != l and full >= 1:
                    full_str = full_str[:full-1] + '>'
                fraction = "({done}/{total})".format(
                    done=humanize.naturalsize(self.readsofar),
                    total=humanize.naturalsize(self.totalsize)).rjust(20, ' ')
                sys.stderr.write("\rUploading {filename}: [{full}{empty}] {percent:3.0f}%"
                                 " {fraction}".format(
                                     filename=filename_tail,
                                     full=full_str,
                                     empty=empty_str,
                                     percent=percent,
                                     fraction=fraction))
                yield data

    def __len__(self):
        return self.totalsize



proxy_read_csv = sys.modules['cldpy.pandas'].read_csv
def read_csv(filepath_or_buffer, **kwargs):
    if (hasattr(filepath_or_buffer, 'read') or not os.path.isfile(filepath_or_buffer)):
        return proxy_read_csv(filepath_or_buffer.read(), **kwargs)

    content_type = 'text/csv'
    with ServerProxy(SERVER_URL, allow_none=True) as server:
        file_hash = sha256_file(filepath_or_buffer)
        has_file = server.has_file(file_hash, content_type)
        if not has_file:
            url = server.upload_url(file_hash, content_type)
        if not has_file:
            data = upload_in_chunks(filepath_or_buffer)
            resp = requests.put(url, headers={'Content-Type': content_type},
                                data=data)
        req = Request('', '', '', [], kwargs)
        resp = Response.deserialize(server.from_file(file_hash, content_type, req.serialize()))
        return resp.unpack(get_factory_singleton())
sys.modules['cldpy.pandas'].read_csv = read_csv
