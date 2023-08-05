# -*- coding: utf-8 -*-
import time,hashlib,json,re,os,platform
import datetime as core_datetime
from kcweb import config
from kcweb.utill.dateutil.relativedelta import relativedelta as core_relativedelta
from kcweb.utill.db import mysql as kcwmysql
from kcweb.utill.db import mongodb as kcwmongodb
from kcweb.utill.db import sqlite as kcwsqlite
from kcweb.utill.cache import cache as kcwcache
from kcweb.utill.redis import redis as kcwredis
from kcweb.utill.http import Http
from kcweb.utill.db import model
from mako.template import Template as kcwTemplate

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from . import globals
redis=kcwredis()
def send_mail(user,text="邮件内容",theme="邮件主题",recNick="收件人昵称"):
    "发送邮件"
    ret=True
    if not theme:
        theme=config.email['theme']
    if not recNick:
        recNick=config.email['recNick']
    try:
        msg=MIMEText(text,'plain','utf-8')
        msg['From']=formataddr([config.email['sendNick'],config.email['sender']]) 
        msg['To']=formataddr([recNick,user]) 
        msg['Subject']=theme

        server=smtplib.SMTP_SSL("smtp.qq.com", 465) 
        server.login(config.email['sender'], config.email['pwd']) 
        server.sendmail(config.email['sender'],[user,],msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
get_sysinfodesffafew=None
def get_sysinfo():
    global get_sysinfodesffafew
    "获取系统信息"
    if get_sysinfodesffafew:
        sysinfo=get_sysinfodesffafew
    else:
        sysinfo={}
        sysinfo['platform']=platform.platform()        #获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'  
        sysinfo['version']=platform.version()         #获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        sysinfo['architecture']=platform.architecture()    #获取操作系统的位数，('32bit', 'ELF')
        sysinfo['machine']=platform.machine()         #计算机类型，'i686'
        sysinfo['node']=platform.node()            #计算机的网络名称，'XF654'
        sysinfo['processor']=platform.processor()       #计算机处理器信息，''i686'
        sysinfo['uname']=platform.uname()           #包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
        sysinfo['start_time']=times()
        get_sysinfodesffafew=sysinfo
            # 还可以获得计算机中python的一些信息：
            # import platform
            # platform.python_build()
            # platform.python_compiler()
            # platform.python_branch()
            # platform.python_implementation()
            # platform.python_revision()
            # platform.python_version()
            # platform.python_version_tuple()
    return sysinfo
def Template(path,**context):
    "模板渲染引擎函数,使用配置的模板路径"
    return Templates(str(config.app['tpl_folder'])+str(path),**context)
def Templates(path,**context):
    "模板渲染引擎函数，需要完整的模板目录文件"
    body=''
    with open(path, 'r',encoding='utf-8') as f:
        content=f.read()
        t=kcwTemplate(content)
        body=t.render(**context)
    return body
def mysql(table=None,configss=None):
    """mysql数据库操作实例
    
    参数 table：表名

    参数 configss 数据库配置  可以传数据库名字符串
    """
    dbs=kcwmysql.mysql()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.database).table(table)
def sqlite(table=None,configss=None):
    """sqlite数据库操作实例
    
    参数 table：表名

    参数 config 数据库配置  可以传数据库名字符串
    """
    dbs=kcwsqlite.sqlite()
    if table is None:
        return dbs
    elif configss:
        return dbs.connect(configss).table(table)
    else:
        return dbs.connect(config.sqlite).table(table)
def M(table=None,confi=None):
    """数据库操作实例
    
    参数 table：表名

    参数 config 数据库配置  可以传数据库名字符串
    """
    if confi:
        if confi['type']=='sqlite':
            return sqlite(table,confi)
        else:
            return mysql(table,confi)
    else:
        if config.database['type']=='sqlite':
            return sqlite(table)
        else:
            return mysql(table)
def mongo(table=None,configss=None):
    """mongodb数据库操作实例
    
    参数 table：表名(mongodb数据库集合名)

    参数 configss mongodb数据库配置  可以传数据库名字符串
    """
    mObj=kcwmongodb.mongo()
    if table is None:
        return mObj
    elif configss:
        return mObj.connect(configss).table(table)
    else:
        return mObj.connect(config.mongo).table(table)
def is_index(params,index):
    """判断列表或字典里的索引是否存在
    params  列表或字典
    index   索引值
    return True/False
    """
    try:
        params[index]
    except KeyError:
        return False
    except IndexError:
        return False
    else:
        return True
def set_cache(name,values,expire="no"):
    """设置缓存

        参数 name：缓存名

        参数 values：缓存值

        参数 expire：缓存有效期 0表示永久  单位 秒
        
        return Boolean类型
        """
    return kcwcache.cache().set_cache(name,values,expire)
def get_cache(name):
    """获取缓存

    return 或者的值
    """
    return kcwcache.cache().get_cache(name)
def del_cache(name):
    """删除缓存

    return Boolean类型
    """
    return kcwcache.cache().del_cache(name)
def md5(strs):
    """md5加密"""
    m = hashlib.md5()
    b = strs.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
def times():
    """时间戳 精确到秒"""
    return int(time.time())
def json_decode(strs):
    """json字符串转python类型"""
    try:
        return json.loads(strs)
    except Exception:
        return {}
def json_encode(strs):
    """转成字符串"""
    try:
        return json.dumps(strs,ensure_ascii=False)
    except Exception:
        return ""
def dateoperator(date,years=0,formats='%Y%m%d%H%M%S',months=0, days=0, hours=0, minutes=0,seconds=0,
                 leapdays=0, weeks=0, microseconds=0,
                 year=None, month=None, day=None, weekday=None,
                 yearday=None, nlyearday=None,
                 hour=None, minute=None, second=None, microsecond=None):
    """日期相加减计算
    date 2019-10-10
    formats 设置需要返回的时间格式 默认%Y%m%d%H%M%S
    
    years 大于0表示加年  反之减年
    months 大于0表示加月  反之减月
    days 大于0表示加日  反之减日

    return %Y%m%d%H%M%S
    """
    formatss='%Y%m%d%H%M%S'
    date=re.sub('[-年/月:：日 时分秒]','',date)
    if len(date) < 8:
        return None
    if len(date) < 14:
        s=14-len(date)
        i=0
        while i < s:
            date=date+"0"
            i=i+1
    d = core_datetime.datetime.strptime(date, formatss)
    strs=(d + core_relativedelta(years=years,months=months, days=days, hours=hours, minutes=minutes,seconds=seconds,
                 leapdays=leapdays, weeks=weeks, microseconds=microseconds,
                 year=year, month=month, day=day, weekday=weekday,
                 yearday=yearday, nlyearday=nlyearday,
                 hour=hour, minute=minute, second=second, microsecond=microsecond))
    strs=strs.strftime(formats)
    return strs
def get_folder():
    '获取当前框架所在目录'
    path=os.path.split(os.path.realpath(__file__))[0] #当前文件目录
    framepath=path.split('\\') ##框架主目录
    s=''
    for k in framepath:
        s=s+'/'+k
    framepath=s[1:]
    return re.sub('/kcw/common','',framepath) #包所在目录
# aa=[]
def get_file(folder='./',is_folder=True,suffix="*",lists=[],append=False):
    """获取文件夹下所有文件夹和文件

    folder 要获取的文件夹路径

    is_folder  是否返回列表中包含文件夹

    suffix 获取指定后缀名的文件 默认全部
    """
    if not append:
        lists=[]
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if is_folder:
                zd={"type":"folder","path":folder+"/"+files,'name':files}
                lists.append(zd)
            get_file(folder+"/"+files,is_folder,suffix,lists,append=True)
        else:
            if suffix=='*':
                zd={"type":"file","path":folder+"/"+files,'name':files}
                lists.append(zd)
            else:
                if files[-(len(suffix)+1):]=='.'+str(suffix):
                    zd={"type":"file","path":folder+"/"+files,'name':files}
                    lists.append(zd)
    return lists

def list_to_tree(data, pk = 'id', pid = 'pid', child = 'lowerlist', root=0,childstatus=True):
    """列表转换tree
    
    data 要转换的列表

    pk 关联节点字段

    pid 父节点字段

    lowerlist 子节点列表

    root 主节点值

    childstatus 当子节点列表为空时是否需要显示子节点字段
    """
    arr = []
    for v in data:
        if v[pid] == root:
            kkkk=list_to_tree(data,pk,pid,child,v[pk],childstatus)
            if childstatus:
                # print(kkkk)
                v[child]=kkkk
            else:
                if kkkk:
                    v[child]=kkkk
            arr.append(v)
    return arr
def get_url(url=''):
    "获取版本下的url"
    retstr='/'
    HTTP_HOST=globals.HEADER.HTTP_HOST.split(".")[0]
    route=config.route
    modular=None
    if route['modular']:
        for mk in route['modular']:
            if HTTP_HOST in mk:
                modular=mk[HTTP_HOST]
    if not modular:
        retstr=retstr+globals.HEADER.PATH_INFO.split("/")[1]+"/"
        if not route['edition']:
            retstr=retstr+globals.HEADER.PATH_INFO.split("/")[2]+"/"
    if not route['edition']:
        retstr=retstr+globals.HEADER.PATH_INFO.split("/")[1]+"/"
    retstr=retstr+url
    return retstr