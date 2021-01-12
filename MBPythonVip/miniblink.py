# -*- coding:utf-8 -*-

from ctypes import (
    c_int,
    c_uint,
    c_longlong,
    c_float,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_double,
    c_void_p,
    POINTER,
    windll,
    cdll
)
from ctypes.wintypes import (
    HWND,
    LPARAM,
    UINT,
    WPARAM
)
from .wkeStruct import (mbPostBodyElements,mbRect,mbProxy,mbWebsocketHookCallbacks)

from .bindwebview import BindWebview
from .callback import CallBack
from .cookie import Cookie
from .jsrunpy import JsRunPy
from .message import Message
from .network import NetWork
from .proxy import Proxy
from .pyrunjs import PyRunJS
from .window import Window
from .tool import Tool
from . import _LRESULT
import platform


class Miniblink():
    def __init__(self,mb):
        self.bindwebview=BindWebview(mb)
        self.callback=CallBack(mb)
        self.cookie=Cookie(mb)
        self.jsrunpy=JsRunPy(mb)
        self.message=Message(mb)
        self.network=NetWork(mb)
        self.proxy=Proxy(mb)
        self.pyrunjs=PyRunJS(mb)
        self.window=Window(mb)
        self.tool=Tool(mb)
    @staticmethod    
    def init(node_path,mb_path):

        architecture=platform.architecture()[0]
        if architecture=='64bit' and (not node_path.endswith('x64.dll')):
            print('请使用与node.dll位数对应的Python版本')
            return 0
        elif architecture=='32bit' and node_path.endswith('x64.dll'):
            print('请使用与node.dll位数对应的Python版本')
            return 0

        cdll.LoadLibrary(node_path)
        mb=windll.LoadLibrary(mb_path)
        mb.mbCreateInitSettings.restype=_LRESULT
        settings=mb.mbCreateInitSettings()
        mb.mbInit(_LRESULT(settings))


        mb.mbCreateWebWindow.restype=c_int
        mb.mbCreateWebView.restype=c_int
        mb.mbShowWindow.argtypes=[c_int,c_bool]
        mb.mbDestroyWebView.argtypes=[c_int]
        mb.mbMoveToCenter.argtypes=[c_int]
        mb.mbSetUserAgent.argtypes=[c_int,c_char_p]
        mb.mbSetDragEnable.argtypes=[c_int,c_bool]
        mb.mbAddPluginDirectory.argtypes=[c_int,c_wchar_p]
        mb.mbSetNpapiPluginsEnabled.argtypes=[c_int,c_bool]
        mb.mbSetCspCheckEnable.argtypes=[c_int,c_bool]
        mb.mbSetDebugConfig.argtypes=[c_int,c_char_p,c_char_p]
        mb.mbSetHeadlessEnabled.argtypes=[c_int,c_bool]
        mb.mbSetNavigationToNewWindowEnable.argtypes=[c_int,c_bool]
        mb.mbSetZoomFactor.argtypes=[c_int,c_float]
        mb.mbSetContextMenuEnabled.argtypes=[c_int,c_bool]
        mb.mbSetTransparent.argtypes=[c_int,c_bool]
        mb.mbSetHandleOffset.argtypes=[c_int,c_int,c_int]
        mb.mbSetHandle.argtypes=[c_int,c_int]
        mb.mbResize.argtypes=[c_int,c_int,c_int]
        mb.mbGoForward.argtypes=[c_int]
        mb.mbGoBack.argtypes=[c_int]
        mb.mbGetHostHWND.argtypes=[c_int]
        mb.mbGetHostHWND.restype=c_int
        mb.mbWebFrameGetMainFrame.argtypes=[c_int]
        mb.mbWebFrameGetMainFrame.restype=c_int
        mb.mbGetLockedViewDC.argtypes=[c_int]
        mb.mbGetLockedViewDC.restype=c_int
        mb.mbUnlockViewDC.argtypes=[c_int]
        mb.mbSetTouchEnabled.argtypes=[c_int,c_bool]
        mb.mbSetMouseEnabled.argtypes=[c_int,c_bool]
        mb.mbSetDeviceParameter.argtypes=[c_int,c_char_p,c_char_p,c_float]


        mb.mbGetUrl.restype=c_char_p
        mb.mbNetCancelRequest.argtypes=[c_int]
        mb.mbNetSetData.argtypes=[c_int,c_char_p,c_int]
        mb.mbNetSetMIMEType.argtypes=[c_int,c_char_p]
        mb.mbNetGetPostBody.argtypes=[c_int]
        mb.mbNetGetPostBody.restype=POINTER(mbPostBodyElements)
        mb.mbSetProxy.argtypes=[c_int,POINTER(mbProxy)]
        mb.mbSetViewProxy.argtypes=[c_int,POINTER(mbProxy)]
        mb.mbSetCookie.argtypes=[c_int,c_char_p,c_char_p]
        mb.mbPerformCookieCommand.argtypes=[c_int,c_int]
        mb.mbSetCookieJarPath.argtypes=[c_int,c_wchar_p]
        mb.mbSetCookieJarFullPath.argtypes=[c_int,c_wchar_p]
        mb.mbClearCookie.argtypes=[c_int]
        mb.mbReload.argtypes=[c_int]
        mb.mbKillFocus.argtypes=[c_int]


        mb.mbFireKeyDownEvent.argtypes=[c_int,c_int,c_uint,c_bool]
        mb.mbFireKeyUpEvent.argtypes=[c_int,c_int,c_uint,c_bool]
        mb.mbFireKeyPressEvent.argtypes=[c_int,c_int,c_uint,c_bool]
        mb.mbFireContextMenuEvent.argtypes=[c_int,c_int,c_int,c_uint]
        mb.mbFireMouseEvent.argtypes=[c_int,c_int,c_int,c_int,c_uint]
        mb.mbFireMouseWheelEvent.argtypes=[c_int,c_int,c_int,c_int,c_uint]
        mb.mbFireWindowsMessage.argtypes=[c_int,HWND,UINT,WPARAM,LPARAM,c_int]

        mb.mbGetJsValueType.argtypes=[c_int,c_longlong]
        mb.mbJsToString.argtypes=[c_int,c_longlong]
        mb.mbJsToString.restype=c_char_p
        mb.mbJsToBoolean.argtypes=[c_int,c_longlong]
        mb.mbJsToBoolean.restype=c_bool
        mb.mbJsToDouble.argtypes=[c_int,c_longlong]
        mb.mbJsToDouble.restype=c_double
        mb.mbResponseQuery.argtypes=[c_int,c_longlong,c_int,c_char_p]

        mb.mbNetSetWebsocketCallback.argtypes=[c_int,POINTER(mbWebsocketHookCallbacks),c_void_p]

        
        mb.mbUtilDecodeURLEscape.argtypes=[c_char_p]
        mb.mbUtilDecodeURLEscape.restype=c_char_p
        mb.mbUtilEncodeURLEscape.argtypes=[c_char_p]
        mb.mbUtilEncodeURLEscape.restype=c_char_p
        mb.mbUtilBase64Encode.argtypes=[c_char_p]
        mb.mbUtilBase64Encode.restype=c_char_p
        mb.mbUtilBase64Decode.argtypes=[c_char_p]
        mb.mbUtilBase64Decode.restype=c_char_p

        return mb


