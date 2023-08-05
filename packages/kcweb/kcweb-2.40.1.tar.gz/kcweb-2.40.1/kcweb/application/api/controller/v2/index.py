# -*- coding: utf-8 -*-
from ${appname}.${modular}.common import *
def index():
    return tpl("/v2/index/index.html",title="欢迎使用kcweb框架",data=['这是${appname}应用${modular}模块下v2版本的一个模板渲染测试效果'])
def inter():
    data={
        'title':'欢迎使用kcweb框架',
        'desc':'这是${appname}应用${modular}模块下v2版本的json输出效果'
    }
    return successjson(data)