# -*- coding: utf-8 -*-
#当前模块的公共类可以写在这里
from ${appname}.common import *
# import win32con,win32api  #安装 pip install -i https://mirrors.aliyun.com/pypi/simple/ pypiwin32  当前模块在windows系统上运行
# class win:
#     __code=None
#     def GetCursorPos(self):
#         "获取鼠标位置"
#         return win32api.GetCursorPos()
#     def set_CursorPos(self,x,y):
#         "设置鼠标位置"
#         win32api.SetCursorPos((x, y))
#     def left_press_down(self):
#         "鼠标左键按下"
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#     def left_bounce_up(self):
#         "鼠标左键弹起"
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
#     def left_click(self):
#         "鼠标左点击"
#         self.left_press_down()
#         time.sleep(0.1)
#         self.left_bounce_up()
#         time.sleep(0.1)
#     def right_press_down(self):
#         "鼠标右按下"
#         win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
#     def right_bounce_up(self):
#         "鼠标右键弹起"
#         win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
#     def right_click(self):
#         "鼠标右点击"
#         self.right_press_down()
#         time.sleep(0.1)
#         self.right_bounce_up()
#         time.sleep(0.1)
#     def key_code(self,code):
#         """键盘码按键
        
#         参数 code按键码  比如a是65  键盘对应数字，查表
#         """
#         win32api.keybd_event(code, 0, 0, 0)  # 键盘按下
#         win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0) #键盘弹起
#     def key_down(self,key):
#         "键盘按下"
#         self.__key_code(key)
#         win32api.keybd_event(self.__code, 0, 0, 0)  # 键盘按下
#     def key_up(self,key):
#         "键盘弹起"
#         self.__key_code(key)
#         win32api.keybd_event(self.__code, 0, win32con.KEYEVENTF_KEYUP, 0) #键盘弹起
#     def key_down_up(self,key):
#         "键盘 按下和弹起"
#         lens=len(key)
#         for i in range(0,lens):
#             self.__key_code(key[i:(i+1)])
#             win32api.keybd_event(self.__code, 0, 0, 0)  # 键盘按下
#             win32api.keybd_event(self.__code, 0, win32con.KEYEVENTF_KEYUP, 0) #键盘弹起
#     def __key_code(self,key):
#         "按键转按键码"
#         if key=='a':
#             self.__code=65
#         elif key=='b':
#             self.__code=66
#         elif key=='c':
#             self.__code=67
#         elif key=='d':
#             self.__code=68
#         elif key=='e':
#             self.__code=69
#         elif key=='f':
#             self.__code=70
#         elif key=='g':
#             self.__code=71
#         elif key=='h':
#             self.__code=72
#         elif key=='i':
#             self.__code=73
#         elif key=='j':
#             self.__code=74
#         elif key=='k':
#             self.__code=75
#         elif key=='l':
#             self.__code=76
#         elif key=='m':
#             self.__code=77
#         elif key=='n':
#             self.__code=78
#         elif key=='o':
#             self.__code=79
#         elif key=='p':
#             self.__code=80
#         elif key=='q':
#             self.__code=81
#         elif key=='r':
#             self.__code=82
#         elif key=='r':
#             self.__code=82
#         elif key=='s':
#             self.__code=83
#         elif key=='t':
#             self.__code=84
#         elif key=='u':
#             self.__code=85
#         elif key=='v':
#             self.__code=86
#         elif key=='w':
#             self.__code=87
#         elif key=='x':
#             self.__code=88
#         elif key=='y':
#             self.__code=89
#         elif key=='z':
#             self.__code=90
#         elif key=='0':
#             self.__code=48
#         elif key=='1':
#             self.__code=49
#         elif key=='2':
#             self.__code=50
#         elif key=='3':
#             self.__code=51
#         elif key=='4':
#             self.__code=52
#         elif key=='5':
#             self.__code=53
#         elif key=='6':
#             self.__code=54
#         elif key=='7':
#             self.__code=55
#         elif key=='8':
#             self.__code=56
#         elif key=='9':
#             self.__code=57