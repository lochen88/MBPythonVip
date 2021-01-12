# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


from MBPythonVip import miniblink
from MBPythonVip import set_icon

from callbackfunc import callBackTest
from config import icon_path,node_path,mb_path
from MBPythonVip.wkeStruct import Rect

mbpython=miniblink.Miniblink
mb=mbpython.init(node_path,mb_path)
wke=mbpython(mb)

import win32gui
from win32con import *
from ctypes import windll,byref
user32=windll.user32
def WndProc(hwnd,msg,wParam,lParam):
    if msg == WM_PAINT:
        rect=Rect()
        user32.GetClientRect(hwnd,byref(rect))
        window.mbResize(webview,rect.Right - rect.Left,rect.Bottom - rect.Top)
    if msg == WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)
def get_hwnd():
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = "测试-1191826896"
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW
    wc.lpfnWndProc = WndProc
    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindowEx(0, reg,'窗口绑定测试-1191826896',WS_OVERLAPPEDWINDOW,300,100,860,760, 0, 0, 0, None)
    return hwnd

def test():
    if mb==0:return
    global webview,window,network
    window=wke.window
    callback=wke.callback
    network=wke.network

    cbtest=callBackTest(mb,None,callback,network)
    callback.mbDocumentReadyCallback=cbtest.document_ready_func

    hwnd=get_hwnd()
    webview=window.bind_window(hwnd=hwnd)
    set_icon(hwnd,icon_path)

    param='ojbk-1191826896'
    callback.mbOnDocumentReady(webview,param=param)
    callback.mbOnDestroy(webview)

    network.mbLoadURL(webview,'https://www.baidu.com/')

    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    win32gui.PumpMessages()
if __name__=='__main__':
    test()