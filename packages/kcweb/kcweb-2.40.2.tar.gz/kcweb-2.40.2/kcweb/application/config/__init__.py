# -*- coding: utf-8 -*-
from .other import *
#下面的配置都是全局的
# 应用配置
app['app_debug']=True  #是否开启调试模式
app['tpl_folder']='./${appname}'  #设置模板文件目录名 注意：所有的配置目录都是以您的运行文件所在目录开始
app['before_request']='before_request'  #设置请求前要执行的函数名
app['after_request']='after_request'    #设置请求后要执行的函数名
app['staticpath']='${appname}/static'          #静态主要目录
# redis配置
redis['host']='127.0.0.1' #服务器地址
redis['port']=6379 #端口
redis['password']=''  #密码
redis['db']=0 #Redis数据库    注：Redis用0或1或2等表示
redis['pattern']=True # True连接池链接 False非连接池链接
redis['ex']=0  #过期时间 （秒）
#缓存配置
cache['type']='File' #驱动方式 支持 File Redis
cache['path']='./${appname}/runtime/cachepath' #缓存保存目录 
cache['expire']=120 #缓存有效期 0表示永久缓存
cache['host']=redis['host'] #Redis服务器地址
cache['port']=redis['port'] #Redis 端口
cache['password']=redis['password'] #Redis登录密码
cache['db']=1 #Redis数据库    注：Redis用1或2或3等表示
# session配置
session['type']='File' #session 存储类型  支持 file、Redis
session['path']='./${appname}/runtime/session/temp' #session缓存目录
session['expire']=86400 #session默认有效期 该时间是指session在服务的保留时间，通常情况下浏览器上会保留该值的10倍
session['prefix']="KCW" # SESSION 前缀
session['host']=redis['host'] #Redis服务器地址
session['port']=redis['port'] #Redis 端口
session['password']=redis['password'] #Redis登录密码
session['db']=2 #Redis数据库    注：Redis用1或2或3等表示

#email配置
email['sender']='' #发件人邮箱账号
email['pwd']='' #发件人邮箱密码(如申请的smtp给的口令)
email['sendNick']='' #发件人昵称
email['theme']='' #默认主题
email['recNick']='' #默认收件人昵称