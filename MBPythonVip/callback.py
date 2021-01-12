# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_char_p,
    c_bool,
    c_void_p,
    POINTER,
    windll,
    CFUNCTYPE,
    cast,
    py_object
)
from .winConst import WinConst
from .wkeStruct import (mbRect,mbWindowFeatures,mbMemBuf,mbMediaLoadInfo,mPos,Rect)
from .method import method
from . import _LRESULT
import json

user32=windll.user32
class CallBack():
    def __init__(self,miniblink,width=360,height=480):
        self.mb=miniblink
        self.width=width
        self.height=height
    def mbOnCreateView(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnCreateView(webview,self._mbCreateViewCallback,_LRESULT(param))
    def mbOnClose(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnClose(webview,self._mbCloseCallback,_LRESULT(param))
    def mbOnDestroy(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnDestroy(webview,self._mbDestroyCallback,_LRESULT(param))
    def mbOnPaintUpdated(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnPaintUpdated(webview,self._mbPaintUpdatedCallback ,_LRESULT(param))
    def mbOnPaintBitUpdated(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnPaintBitUpdated(webview, self._mbPaintBitUpdatedCallback,_LRESULT(param))
    def mbOnNavigation(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnNavigation(webview,self._mbNavigationCallback,_LRESULT(param))
    def mbOnTitleChanged(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnTitleChanged(webview,self._mbTitleChangedCallback,_LRESULT(param))
    def mbOnURLChanged(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnURLChanged(webview,self._mbURLChangedCallback,_LRESULT(param))
    def mbOnAlertBox(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnAlertBox(webview,self._mbAlertBoxCallback,_LRESULT(param))
    def mbOnConfirmBox(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnConfirmBox(webview,self._mbConfirmBoxCallback,_LRESULT(param))
    def mbOnPromptBox(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnPromptBox(webview,self._mbPromptBoxCallback,_LRESULT(param))
    def mbOnConsole(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnConsole(webview,self._mbConsoleCallback,_LRESULT(param))
    def mbOnDownload(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnDownload(webview,self._mbDownloadCallback,_LRESULT(param))
    def mbOnDocumentReady(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnDocumentReady(webview,self._mbDocumentReadyCallback,_LRESULT(param))
    def mbNetOnResponse(self,webview,param=0):
        #有BUG 用了界面显示不了
        if param!=0:
            param=id(param)
        self.mb.mbNetOnResponse(webview,self._mbNetResponseCallback,_LRESULT(param))
    def mbOnLoadUrlBegin(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnLoadUrlBegin(webview,self._mbLoadUrlBeginCallback,_LRESULT(param))
    def mbOnLoadUrlEnd(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnLoadUrlEnd(webview,self._mbLoadUrlEndCallback,_LRESULT(param))
    def mbOnLoadUrlFail(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnLoadUrlFail(webview,self._mbLoadUrlFailCallback,_LRESULT(param))
    def mbOnLoadingFinish(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnLoadingFinish(webview,self._mbLoadingFinishCallback,_LRESULT(param))
    def mbOnNetGetFavicon(self,webview,param=0):
        if param!=0:
            param=id(param)
        self.mb.mbOnNetGetFavicon(webview,self._mbNetGetFaviconCallback,_LRESULT(param))
    

    '''
    ------------------回调函数---------------
    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    ------------------回调函数---------------
    '''
    @method(CFUNCTYPE(c_bool,c_int, c_void_p))
    def _mbCloseCallback(self,webview, param):
        if hasattr(self,'mbCloseCallback'):
            if param!=None:
                param=cast(param,py_object).value
            return self.mbCloseCallback(webview=webview,param=param)
        return True
    @method(CFUNCTYPE(None,c_int, c_void_p))
    def _mbDestroyCallback(self,webview, param):
        self.mb.mbDestroyWebView(webview)
        if hasattr(self,'mbDestroyCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbDestroyCallback(webview=webview,param=param)
        user32.PostQuitMessage(0)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_int,c_int,c_int,c_int,c_int))
    def _mbPaintUpdatedCallback(self,webview,param,hdc,x,y,cx,cy):
        if hasattr(self,'mbPaintUpdatedCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbPaintUpdatedCallback(webview=webview,param=param,hdc=hdc,x=x,y=y,cx=cx,cy=cy)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_int,POINTER(mbRect),c_int,c_int))
    def _mbPaintBitUpdatedCallback(self,webview,param,buf,rect,width,height):
        if hasattr(self,'mbPaintBitUpdatedCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbPaintBitUpdatedCallback(webview=webview,param=param,buf=buf,rect=rect,width=width,height=height)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_void_p))
    def _mbDocumentReadyCallback(self,webview,param,frameId):

        if hasattr(self,'mbDocumentReadyCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbDocumentReadyCallback(webview=webview,param=param,frameId=frameId)
    @method(CFUNCTYPE(c_int, c_int, c_void_p,c_int,c_char_p,POINTER(mbWindowFeatures)))
    def _mbCreateViewCallback(self,webview,param,navigationType,url,windowFeatures):
        if hasattr(self,'mbCreateViewCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            return self.mbCreateViewCallback(webview=webview,param=param,navigationType=navigationType,url=url,windowFeatures=windowFeatures)
        return 0
    @method(CFUNCTYPE(None, c_int, c_void_p,c_int,c_char_p))
    def _mbNavigationCallback(self,webview,param,navigationType,url):
        url=url.decode()
        if url=='about:blank':return
        if hasattr(self,'mbNavigationCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbNavigationCallback(webview=webview,param=param,navigationType=navigationType,url=url)
    @method(CFUNCTYPE(None, c_int, c_void_p, c_char_p))
    def _mbTitleChangedCallback(self,webview, param, title):
        if hasattr(self,'mbTitleChangedCallback'):
            title=title.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbTitleChangedCallback(webview=webview, param=param, title=title)
    @method(CFUNCTYPE(None, c_int, c_void_p,c_char_p,c_bool,c_bool))
    def _mbURLChangedCallback(self,webview,param,url,canGoBack,canGoForward):
        if hasattr(self,'mbURLChangedCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbURLChangedCallback(webview=webview, param=param,url=url,canGoBack=canGoBack,canGoForward=canGoForward)
    @method(CFUNCTYPE(None, c_int, c_void_p,c_char_p))
    def _mbAlertBoxCallback(self,webview,param,msg):
        if hasattr(self,'mbAlertBoxCallback'):
            msg=msg.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbAlertBoxCallback(webview=webview, param=param,msg=msg)
    @method(CFUNCTYPE(c_bool, c_int, c_void_p,c_char_p))
    def _mbConfirmBoxCallback(self,webview,param,msg):
        if hasattr(self,'mbConfirmBoxCallback'):
            msg=msg.decode()
            if param!=None:
                param=cast(param,py_object).value
            return self.mbConfirmBoxCallback(webview=webview, param=param,msg=msg)
        return False
    @method(CFUNCTYPE(c_void_p, c_int, c_void_p,c_char_p,c_char_p))
    def _mbPromptBoxCallback(self,webview,param,msg,defaultResult):
        if hasattr(self,'mbPromptBoxCallback'):
            msg=msg.decode()
            defaultResult=defaultResult.decode()
            if param!=None:
                param=cast(param,py_object).value
            text=self.mbPromptBoxCallback(webview=webview, param=param,msg=msg,defaultResult=defaultResult)
            if isinstance(text,str):
                text=text.encode()
                lens=len(text)
                new_result=self.mb.mbCreateString(text,lens)
                return new_result
        return 0
    @method(CFUNCTYPE(None, c_int,c_void_p, c_int,c_char_p,c_char_p,c_int,c_char_p))
    def _mbConsoleCallback(self,webview,param,level,msg,sourceName,sourceLine,stackTrace):
        if hasattr(self,'mbConsoleCallback'):
            msg=msg.decode()
            sourceName=sourceName.decode()
            stackTrace=stackTrace.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbConsoleCallback(webview=webview, param=param,level=level,msg=msg,sourceName=sourceName,sourceLine=sourceLine,stackTrace=stackTrace)
    @method(CFUNCTYPE(c_bool,c_int,c_void_p,c_int,c_char_p,c_int))
    def _mbDownloadCallback(self,webview,param,frameId,url,downloadJob):
        if hasattr(self,'mbDownloadCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbDownloadCallback(webview=webview, param=param,url=url,downloadJob=downloadJob)
        return True
    @method(CFUNCTYPE(c_bool,c_int,c_void_p,c_char_p,c_int))
    def _mbNetResponseCallback(self,webview,param,url,job):
        if hasattr(self,'mbNetResponseCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            return self.mbNetResponseCallback(webview=webview, param=param,url=url,job=job)
        return False
    @method(CFUNCTYPE(c_bool,c_int,c_void_p,c_char_p,c_void_p))
    def _mbLoadUrlBeginCallback(self,webview,param,url,job):
        url=url.decode()
        if url=='about:blank':return False
        if hasattr(self,'mbLoadUrlBeginCallback'):
            if param!=None:
                param=cast(param,py_object).value
            return self.mbLoadUrlBeginCallback(webview=webview, param=param,url=url,job=job)
        return False
    @method(CFUNCTYPE(None,c_int,c_void_p,c_char_p,c_void_p,c_void_p,c_int))
    def _mbLoadUrlEndCallback(self,webview,param,url,job,buf,lens):
        if hasattr(self,'mbLoadUrlEndCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbLoadUrlEndCallback(webview=webview, param=param,url=url,job=job,buf=buf,lens=lens)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_char_p,c_void_p))
    def _mbLoadUrlFailCallback(self,webview,param,url,job):
        url=url.decode()
        if url=='about:blank':return
        if hasattr(self,'mbLoadUrlFailCallback'):
            if param!=None:
                param=cast(param,py_object).value
            self.mbLoadUrlFailCallback(webview=webview, param=param,url=url,job=job)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_int,c_char_p,c_int,c_char_p))
    def _mbLoadingFinishCallback(self,webview,param,frameId,url,result,failedReason):
        #result 0:succeed,1:failed,2:canceled
        url=url.decode()
        if url=='about:blank':return
        if hasattr(self,'mbLoadingFinishCallback'):
            if result==1:
                failedReason=failedReason.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbLoadingFinishCallback(webview=webview, param=param,url=url,result=result,failedReason=failedReason)
    @method(CFUNCTYPE(None, c_int, c_void_p,c_char_p,POINTER(mbMemBuf)))
    def _mbNetGetFaviconCallback(self,webview,param,url,buf):
        if hasattr(self,'mbNetGetFaviconCallback'):
            url=url.decode()
            if param!=None:
                param=cast(param,py_object).value
            self.mbNetGetFaviconCallback(webview=webview, param=param,url=url,buf=buf)
    