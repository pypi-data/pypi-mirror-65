# -*- coding: utf-8 -*-
from kcweb.common import globals as kcwglobals
from urllib import parse
import json
class args:
    "获取url"
    def get(name):
        params = parse.parse_qs(parse.urlparse(kcwglobals.HEADER.URL).query)
        try:
            k=params[name][0]
        except:
            k=None
        return k
class froms:
    "获取from"
    def get(name):
        data=kcwglobals.HEADER.BODY_DATA
        params = parse.parse_qs(parse.urlparse("?"+str(data)).query)
        # print(params)
        try:
            k=parse.unquote(params[name][0])
        except:
            k=None
        return k
def get_data():
    "获取请求参数体"
    return kcwglobals.HEADER.BODY_DATA
def get_json():
    "获取请求参数体json"
    try:
        return json.loads(kcwglobals.HEADER.BODY_DATA)
    except:
        return None
