# -*- coding:utf-8 -*-
from ctypes import (
    c_int,
    c_double,
    c_ushort,
    c_long,
    c_longlong,
    c_char,
    c_char_p,
    c_wchar_p,
    c_bool,
    c_void_p,
    c_size_t,
    Structure,
    POINTER,
    CFUNCTYPE
    )

from ctypes.wintypes import (
    LPARAM,
    DWORD,
    LONG,
    WORD,
    BYTE
)

class mbProxy(Structure):

    _fields_ = [('type', c_int),('hostname', c_char *100),('port', c_ushort ),('username', c_char *50),('password',c_char *50)]
class mbRect(Structure):

    _fields_=[('x',c_int),('y',c_int),('w',c_int),('h',c_int)]
class mbMemBuf(Structure):

    _fields_=[('size',c_int),('data',c_char_p),('length',c_size_t)]
class mbString(Structure):
    ...
class mbPostBodyElement(Structure):

    _fields_=[('size',c_int),('type',c_int),('data',POINTER(mbMemBuf)),('filePath',POINTER(mbString)),('fileStart',c_longlong),('fileLength',c_longlong)]
    ...
class mbPostBodyElements(Structure):

    _fields_ =[('size',c_int),('element',POINTER(POINTER(mbPostBodyElement))),('elementSize',c_size_t),('isDirty',c_bool)]
class mbScreenshotSettings(Structure):

    _fields_=[('structSize',c_int),('width',c_int),('height',c_int)]
class mbWindowFeatures(Structure):

    _fields_=[('x',c_int),('y',c_int),('width',c_int),('height',c_int),('menuBarVisible',c_bool),('statusBarVisible',c_bool),('toolBarVisible',c_bool),('locationBarVisible',c_bool),('scrollbarsVisible',c_bool),('resizable',c_bool),('fullscreen',c_bool)]

class mbPrintSettings(Structure):

    _fields_=[('structSize',c_int),('dpi',c_int),('width',c_int),('height',c_int),('marginTop',c_int),('marginBottom',c_int),('marginLeft',c_int),('marginRight',c_int),('isPrintPageHeadAndFooter',c_bool),('isPrintBackgroud',c_bool)]
class mbPdfDatas(Structure):

    _fields_=[('count',c_int),('sizes',c_size_t),('datas',POINTER(c_void_p))]


class Rect(Structure):

    _fields_=[('Left',c_int),('Top',c_int),('Right',c_int),('Bottom',c_int)]

class mPos(Structure):

    _fields_=[('x',c_int),('y',c_int)]

class mSize(Structure):
    ...
mSize._fields_=[('cx',c_int),('cy',c_int)]

class bitMap(Structure):

    _fields_=[('bmType',c_int),('bmWidth',c_int),('bmHeight',c_int),('bmWidthBytes',c_int),('bmPlanes',c_int),('bmBitsPixel',c_int),('bmBits',c_int)]

class blendFunction(Structure):

    _fields_=[('BlendOp',BYTE),('BlendFlags',BYTE),('SourceConstantAlpha',BYTE),('AlphaFormat',BYTE)]


class COMPOSITIONFORM(Structure):

    _fields_=[('dwStyle',c_int),('ptCurrentPos',mPos),('rcArea',Rect)]


class BITMAPINFOHEADER(Structure):
    """ 关于DIB的尺寸和颜色格式的信息 """
    _fields_ = [
        ("biSize", DWORD),
        ("biWidth", LONG),
        ("biHeight", LONG),
        ("biPlanes", WORD),
        ("biBitCount", WORD),
        ("biCompression", DWORD),
        ("biSizeImage", DWORD),
        ("biXPelsPerMeter", LONG),
        ("biYPelsPerMeter", LONG),
        ("biClrUsed", DWORD),
        ("biClrImportant", DWORD)
    ]
class BITMAPFILEHEADER(Structure):
    __file__=[
        ('bfType',c_int),
        ('bfSize',c_int),
        ('bfReserved1',c_int),
        ('bfReserved2',c_int),
        ('bfOffBits',c_int)
    ]
class BITMAPINFO(Structure):

    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", DWORD * 3)]

class COPYDATASTRUCT(Structure):
    _fields_ = [('dwData', LPARAM),('cbData', DWORD),('lpData', c_char_p)]


from . import _LRESULT
class PAINTSTRUCT(Structure):
    _fields_=[('hdc',_LRESULT),('fErase',c_int),('rcPaint',Rect),('fRestore',c_int),('fIncUpdate',c_int),('rgbReserved',c_char *32)]

class mbMediaLoadInfo(Structure):
    _fields_=[('size',c_int),('width',c_int),('height',c_int),('duration',c_double)]





class mbWebsocketHookCallbacks(Structure):

    _fields_=[('onWillConnect',CFUNCTYPE(c_void_p,c_int,c_void_p,c_void_p,c_char_p,c_bool)),('onConnected',CFUNCTYPE(c_bool,c_int,c_void_p,c_void_p)),('onReceive',CFUNCTYPE(c_void_p,c_int,c_void_p,c_void_p,c_int,c_char_p,c_size_t,c_bool)),('onSend',CFUNCTYPE(c_void_p,c_int,c_void_p,c_void_p,c_int,c_char_p,c_size_t,c_bool)),('onError',CFUNCTYPE(None,c_int,c_void_p,c_void_p))]


