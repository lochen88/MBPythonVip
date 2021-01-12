# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_char_p,
    c_void_p,
    CFUNCTYPE
)
from .method import method

class Cookie():
    def __init__(self,miniblink):        
        self.mb=miniblink
    @method(CFUNCTYPE(None,c_int,c_void_p,c_int,c_char_p))
    def _mbGetCookieCallback(self,webView,param,state,cookie):
        #state 0:kMbAsynRequestStateOk 1:kMbAsynRequestStateFail
        cookie=cookie.decode()
        print(cookie,state)
        if hasattr(self,'mbGetCookieCallback'):
            return self.mbGetCookieCallback(webview=webview, param=param,state=state,cookie=cookie)      
    def mbGetCookie(self,webview,param=0):
        self.mb.mbGetCookie(webview,self._mbGetCookieCallback,param)
    def mbSetCookie(self,webview,url,cookie):
        #cookie格式PERSONALIZE=123;expires=Monday, 13-Jun-2022 03:04:55 GMT
        if not self.is_set_cookie:return
        cookie=cookie.split(';')
        url=url.encode('utf8')
        for x in cookie:
            self.mb.mbSetCookie(webview,url,x.encode('utf8'))
        self.mb.mbPerformCookieCommand(webview,2)
        self.is_set_cookie=False
    def mbSetCookieJarPath(self,webview,path):
        self.mb.mbSetCookieJarPath(webview,path)
    def mbSetCookieJarFullPath(self,webview,path):
        self.mb.mbSetCookieJarFullPath(webview,path)
    def mbClearCookie(self,webview):

        self.mb.mbClearCookie(webview)