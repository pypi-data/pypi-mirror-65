# -*- coding: utf-8 -*-
import socket,time,re,os,sys,traceback,threading,urllib
from . Events import Events
from . common import *
from . import config
from mako.template import Template
from datetime import datetime
from threading import local
from .utill import filetype
from kcweb.utill.cache import cache as kcwcache
class web:
    __name=None
    __appname=None
    __config=config 
    def __new__(self,name,appname=None):
        self.__name=name
        self.__appname=appname
        if self.__name != '__main__':
            def apps(env, start_response):
                # REQUEST_METHOD=env['REQUEST_METHOD'] #GET
                # QUERY_STRING=env['QUERY_STRING'] #a=1&b=1
                # RAW_URI=env['RAW_URI'] #/aa/bb/cc?a=1&b=1
                # SERVER_PROTOCOL=env['SERVER_PROTOCOL'] #HTTP/1.1
                # HTTP_HOST=env['HTTP_HOST'] #212.129.149.238:39010
                # HTTP_COOKIE=env['HTTP_COOKIE'] #cookie
                # REMOTE_ADDR=env['REMOTE_ADDR'] #27.156.27.201
                # PATH_INFO=env['PATH_INFO'] #/aa/bb/cc
                # HTTP_USER_AGENT=env['HTTP_USER_AGENT'] #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
                try:
                    env['BODY_DATA']=str(env['wsgi.input'].next(), encoding = "utf-8")
                except:
                    env['BODY_DATA']=""
                p=(config.app['staticpath']+env['RAW_URI'].replace(' ',''))
                status='200 ok'
                if os.path.isfile(p):
                    kind = filetype.guess(p)
                    if kind is None:
                        f=open(p,"rb")
                        body=f.read()
                        f.close()
                        resheader=[
                            ("Cache-Control","public, max-age=43200"),
                        ]
                    else:
                        f=open(p,"rb")
                        body=f.read()
                        f.close()
                        resheader=[
                            ("Content-Type",kind.mime),
                            ("Cache-Control","public, max-age=43200"),
                            ("Accept-Ranges","bytes"),
                            # ("Content-Length",len(body))
                        ]
                else:
                    status,resheader,body=self.__routes(self,env)
                    body=bytes(body, encoding='utf-8')
                # print(env['bodydata'])
                # print("\n\nwsgi.input",env['wsgi.input'])
                # print("\n\ndir(env['wsgi.input'])",dir(env['wsgi.input']))
                # print("\n\nenv['wsgi.input'].__dict__",env['wsgi.input'].__dict__)
                # try:
                #     print("\n\nwsgi.input.buf()",env['wsgi.input'].buf())
                # except Exception as e:
                #     print("\n\nwsgi.input.buf() error:",e)
                # try:
                #     print("\n\nwsgi.input.next()",env['wsgi.input'].next())
                # except Exception as e:
                #     print("\n\nwsgi.input.next() error:",e)
                # try:
                #     print("\n\nwsgi.input.read()",env['wsgi.input'].read())
                # except Exception as e:
                #     print("\n\nwsgi.input.read() error:",e)
                # try:
                #     print("\n\nwsgi.input.reader()",env['wsgi.input'].reader())
                # except Exception as e:
                #     print("\n\nwsgi.input.reader() error:",e)
                # try:
                #     print("\n\nwsgi.input.readline()",env['wsgi.input'].readline())
                # except Exception as e:
                #     print("\n\nwsgi.input.readline() error:",e)
                # try:
                #     print("\n\nwsgi.input.readlines()",env['wsgi.input'].readlines())
                # except Exception as e:
                #     print("\n\nwsgi.input.readlines() error:",e)
                # try:
                #     print("wsgi.input.aa",env['wsgi.input'].get("SCRIPT_NAME", ""))
                # except Exception as e:
                #     print("wsgi.input.get('aa') error:",e)
                # try:
                #     print("wsgi.input.aa",env['wsgi.input']['aa'])
                # except Exception as e:
                #     print("wsgi.input['aa'] error:",e)
                # print(dir(env['wsgi.input']).getsize)
                # from io import StringIO
                # stdout = StringIO()
                # print("Hello world!", file=stdout)
                # print(file=stdout)
                # h = sorted(env.items())
                # for k,v in h:
                #     print(k,'=',repr(v), file=stdout)
                # print(stdout.getvalue().encode("utf-8"))
                start_response(status,resheader)
                return [body]
            return apps
        else:
            return super().__new__(self)
    def run(self,filename,host="127.0.0.1",port="39001",name='python3'):
        """运行开发环境

        filename: 命令行脚本名称

        host: 监听地址
        
        port: 端口

        name: python命令行解释机名字 默认python3
        """
        if self.__config.app['app_debug']:
            arg=sys.argv
            if len(arg)==2 and arg[1]=='eventlog':
                self.__impl(host=host,port=port,filename=filename)
            else:
                Events([name,str(filename)+'.py','eventlog'])
        else:
            self.__impl(
                host=host,
                port=port,
                filename=filename
            )
    def __impl(self,host,port,filename):
        "运行测试服务器"
        try:
            self.__http_server(
                host=host,
                port=port,
                filename=filename
            )
        except KeyboardInterrupt:
            pass
    def __get_modular(self,header):
        "获取模块"
        modular=''
        route=self.__config.route
        if route['modular']:
            if isinstance(route['modular'],str):
                modular=route['modular']
            else:
                HTTP_HOST=header['HTTP_HOST'].split(".")[0]
                for mk in route['modular']:
                    if HTTP_HOST in mk:
                        modular=mk[HTTP_HOST]
        return modular
    def __getconfigroute(self,PATH_INFO,header):
        "使用配置路由"
        route=self.__config.route
        routedefault=route['default']
        methods=route['methods']
        paths=''
        for path in PATH_INFO:
            paths+="/"+path
        try:
            for item in route['children']:
                if ':' in item['path']:
                    path=item['path'].split(':')
                    if(len(path)==len(PATH_INFO)):
                        is_pp=False
                        try:
                            item['methods']
                        except:pass
                        else:
                            methods=item['methods']
                        for k in methods: #匹配请求方式
                            if header['REQUEST_METHOD'] in k:
                                is_pp=True
                                break
                        if path[0]==paths[:len(path[0])] and is_pp:
                            del PATH_INFO[0]
                            cs=PATH_INFO
                            PATH_INFO=item['component'].split('/')
                            for v in cs:
                                PATH_INFO.append(v)
                            routedefault=True
                            break
                elif item['path']==paths or item['path']+'/'==paths:
                    PATH_INFO=item['component'].split('/')
                    routedefault=True
                    break
        except:pass
        return routedefault,PATH_INFO
    def defaultroute(self,header,PATH_INFO):
        "路由匹配"
        route=self.__config.route
        modular=web.__get_modular(self,header)
        routedefault=route['default']
        methods=route['methods']
        if routedefault:
            edition='index'
            files=route['files']
            funct=route['funct']
        else:
            edition=''
            files=''
            funct=''
        param=[]
        urls=''
        i=0
        HTTP_HOST=header['HTTP_HOST'].split(".")[0]
        ##默认路由start #################################################################################
        
        if modular:
            if route['edition']:  #匹配模块并且匹配了版本
                edition=route['edition']
                routedefault,PATH_INFO=web.__getconfigroute(
                    self,
                    PATH_INFO,
                    header
                )
                if routedefault: #使用路由
                    for path in PATH_INFO:
                        if path:
                            if i==0:
                                files=path
                                urls=urls+"/"+str(path)
                            elif i==1:
                                funct=path
                                urls=urls+"/"+str(path)
                            else:
                                param.append(urllib.parse.unquote(path))
                        i+=1
            else:                  #配置模块没有配置版本
                routedefault,PATH_INFO=web.__getconfigroute(
                    self,
                    PATH_INFO,
                    header
                )
                if routedefault: #使用默认路由
                    for path in PATH_INFO:
                        if path:
                            if i==0:
                                edition=path
                            elif i==1:
                                files=path
                                urls=urls+"/"+str(path)
                            elif i==2:
                                funct=path
                                urls=urls+"/"+str(path)
                            else:
                                param.append(urllib.parse.unquote(path))
                        i+=1
        elif route['edition']:  #配置版本的但没有匹配模块
            edition=route['edition']
            routedefault,PATH_INFO=web.__getconfigroute(
                self,
                PATH_INFO,
                header
            )
            if routedefault: #使用默认路由
                for path in PATH_INFO:
                    if path:
                        if i==0:
                            modular=path
                        elif i==1:
                            files=path
                            urls=urls+"/"+str(path)
                        elif i==2:
                            funct=path
                            urls=urls+"/"+str(path)
                        else:
                            param.append(urllib.parse.unquote(path))
                    i+=1
        else: #完全默认
            routedefault,PATH_INFO=web.__getconfigroute(self,PATH_INFO,header)
            for path in PATH_INFO:
                if path:
                    if i==0:
                        modular=path
                    elif i==1:
                        edition=path
                    elif i==2:
                        files=path
                        urls=urls+"/"+str(path)
                    elif i==3:
                        funct=path
                        urls=urls+"/"+str(path)
                    else:
                        param.append(urllib.parse.unquote(path))
                i+=1
        #默认路由end ############################################################
        return methods,modular,edition,files,funct,tuple(param)
    def __tran(self,data,status,resheader):
        "转换控制器返回的内容"
        if isinstance(data,tuple):
            i=0
            for item in data:
                if i==0:
                    body=item
                elif i==1:
                    status=item
                elif i==2:
                    if isinstance(item,dict):
                        for key in item:
                            resheader[key]=item[key]
                    else:
                        raise Exception('错误！这个不是一个字典')
                else:
                    break
                i+=1
        else:
            body=data
        return body,status,resheader
    def __set_globals(self,header):
        globals.HEADER.Method=header['REQUEST_METHOD']
        globals.HEADER.URL=header['RAW_URI']
        globals.HEADER.PATH_INFO=header['PATH_INFO']
        globals.HEADER.QUERY_STRING=header['QUERY_STRING']
        globals.HEADER.SERVER_PROTOCOL=header['SERVER_PROTOCOL']
        globals.HEADER.HTTP_HOST=header['HTTP_HOST']
        globals.HEADER.BODY_DATA=header['BODY_DATA']
        try:
            globals.HEADER.HTTP_COOKIE=header['HTTP_COOKIE']
        except:
            globals.HEADER.HTTP_COOKIE=None
        globals.HEADER.HTTP_USER_AGENT=header['HTTP_USER_AGENT']
    def __del_globals():
        globals.VAR = local()
        globals.HEADER = local()
        globals.G = local()
    def __routes(self,header):
        body="这是一个http测试服务器"
        status="200 ok"
        resheader={"Content-Type":"text/html; charset=utf-8"}
        web.__set_globals(self,header)
        PATH_INFO=header['PATH_INFO'].split('/')
        del PATH_INFO[0]
        methods,modular,edition,files,funct,param=web.defaultroute(self,header,PATH_INFO)
        if header['REQUEST_METHOD'] in methods:
            try:
                obj=getattr(web.__appname,modular)
            except (AttributeError,UnboundLocalError):
                status="500 Internal Server Error"
                body=web.__tpl(
                    title = status,
                    e=status,
                    data="无法找到目录："+str(modular)+"/"
                )
            else:
                try:
                    obj=getattr(obj,"controller")
                except (AttributeError,UnboundLocalError):
                    status="404 Not Found"
                    body=web.__tpl(
                        title = status,
                        e=status,
                        data="无法找到目录："+str(modular)+"/controller/"
                    )
                else:
                    try:
                        obj=getattr(obj,edition)
                    except (AttributeError,UnboundLocalError) as e:
                        con="无法找到目录："+str(modular)+"/controller/"+str(edition)+"/"
                        try:
                            data=getattr(obj,"error")(e,con)
                            body,status,resheader=web.__tran(
                                self,
                                data,
                                status,
                                resheader
                            )
                        except (AttributeError,UnboundLocalError):
                            status="404 Not Found"
                            body=web.__tpl(
                                title = status,
                                e=status,data=con
                            )
                        except Exception as e:
                            status="500 Internal Server Error"
                            errms=status
                            if self.__config.app['app_debug']:
                                print(traceback.format_exc())
                                errms=traceback.format_exc().split("\n")
                            body=web.__tpl(
                                title = status,
                                data=errms,e=e
                            )
                    else:
                        try:
                            obj=getattr(obj,files)
                        except (AttributeError,UnboundLocalError) as e:
                            con="无法找到文件："+str(modular)+"/controller/"+str(edition)+"/"+str(files)+".py"
                            try:
                                data=getattr(obj,"error")(e,con)
                                body,status,resheader=web.__tran(
                                    self
                                    ,data
                                    ,status
                                    ,resheader
                                )
                            except (AttributeError,UnboundLocalError):
                                status="404 Not Found"
                                body=web.__tpl(
                                    title = status
                                    ,data=con
                                    ,e=status)
                            except Exception as e:
                                status="500 Internal Server Error"
                                errms=status
                                if self.__config.app['app_debug']:
                                    print(traceback.format_exc())
                                    errms=traceback.format_exc().split("\n")
                                body=web.__tpl(
                                    title = status,
                                    data=errms,
                                    e=e
                                )
                        else:
                            try:
                                data=None
                                if self.__config.app['before_request']:  #请求前执行的函数
                                    try:
                                        data=getattr(obj,self.__config.app['before_request'])()
                                        if data:
                                            body,status,resheader=web.__tran(
                                                self,data,
                                                status,
                                                resheader
                                            )
                                    except (AttributeError):
                                        print(traceback.format_exc())
                                        pass
                                    except Exception as e:
                                        try:
                                            data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                                            body,status,resheader=web.__tran(
                                                self,data,
                                                status,
                                                resheader
                                            )
                                        except (AttributeError):
                                            data=True
                                            status="500 Internal Server Error"
                                            errms=status
                                            if self.__config.app['app_debug']:
                                                # print(traceback.format_exc())
                                                errms=traceback.format_exc().split("\n")
                                            body=web.__tpl(
                                                title = status,
                                                data=errms,e=e
                                            )
                                        except Exception as e:
                                            data=True
                                            status="500 Internal Server Error"
                                            errms=status
                                            if self.__config.app['app_debug']:
                                                print(traceback.format_exc())
                                                errms=traceback.format_exc().split("\n")
                                            body=web.__tpl(
                                                title = status,
                                                data=errms,e=e
                                            )
                                if not data:
                                    data=getattr(obj,funct)(*param)
                                    body,status,resheader=web.__tran(
                                        self,data,
                                        status,
                                        resheader
                                    )
                            except Exception as e:
                                try:
                                    data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                                    body,status,resheader=web.__tran(
                                        self,data,
                                        status,
                                        resheader
                                    )
                                except (AttributeError):
                                    status="500 Internal Server Error"
                                    errms=status
                                    if self.__config.app['app_debug']:
                                        print(traceback.format_exc())
                                        errms=traceback.format_exc().split("\n")
                                    body=web.__tpl(
                                        title = status,
                                        data=errms,
                                        e=e
                                    )
                                except Exception as e:
                                    status="500 Internal Server Error"
                                    errms=status
                                    if self.__config.app['app_debug']:
                                        print(traceback.format_exc())
                                        errms=traceback.format_exc().split("\n")
                                    body=web.__tpl(
                                        title = status,
                                        data=errms,
                                        e=e
                                    )
        else:
            status="405 Method Not Allowed"
            body=web.__tpl(
                title = status,
                data='405 Method Not Allowed',
                e=''
            )
        try:
            resheader['set-cookie']=globals.set_cookie
            del globals.set_cookie
        except:pass
        
        if self.__config.app['after_request']:  #请求后执行的函数
            try:
                data=getattr(obj,self.__config.app['after_request'])()
                if data:
                    body,status,resheader=web.__tran(self,data,status,resheader)
            except (AttributeError,UnboundLocalError):pass
            except Exception as e:
                try:
                    data=getattr(obj,"error")(e,traceback.format_exc().split("\n"))
                    body,status,resheader=web.__tran(
                        self,data,
                        status,
                        resheader
                    )
                except AttributeError as e:
                    status="500 Internal Server Error"
                    errms=status
                    if self.__config.app['app_debug']:
                        print(traceback.format_exc())
                        errms=traceback.format_exc().split("\n")
                    body=web.__tpl(
                        title = status
                        ,data=errms,
                        e=e
                    )
                except Exception as e:
                    status="500 Internal Server Error"
                    errms=status
                    if self.__config.app['app_debug']:
                        print(traceback.format_exc())
                        errms=traceback.format_exc().split("\n")
                    body=web.__tpl(
                        title = status,
                        data=errms,
                        e=""
                    )
        resheaders=[]
        for key in resheader:
            resheaders.append((key,resheader[key]))
        web.__del_globals()
        if isinstance(resheaders,list):
            if not body:
                body=''
            return str(status),resheaders,str(body)
        else:
            raise Exception()
    def __tpl(**context):
        path=os.path.split(os.path.realpath(__file__))[0]
        body=''
        with open(path+'/tpl/error.html', 'r',encoding='utf-8') as f:
            content=f.read()
            t=Template(content)
            body=t.render(**context)
        return body
    
    
    def __http_server(self,host,port,filename):
        tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            tcp_socket.bind((host,int(port)))
        except OSError:
            print("通常每个套接字地址(协议/网络地址/端口)只允许使用一次（按CTRL+C退出）")
        else:
            tcp_socket.listen(1024)
            print('! 警告：这是开发服务器。不要在生产环境中部署使用它')
            print('* 生产环境中建议使用gunicorn,gunicorn运行命令如：gunicorn -b '+host+':'+str(port)+' '+str(filename)+':app')
            if self.__config.app['app_debug']:
                print('* 调试器：开启')
            else:
                print('* 调试器：已关闭')
            print("* 运行在http://"+host+":"+str(port)+"/ （按CTRL+C退出）")
            while True:
                new_tcp_socket,client_info=tcp_socket.accept()
                t=threading.Thread(target=self.__server_client,args=(new_tcp_socket,))
                t.daemon=True
                t.start()
            tcp_socket.close()
    def __server_client(self,new_socket):
        # 处理http的的请求
        data=new_socket.recv(1047576).decode()
        if data:
            datas=data.split("\r\n")
            data1=datas[0]
            #reqsest
            REQUEST_METHOD=data1.split("/")[0].replace(' ','') ##GET
            RAW_URI=re.findall(REQUEST_METHOD+"(.+?) HTTP", data1) #/aa/bb/cc?a=1&b=1
            if RAW_URI:
                RAW_URI=RAW_URI[0]
            else:
                RAW_URI=''
            PATH_INFO=RAW_URI.split("?")[0] #/aa/bb/cc
            QUERY_STRING=RAW_URI.replace(str(PATH_INFO),'').replace('?','') #a=1&b=1
            SERVER_PROTOCOL=data1.split(" ")[-1] #HTTP/1.1
            HTTP_HOST=re.findall("Host: (.+?)\r\n", data)#212.129.149.238:39010
            if HTTP_HOST:
                HTTP_HOST=HTTP_HOST[0]
            else:
                HTTP_HOST=''
            HTTP_COOKIE=re.findall("Cookie: (.+?)\r\n", data)#cookie
            if HTTP_COOKIE:
                HTTP_COOKIE=HTTP_COOKIE[0]
            else:
                HTTP_COOKIE=''
            REMOTE_ADDR=''
            HTTP_USER_AGENT=re.findall("User-Agent: (.+?)\r\n", data) #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
            if HTTP_USER_AGENT:
                HTTP_USER_AGENT=HTTP_USER_AGENT[0]
            else:
                HTTP_USER_AGENT=''
            BODY_DATA=datas[len(datas)-1]
            # print(data)
            #reqsest
            reqheader={ 
                'REQUEST_METHOD':REQUEST_METHOD,
                'RAW_URI':RAW_URI,
                'PATH_INFO':PATH_INFO,
                'QUERY_STRING':QUERY_STRING,
                'SERVER_PROTOCOL':SERVER_PROTOCOL,
                'HTTP_HOST':HTTP_HOST,
                'HTTP_COOKIE':HTTP_COOKIE,
                'REMOTE_ADDR':REMOTE_ADDR,
                'HTTP_USER_AGENT':HTTP_USER_AGENT,
                'BODY_DATA':BODY_DATA
            }
            # print(BODY_DATA)
            p=(config.app['staticpath']+RAW_URI.replace(' ',''))
            # print("目录",p)
            status='200 ok'
            if os.path.isfile(p):
                # print('静态文件',p)
                kind = filetype.guess(p)
                if kind is None:
                    
                    f=open(p,"rb")
                    body=f.read()
                    f.close()
                    resheader=[("Cache-Control","public, max-age=43200"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                    
                    header="HTTP/1.1 %s \n" % status
                    header+="Content-Length:%d\n" % len(body)
                else:
                    f=open(p,"rb")
                    body=f.read()
                    f.close()
                    resheader=[("Content-Type",kind.mime),("Cache-Control","public, max-age=43200"),("Accept-Ranges","bytes"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                    header="HTTP/1.1 %s \n" % status
                    header+="Content-Length:%d\n" % len(body)
            else:
                status,resheader,body=self.__routes(reqheader)
                body=body.encode()
                header="HTTP/1.1 %s \n" % status
                header+="Content-Length:%d\n" % len(body)
            
            print(HTTP_HOST+' -- ['+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'] "'+REQUEST_METHOD+" "+RAW_URI +" "+SERVER_PROTOCOL + '" '+status+"-")
            t=time.time()
            header+="Server:kcweb\n"
            header+="Date:%s\n" % datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            for t in resheader:
                header+="%s:%s\n" % (t[0],t[1])
            header+="\n"
            try:
                new_socket.send(header.encode())
                new_socket.send(body)
            except Exception as e:
                pass
        new_socket.close() 
    def __http_sever(self,host,port):
        #http测试服务器
        if self.__config.app['app_debug']:
            print('* 调试器：开启')
        else:
            print('* 调试器：已关闭')
        print("* 运行在http://"+host+":"+str(port)+"/ （按CTRL+C退出）")
        tcp_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_socket.bind((host,int(port)))
        tcp_socket.listen(1024)
        pack_length=1024
        tcp_socket.setblocking(False)
        tcp_socket_list=list()
        
        
        while True:
            try:
                new_tcp_socket,client_info=tcp_socket.accept()
            except:
                pass
            else:
                new_tcp_socket.setblocking(False)
                tcp_socket_list.append(new_tcp_socket)
            for cli_soc in tcp_socket_list:
                try:
                    data=cli_soc.recv(pack_length).decode()
                except Exception as e:
                    pass
                else:
                    if data:
                        datas=data.split("\r\n")
                        data1=datas[0]
                        #reqsest
                        REQUEST_METHOD=data1.split("/")[0].replace(' ','') ##GET
                        RAW_URI=re.findall(REQUEST_METHOD+"(.+?) HTTP", data1) #/aa/bb/cc?a=1&b=1
                        if RAW_URI:
                            RAW_URI=RAW_URI[0]
                        else:
                            RAW_URI=''
                        PATH_INFO=RAW_URI.split("?")[0] #/aa/bb/cc
                        QUERY_STRING=RAW_URI.replace(str(PATH_INFO),'').replace('?','') #a=1&b=1
                        SERVER_PROTOCOL=data1.split(" ")[-1] #HTTP/1.1
                        HTTP_HOST=re.findall("Host: (.+?)\r\n", data)#212.129.149.238:39010
                        if HTTP_HOST:
                            HTTP_HOST=HTTP_HOST[0]
                        else:
                            HTTP_HOST=''
                        HTTP_COOKIE=re.findall("Cookie: (.+?)\r\n", data)#cookie
                        if HTTP_COOKIE:
                            HTTP_COOKIE=HTTP_COOKIE[0]
                        else:
                            HTTP_COOKIE=''
                        REMOTE_ADDR=''
                        HTTP_USER_AGENT=re.findall("User-Agent: (.+?)\r\n", data) #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0
                        if HTTP_USER_AGENT:
                            HTTP_USER_AGENT=HTTP_USER_AGENT[0]
                        else:
                            HTTP_USER_AGENT=''
                        BODY_DATA=datas[len(datas)-1]
                        #reqsest
                        reqheader={ 
                            'REQUEST_METHOD':REQUEST_METHOD,
                            'RAW_URI':RAW_URI,
                            'PATH_INFO':PATH_INFO,
                            'QUERY_STRING':QUERY_STRING,
                            'SERVER_PROTOCOL':SERVER_PROTOCOL,
                            'HTTP_HOST':HTTP_HOST,
                            'HTTP_COOKIE':HTTP_COOKIE,
                            'REMOTE_ADDR':REMOTE_ADDR,
                            'HTTP_USER_AGENT':HTTP_USER_AGENT,
                            'BODY_DATA':BODY_DATA
                        }
                        p=(config.app['staticpath']+RAW_URI.replace(' ',''))
                        
                        status='200 ok'
                        if os.path.isfile(p):
                            kind = filetype.guess(p)
                            if kind is None:
                                f=open(p,"rb")
                                body=f.read()
                                f.close()
                                resheader=[("Cache-Control","public, max-age=43200"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                                
                                header="HTTP/1.1 %s \n" % status
                                header+="Content-Length:%d\n" % len(body)
                            else:
                                f=open(p,"rb")
                                body=f.read()
                                f.close()
                                resheader=[("Content-Type",kind.mime),("Cache-Control","public, max-age=43200"),("Accept-Ranges","bytes"),("Expires","Thu, 07 Nov 2019 02:59:02 GMT")]
                                header="HTTP/1.1 %s \n" % status
                                header+="Content-Length:%d\n" % len(body)
                        else:
                            status,resheader,body=self.__routes(reqheader)
                            body=body.encode()
                            header="HTTP/1.1 %s \n" % status
                            header+="Content-Length:%d\n" % len(body)
                        
                        print(HTTP_HOST+' -- ['+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'] "'+REQUEST_METHOD+" "+RAW_URI +" "+SERVER_PROTOCOL + '" '+status+"-")
                        t=time.time()
                        header+="Server:kcweb\n"
                        header+="Date:%s\n" % datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
                        for t in resheader:
                            header+="%s:%s\n" % (t[0],t[1])
                        header+="\n"
                        try:
                            cli_soc.send(header.encode())
                            cli_soc.send(body)
                        except Exception as e:
                            cli_soc.close()
                    else:
                        cli_soc.close()
                        tcp_socket_list.remove(cli_soc)
        tcp_socket.close()
