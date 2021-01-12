# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_size_t,
    c_char,
    c_char_p,
    c_void_p,
    c_bool,
    POINTER,
    create_string_buffer,
    CFUNCTYPE
)
from .wkeStruct import mbWebsocketHookCallbacks
from .method import method
import binascii

class NetWork():
    def __init__(self,miniblink):     
        self.types=['.jpg','.png','.mp4','.ts','.mp3','.avi','.gif']
        self.bufs=[]
        self.mb=miniblink
    def mbLoadURL(self,webview,url):
        url=url.encode()
        self.mb.mbLoadURL(webview,url)
    def mbLoadHtmlWithBaseUrl(self,webview,html=None,baseUrl=None):
        if not isinstance(html,str):return
        html=html.encode()
        if baseUrl!=None:
            baseUrl=baseUrl.encode()
        self.mb.mbLoadHtmlWithBaseUrl(webview,html,baseUrl)
    def mbPostURL(self,webview,url,data):
        url=url.encode()
        data=data.encode()
        lens=len(data)
        self.mb.mbPostURL(webview,url,data,lens)
    def mbReload(self,webview):
        self.mb.mbReload(webview)
    def mbStopLoading(self,webview):
        self.mb.mbStopLoading(webview)
    def mbGetUrl(self,webview):
        url=self.mb.mbGetUrl(webview)
        return url.decode()


    @method(CFUNCTYPE(None,c_int,c_void_p,c_char_p))
    def _mbGetSourceCallback(self,webview,param,mhtml):
        source=mhtml.decode()
        print(source)
        if hasattr(self,'mbGetSourceCallback'):
            return self.mbGetSourceCallback(webview=webview, param=param,mhtml=mhtml)
    def mbGetSource(self,webview,param=0):
        self.mb.mbGetSource(webview,self._mbGetSourceCallback,param)
    @method(CFUNCTYPE(None,c_int,c_void_p,c_char_p))
    def _onUtilSerializeToMHTML(self,webview,param,mhtml):
        mhtml=mhtml.decode()
        print(mhtml)
        if hasattr(self,'onUtilSerializeToMHTML'):
            return self.onUtilSerializeToMHTML(webview=webview, param=param,mhtml=mhtml)
    def mbUtilSerializeToMHTML(self,webview):
        self.mb.mbUtilSerializeToMHTML(webview,self._mbGetSourceCallback ,param)

    def get_type(self,url):
        for x in self.types:
            if x in url:
                return x
        return    
    def save_buf_data(self,url,buf,lens):
        if lens==0:return
        contents=(c_char * lens).from_address(buf)
        _type=self.get_type(url)
        if _type==None:return
        name=binascii.crc32(url.encode())
        file_name=f'{name}{_type}'
        try:
            with open(file_name,'wb') as f:
                f.write(contents)
            self.bufs.append({url:file_name})
        except:
            ...
        finally:
            ...
    def cancel_request(self,job,url,ident_ls=['.jpg']):
        for x in ident_ls:
            if  x in url:
                self.mb.mbNetCancelRequest(job)
                return True
        return False
    def set_response_data(self,job,buf,data='',file_name=None):
        lens=len(data)
        if lens!=0:
            self.mb.mbNetSetData(job,data,lens)
            return True
        elif file_name!=None:
            with open(file_name) as f:
                data=f.read()
                data=data.encode()
                lens=len(data)
            if lens!=0:
                if '.js' in file_name:
                    self.mb.mbNetSetMIMEType(job,b'text/javascript')
                elif '.html' in file_name:
                    self.mb.wkeNetSetMIMEType(job,b'text/html')
                self.mb.mbNetSetData(job,data,lens)
                return True
        return False    
    def get_post_data(self,job,url,ident=''):
        if ident not in url:return '',0,None
        elements=self.mb.mbNetGetPostBody(job)
        try:
            data=elements.contents.element.contents.contents.data.contents.data
            lens=elements.contents.element.contents.contents.data.contents.length
        except:
            return '',0,None
        data=data[:lens].decode('utf8','ignore')
        return data,lens,elements


   