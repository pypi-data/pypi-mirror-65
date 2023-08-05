# -*- coding: utf-8 -*-
from ${appname}.${modular}.common import *
def index():
    return tpl("/v1/index/index.html",title="欢迎使用kcweb框架",data=['这是${appname}应用${modular}模块下v1版本的一个模板渲染测试效果'])
def inter(id='',title=""):
    data={
        'title':title,
        'id':id
    }
    return successjson(data)
def home(id='',title=""):
    data={
        "title":"标题是"+title,
        "id":"id是"+id
    }
    return successjson(data)