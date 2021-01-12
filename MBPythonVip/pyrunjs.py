# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_longlong,
    c_char_p,
    c_void_p,
    CFUNCTYPE
)
from .method import method

class PyRunJS():
    def __init__(self,miniblink):

        self.mb=miniblink

    @method(CFUNCTYPE(None,c_int,c_void_p,c_void_p,c_longlong))
    def _mbRunJsCallback(self,webview,param,es,v):
        '''
        mbJsType:
        kMbJsTypeNumber = 0,
        kMbJsTypeString = 1,
        kMbJsTypeBool = 2,
        kMbJsTypeUndefined  = 5,
        kMbJsTypeNull = 7,
        '''
        val_type =self.mb.mbGetJsValueType(es,v)
        if val_type==0:
            val=self.mb.mbJsToDouble(es,v)
        elif val_type==1:
            val=self.mb.mbJsToString(es,v)
            val=val.decode()
        elif val_type==2:
            val=self.mb.mbJsToBoolean(es,v)
        elif val_type==5 or val_type==7:
            val=None
        if hasattr(self,'get_js_return'):
            self.get_js_return(v=val, val_type=val_type, param=param)
  
    def run_js(self,webview,frameId=1,js_code=None,isInClosure=True,param=0):
        if not isinstance(js_code,str):return
        js_code=js_code.encode()
        unuse=0
        self.mb.mbRunJs(webview,frameId,js_code,isInClosure,self._mbRunJsCallback,param,unuse)
    def run_js_file(self,webview,frameId=1,file_name=None):
        if not isinstance(file_name,str):return
        with open(file_name) as f:
            js_code=f.read()
            return self.run_js(webview,frameId=frameId,js_code=js_code)


