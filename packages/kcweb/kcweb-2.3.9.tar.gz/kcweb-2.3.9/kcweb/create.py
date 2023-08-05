# -*- coding: utf-8 -*-
import os,re,traceback,shutil,platform,sys
from mako.template import Template as kcwTemplate
def Template(path,**context):
    body=''
    with open(str(path), 'r',encoding='utf-8') as f:
        content=f.read()
        t=kcwTemplate(content)
        body=t.render(**context)
    return body
class create:
    appname=None
    modular=None
    path=os.path.split(os.path.realpath(__file__))[0] #当前文件目录 
    def __init__(self,appname="application",modular="api"):
        self.appname=appname
        self.modular=modular
        if not os.path.exists(self.appname):
            os.makedirs(self.appname)
        if not os.path.exists(self.appname+"/script"):
            os.makedirs(self.appname+"/script/common")
            f=open(self.appname+"/script/common/__init__.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/script/common/__init__.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
            f=open(self.appname+"/script/common/win.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/script/common/win.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
            f=open(self.appname+"/script/test.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/script/test.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
        if not os.path.exists(self.appname+"/common"):
            os.makedirs(self.appname+"/common")
            f=open(self.appname+"/common/__init__.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/common/__init__.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
        if not os.path.exists(self.appname+"/config"):
            os.makedirs(self.appname+"/config")
            f=open(self.appname+"/config/__init__.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/config/__init__.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
            f=open(self.appname+"/config/other.py","w+",encoding='utf-8')
            content=Template(self.path+"/application/config/other.py",appname=appname,modular=modular)
            f.write(content)
            f.close()
        if not os.path.exists(self.appname+"/"+self.modular): #创建模块
            os.makedirs(self.appname+"/"+self.modular)
            self.zxmodular("")
        #在应用目录下创建初始化文件
        lists=os.listdir(self.appname)
        modulars=[]
        filters=['__init__','__pycache__','common','config','runtime','log']
        for files in lists:
            if not os.path.isfile(self.appname+"/"+files):
                if files not in filters:
                    modulars.append(files)
        f=open(self.appname+"/__init__.py","w+",encoding='utf-8')
        content=Template(self.path+"/application/__init__.py",appname=appname,tuple_modular=modulars)
        f.write(content)
        f.close()
        if "Windows" in platform.platform():
            pythonname="python"
        else:
            pythonname="python3"
        sys.argv[0]=re.sub('.py','',sys.argv[0])
        content=('# #gunicorn -b 0.0.0.0:39010 '+self.appname+':app\n'+
                 'from kcweb import web\n'+
                 'import '+self.appname+' as application\n'+
                 'app=web(__name__,application)\n'+
                 'if __name__ == "__main__":\n'+
                 '    #server 是当前文件名  host监听ip port端口 name python解释器名字 (windows一般是python  linux一般是python3)\n'+
                 '    app.run("'+sys.argv[0]+'",host="0.0.0.0",port="39001",name="'+pythonname+'")')
        f=open("./"+sys.argv[0]+".py","w+",encoding='utf-8')
        f.write(content)
        f.close()
    def zxmodular(self,sourcep):
        "处理模块文件"
        path1=self.path+"/application/api"+sourcep
        path2=self.appname+"/"+self.modular+sourcep
        lists=os.listdir(path1)
        for files in lists:
            if os.path.isfile(path1+"/"+files):
                if ".py" in files:
                    content=Template(path1+"/"+files,appname=self.appname,modular=self.modular)
                    f=open(path2+"/"+files,"w+",encoding='utf-8')
                    f.write(content)
                    f.close()
                else:
                    f=open(path1+"/"+files,"r",encoding='utf-8')
                    content=f.read()
                    f.close()
                    f=open(path2+"/"+files,"w+",encoding='utf-8')
                    f.write(content)
                    f.close()
            elif files != '__pycache__':
                if not os.path.exists(path2+"/"+files):
                    os.makedirs(path2+"/"+files)
                self.zxmodular(sourcep+"/"+files)

