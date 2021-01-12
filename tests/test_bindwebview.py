# -*- coding:utf-8 -*-
import os
import sys
from pathlib import Path
current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
os.chdir(str(current_folder))
sys.path.append(father_folder)


from MBPythonVip import miniblink

from config import node_path,mb_path
from callbackfunc import callBackTest

mbpython=miniblink.Miniblink
mb=mbpython.init(node_path,mb_path)
wke=mbpython(mb)

import win32gui
from win32con import *
from ctypes import windll
user32=windll.user32

def WndProc(hwnd,msg,wParam,lParam):
    if msg == WM_DESTROY:
        win32gui.PostQuitMessage(0)
        sys.exit(0)
        return 0
    return win32gui.DefWindowProc(hwnd,msg,wParam,lParam)
def get_hwnd():
    wc = win32gui.WNDCLASS()
    wc.hbrBackground = COLOR_BTNFACE + 1
    wc.hCursor = win32gui.LoadCursor(0,IDI_APPLICATION)
    wc.lpszClassName = "test-1191826896"
    wc.style =  CS_GLOBALCLASS|CS_VREDRAW | CS_HREDRAW
    wc.lpfnWndProc = WndProc
    reg = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(reg,'webview绑定测试-1191826896',WS_CLIPCHILDREN|WS_CLIPSIBLINGS|WS_POPUP|WS_MINIMIZEBOX,300,100,860,760,0,0,0,None)
    return hwnd

def test_js_run_py(**kwargs):
    webview=kwargs['webview']
    queryId=kwargs['queryId']
    customMsg=kwargs['customMsg']
    request=kwargs['request']
    param=kwargs['param']
    hwnd=param
    val=request
    print('test_js_run_py',customMsg,request)
    if val=='move':
        user32.ReleaseCapture()
        user32.SendMessageW(hwnd,161, 2, 0)
    elif val=='close':
        win32gui.PostQuitMessage(0)
    elif val=='max':
        ismax=user32.IsZoomed(hwnd)
        if ismax==0:
            user32.ShowWindow(hwnd,3)
        elif ismax==1:
            user32.ShowWindow(hwnd,1)
    elif val=='min':
        user32.ShowWindow(hwnd,2)
    elif val=='menu':
        jsrunpy.return_to_js(webview,queryId,0,'点击菜单')
    elif val=='loadurl':
        j_webview=window.mbCreateWebWindow(0,0,0,0,360,480)
        network.mbLoadURL(j_webview,'https://www.baidu.com/')
        window.mbShowWindow(j_webview)
        
def test():
    if mb==0:return
    global jsrunpy,window,network
    window=wke.window
    callback=wke.callback
    network=wke.network
    pyrunjs=wke.pyrunjs
    jsrunpy=wke.jsrunpy
    bindwebview=wke.bindwebview

    cbtest=callBackTest(mb,pyrunjs,callback,network)
    callback.mbDocumentReadyCallback=cbtest.document_ready_func
 
    jsrunpy.python_func=test_js_run_py
    hwnd=get_hwnd()
    webview=bindwebview.bind_webview(hwnd=hwnd,isTransparent=True,isZoom=True)
    jsrunpy.bind_func(webview, param=hwnd)

    param='ojbk-1191826896'
    callback.mbOnDocumentReady(webview,param=param)
    callback.mbOnDestroy(webview)

    # network.mbLoadURL(webview,'https://www.baidu.com/')
    network.mbLoadURL(webview,f'{current_folder}/testjs/testjs.html')

    win32gui.ShowWindow(hwnd,SW_SHOWNORMAL)
    win32gui.PumpMessages()
if __name__=='__main__':
    test()