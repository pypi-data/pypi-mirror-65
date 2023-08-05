# -*- coding: utf-8 -*-
from ${appname}.common import *
#下面的方法在当前模块中有效
G=globals.G
#下面的方法在当前模块中有效
def before_request():
    G.userinfo=get_session("userinfo")
    print('${modular}模块在请求前执行，我是要在配置文件配置后才能生效哦！',G.userinfo)
def after_request():
    print('${modular}模块在请求后执行，我是要在配置文件配置后才能生效哦！')
def set_session(name,value,expire=None):
    "设置session"
    return session.set("${appname}${modular}"+str(name),value,expire)
def get_session(name):
    "获取session"
    return session.get("${appname}${modular}"+str(name))
def del_session(name):
    "删除session"
    return session.rm("${appname}${modular}"+str(name))
def tpl(path,**context):
    return Template("/${modular}/tpl/"+str(path),**context)
