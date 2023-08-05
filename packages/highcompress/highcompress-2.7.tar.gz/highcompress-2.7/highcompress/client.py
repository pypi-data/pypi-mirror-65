# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import requests
import urllib.request
from dotmap import DotMap
import json
import base64

class Client(object):

    def __init__(self, key):
        self.key=key

    def requests(self, api, data, path):

        url = "http://127.0.0.1:8000/api/v3/compress"
        ext = data.split(".")[-1::1][0]
        payload = {'type': 'python','mime': ext}
        files = [
                ('data', open(data,'rb'))
        ]
        key = "api:"+api
        auth = base64.b64encode(key.encode()).decode()
        headers = {
        'Authorization': 'Basic '+auth
        }
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        data = response.json()
        if data["status"]=="200":
            urllib.request.urlretrieve(data["location"], path)
            data.pop('location', None)
            data.pop('status', None)
        return data
        
    def check_credits(self):
        if self.key == "":
            return "Please set the api key first"
        url = "http://127.0.0.1:8000/api/v3/info"
        key = "api:"+self.key
        auth = base64.b64encode(key.encode()).decode()
        payload = {}
        headers = {
        'Authorization': 'Basic '+auth
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        return (response.json())
