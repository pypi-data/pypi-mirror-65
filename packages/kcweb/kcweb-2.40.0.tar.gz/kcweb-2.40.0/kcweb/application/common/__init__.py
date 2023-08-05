# -*- coding: utf-8 -*-
from kcweb.common import *
from ${appname} import config
import math
def return_list(lists,count,pagenow,pagesize):
    """返回分页列表

    lists 数据库列表数据

    count 数据库总数量

    pagenow 页码

    pagesize 每页数量
    """
    data={
        'count':count,
        'pagenow':pagenow,
        'pagesize':pagesize,
        'pagecount':math.ceil(int(count)/int(pagesize)),
        'lists':lists
    }
    return data
def successjson(data=[],code=0,msg="成功",status='200 ok'):
    """成功说在浏览器输出包装过的json

        参数 data 结果 默认[]

        参数 code body状态码 默认0

        参数 msg body状态描述 默认 成功

        参数 status http状态码 默认 200

        返回 json字符串结果集 
        """
    res={
        "code":code,
        "msg":msg,
        "time":times(),
        "data":data
    }
    return json_encode(res),status,{"Content-Type":"application/json; charset=utf-8","Access-Control-Allow-Origin":"*"}
def errorjson(data=[],code=1,msg="失败",status='500 error'):
    """错误时在浏览器输出包装过的json

    参数 data 结果 默认[]

    参数 code body状态码 默认0

    参数 msg body状态描述 默认 成功

    参数 status http状态码 默认 200

    返回 json字符串结果集 
    """
    return successjson(data=data,code=code,msg=msg,status=status)
def randoms(lens=6,types=1):
    """生成随机字符串
    
    lens 长度

    types 1数字 2字母 3字母加数字
    """
    strs="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,!@#$%^&*()_+=-;',./:<>?"
    if types==1:
        strs="0123456789"
    elif types==2:
        strs="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    elif types==3:
        strs="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    k=''
    i=0
    while i < lens:
        k+=random.choice(strs)
        i+=1
    return k