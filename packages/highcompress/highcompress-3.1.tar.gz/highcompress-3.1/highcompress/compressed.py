# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import highcompress
import base64


class Compressed(object):
    
    @staticmethod
    def from_file(cls, path, path2=""):
        validExt=["jpg","png","JPG","PNG","JPEG","jpeg"]
        if path == "":
            return "Please provide image path"
        ext = path.split(".")[-1::1][0]
        if ext not in validExt:
            return "Please provide valid image (jpg, png or jpeg)"
        if(path2==""):
            path2=path
        return cls._shrink_high(path,path2)

    @staticmethod
    def shrink_high(cls,data,path2):
        if not cls.apikey:
            return ('Provide an API key with highcompress.key = ...')
        else:
            response = cls._request(cls.apikey,data,path2)
        return response
