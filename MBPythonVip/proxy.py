# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_ushort
)
from .wkeStruct import mbProxy

class Proxy():
    def __init__(self,miniblink):     

        self.mb=miniblink
    def mbSetViewProxy(self,ip,port,proxy_type=1,user=None,password=None):
        if not all([ip,port]):return
        if user==None:
            user=b''
        else:
            user=user.encode('utf8')
        if password==None:
            password=b''
        else:
            password=password.encode('utf8')
        ip=ip.encode('utf8')
        port=int(port)
        proxy = mbProxy(type=c_int(proxy_type), hostname=ip, port=c_ushort(port),username=user,password=password)
        self.mb.mbSetProxy(webview,proxy)
    def mbSetProxy(self,webview,ip,port,proxy_type=1,user=None,password=None):
        # proxy_type={
        # 0:WKE_PROXY_NONE,
        # 1:WKE_PROXY_HTTP,
        # 2:WKE_PROXY_SOCKS4,
        # 3:WKE_PROXY_SOCKS4A,
        # 4:WKE_PROXY_SOCKS5,
        # 5:WKE_PROXY_SOCKS5HOSTNAME}
        if not all([ip,port]):return
        if user==None:
            user=b''
        else:
            user=user.encode('utf8')
        if password==None:
            password=b''
        else:
            password=password.encode('utf8')
        ip=ip.encode('utf8')
        port=int(port)
        proxy=mbProxy(type=c_int(proxy_type), hostname=ip, port=c_ushort(port),username=user,password=password)
        self.mb.mbSetViewProxy(webview,proxy)