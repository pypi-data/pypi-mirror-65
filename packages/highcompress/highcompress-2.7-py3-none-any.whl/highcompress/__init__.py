# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import sys
class highcompress(object):

    def __init__(self, module):
        self._module = module
        self._client = None
        self._apikey = None
        self._compression_count = None
        self._apikey = None

    @property
    def key(self):
        return self.apikey

    @key.setter
    def key(self,value):
        self.apikey = value

    # Delegate to underlying base module.
    def __getattr__(self, attr):
        return getattr(self._module, attr)

    def from_file(self, source="", destination=""):
        if source == "":
             return "Please provide image path"
        return Compressed.from_file(self,source,destination)

    def _shrink_high(self,data,path2):
        return Compressed.shrink_high(self, data, path2)
        
    def check_credit(self):
        client=Client(self.key)
        return client.check_credits()

    def _request(self,key,data,path2):
        return Client.requests(self, key, data, path2)
        
        
highcompress = sys.modules[__name__] = highcompress(sys.modules[__name__])

from .compressed import Compressed
from .client import Client
