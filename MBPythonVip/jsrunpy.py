# -*- coding:utf-8 -*-
from ctypes import (    
    c_void_p,
    c_longlong,
    c_int,
    c_char_p,
    CFUNCTYPE
)
from .method import method

class JsRunPy():
    def __init__(self,miniblink):

        self.mb=miniblink

    def bind_func(self,webview,param=0):
        self.mb.mbOnJsQuery(webview,self._mbJsQueryCallback,param)

    @method(CFUNCTYPE(None,c_int,c_void_p,c_int,c_longlong,c_int,c_char_p))
    def _mbJsQueryCallback(self,webview,param,es,queryId,customMsg,request):
        if hasattr(self,'python_func'):
            queryId=c_longlong(queryId)
            customMsg=c_int(customMsg).value
            request=request.decode()
            return self.python_func(webview=webview,param=param,es=es,queryId=queryId,customMsg=customMsg,request=request)
    def return_to_js(self,webview,queryId,customMsg:int,response:str):
        response=response.encode()
        self.mb.mbResponseQuery(webview,queryId,customMsg,response)
        