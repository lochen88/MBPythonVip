# -*- coding:utf-8 -*-
from ctypes import (
    byref,
    windll
)
from ctypes.wintypes import MSG
from .winConst import WinConst
from .wkeStruct import Rect
from .wndproc import WndProcHook


user32=windll.user32
class Window():
    def __init__(self,miniblink):
        self.width=360
        self.height=480
        self.mb=miniblink
    def mbCreateWebWindow(self,_type=0,hwnd=0,x=0,y=0,width=360,height=480):
        webview =self.mb.mbCreateWebWindow(
            _type,hwnd, x, y,
            width, height
        )
        if _type==0:
            webview_hwnd=self.mb.mbGetHostHWND(webview)
            tmp_WndProc=WndProcHook(webview_hwnd,webview)
            tmp_WndProc.add_msg_func(WinConst.WM_SETCURSOR,self.onSetCursor)
            tmp_WndProc.hook_WndProc()

        return webview
    def mbShowWindow(self,webview,_bool=True):
        self.mb.mbShowWindow(webview,_bool)
    def mbCreateWebView(self):
        return self.mb.mbCreateWebView()
    def mbDestroyWebView(self,webview):
        self.mb.mbDestroyWebView(webview)
    def mbMoveToCenter(self,webview):
        self.mb.mbMoveToCenter(webview)
    def mbSetUserAgent(self,webview,ua):
        ua=ua.encode()
        self.mb.mbSetUserAgent(webview,ua)
    def mbSetDragEnable(self,webview,_bool):
        self.mb.mbSetDragEnable(webview,_bool)
    def mbAddPluginDirectory(self,webview,_path):
        self.mb.mbAddPluginDirectory(webview,_path)
    def mbSetNpapiPluginsEnabled(self,webview,_bool,_path=None):
        if _path!=None:
            self.wkeAddPluginDirectory(webview,_path)
        self.mb.mbSetNpapiPluginsEnabled(webview,_bool)
    def mbSetCspCheckEnable(self,webview,_bool=False):
        self.mb.mbSetCspCheckEnable(webview,_bool)
    def mbSetDebugConfig(self,webview,debug,param):
        debug=debug.encode()
        if isinstance(param,str):
            param=param.encode()
        self.mb.mbSetDebugConfig(webview,debug,param)
    def mbSetHeadlessEnabled(self,webview,_bool):
        self.mb.mbSetHeadlessEnabled(webview,_bool)
    def mbSetNavigationToNewWindowEnable(self,webview,_bool):
        self.mb.mbSetNavigationToNewWindowEnable(webview,_bool)
    def mbSetZoomFactor(self,webview,factor):
        self.mb.mbSetZoomFactor(webview,factor)
    def mbSetContextMenuEnabled(self,webview,_bool):
        self.mb.mbSetContextMenuEnabled(webview,_bool)
    def mbSetTransparent(self,webview,_bool):
        self.mb.mbSetTransparent(webview,_bool)
    def mbSetHandleOffset(self,webview,x,y):
        self.mb.mbSetHandleOffset(webview,x,y)
    def mbSetHandle(self,webview,hwnd):
        self.mb.mbSetHandle(webview,hwnd)
    def mbResize(self,webview,width=0,height=0):
        if width==0 or height==0:return False
        self.mb.mbResize(webview,width,height)
        return True
    def mbGoForward(self,webview):
        self.mb.mbGoForward(webview)
    def mbGoBack(self,webview):
        self.mb.mbGoBack(webview)
    def mbGetHostHWND(self,webview):
        return self.mb.mbGetHostHWND(webview)
    def mbWebFrameGetMainFrame(self,webview):
        return self.mb.mbWebFrameGetMainFrame(webview)
    def mbGetLockedViewDC(self,webview):
        hdc=self.mb.mbGetLockedViewDC(webview)
        return hdc
    def mbUnlockViewDC(self,webview):
        self.mb.mbUnlockViewDC(webview)
    def mbSetTouchEnabled(self,webview,_bool):
        b=not _bool
        self.mb.mbSetTouchEnabled(webview,_bool)
        self.mb.mbSetMouseEnabled(webview,b)
    def mbSetDeviceParameter(self,webview,key,value,_int,_float):
        key=key.encode()
        if value=='':
            value=b''
        else:
            value=value.encode()
        self.mb.mbSetDeviceParameter(webview, key,value,_int,_float)

    def bind_window(self,hwnd=0,show=True):
        if hwnd==0:
            user32.PostQuitMessage(0)
            return 0
        webview=self.mbCreateWebWindow(_type=2,hwnd=hwnd)
        rc=Window.get_client_rect(hwnd)
        width = rc.Right - rc.Left
        height = rc.Bottom - rc.Top
        self.mbResize(webview,width,height)
        self.mbShowWindow(webview,show)
        return webview
    def message_loop(self,webview=None):

        msg = MSG()
        while user32.GetMessageW(byref(msg), 0, 0, 0) > 0:
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))

    def onSetCursor(self,webview,hwnd, wParam, lParam):
        x=lParam & 65535
        y=lParam >> 16
        if x in [12,10,11,15,13,16,14,17]:
            if x==12:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENS))
            elif x==10:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZEWE))
            elif x==11:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZEWE))
            elif x==15:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENS))
            elif x==13:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENWSE))
            elif x==16:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENESW))
            elif x==14:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENESW))
            elif x==17:
                user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENWSE))
        else:
            self.mb.mbFireWindowsMessage(webview,hwnd,WinConst.WM_SETCURSOR,wParam,lParam,0)
        return 0


    @staticmethod
    def get_window_rect(hwnd):
        rect=Rect()
        user32.GetWindowRect(hwnd,byref(rect))
        return rect
    @staticmethod
    def get_client_rect(hwnd):
        rect=Rect()
        user32.GetClientRect(hwnd,byref(rect))
        return rect
