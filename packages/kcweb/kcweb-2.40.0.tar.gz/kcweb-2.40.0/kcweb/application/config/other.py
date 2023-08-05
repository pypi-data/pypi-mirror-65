# -*- coding: utf-8 -*-
from kcweb.config import *
#路由配置
route['default']=True #是否开启默认路由  默认路由开启后面不影响以下配置的路由，模块名/版本名/控制器文件名/方法名 作为路由地址   如：http://www.kcw.com/api/v1/index/index/
route['modular']='${modular}'
route['edition']='v1'
route['files']='index' #默认路由文件（控制器）
route['funct']='index'  #默认路由函数 (操作方法)
route['methods']=['POST','GET'] #默认请求方式
route['children']=[
    {'title':'首页','path':'','component':'index/home','methods':['POST','GET']},
    {'title':'接口','path':'/inter/:id','component':'index/inter','methods':['POST','GET']}
]
#sqlite配置
sqlite['db']='kcwlicuxweb' #sqlite数据库文件
