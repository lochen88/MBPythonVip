# -*- coding:utf-8 -*-
from ctypes import (
    c_long,
    c_ushort,
    c_ulong,
    byref
)
from .wkeStruct import mPos

class Message():
    def __init__(self,miniblink):

        self.mb=miniblink
    def mbFireMouseEvent(self,webview,msg,x,y,flags=0):
        return self.mb.mbFireMouseEvent(webview,msg,x,y,flags)
    def mbFireKeyDownEvent(self,webview,virtualKeyCode,flags=0):
        return self.mb.mbFireKeyDownEvent(webview,virtualKeyCode,flags,False)
    def mbFireKeyUpEvent(self,webview,virtualKeyCode,flags=0):
        return self.mb.mbFireKeyUpEvent(webview,virtualKeyCode,flags,False)
    def mbFireKeyPressEvent(self,webview,virtualKeyCode,flags):
        return self.mb.mbFireKeyPressEvent(webview,virtualKeyCode,flags,False)
    def mbFireWindowsMessage(self,webview,hwnd,msg,wParam,lParam,result):
        return self.mb.mbFireWindowsMessage(webview,hwnd,msg,wParam,lParam,result)
    @staticmethod
    def fire_mouse_msg(hwnd,msg,x,y):
        pos=c_long(c_ushort(x).value | c_ulong(c_ushort(y).value).value << 16).value
        return user32.PostMessageW(hwnd,msg,0,pos)
    @staticmethod
    def fire_keyboard_msg(hwnd,virtualKeyCode,msg):
        return user32.SendMessageW(hwnd,msg,virtualKeyCode,0)
    @staticmethod
    def get_mouse_pos():
        p=mPos()
        user32.GetCursorPos(byref(p))
        return p
