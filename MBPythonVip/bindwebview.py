# -*- coding:utf-8 -*-
from ctypes import (
    byref,
    windll
)
from ctypes.wintypes import RGB
from .winConst import WinConst
from .wkeStruct import (mbRect,Rect,mPos,mSize,COMPOSITIONFORM,bitMap,blendFunction,PAINTSTRUCT)
from .method import method
from .callback import CallBack
from .wndproc import WndProcHook
from . import _LRESULT


gdi32 = windll.gdi32
user32=windll.user32
class BindWebview():
    def __init__(self,miniblink,webview=0):
        global js
        self.mb=miniblink
        self.m_webview=webview
        self.cb=CallBack(miniblink)
        self.cb.mbPaintUpdatedCallback=self.__paint_func
    def bind_webview(self,hwnd=0,isTransparent=False,isZoom=True):
        if user32.IsWindow(hwnd)==0:
            return 0
        if self.m_webview==0:
           self.m_webview=self.mb.mbCreateWebView()
        if self.m_webview==0:
            return 0
        self.isZoom=isZoom
        self.mb.mbSetHandle(self.m_webview,hwnd)

        self.cb.mbOnPaintUpdated(self.m_webview,hwnd)

        if isTransparent:
            self.mb.mbSetTransparent(self.m_webview,True)
            exStyle=user32.GetWindowLongW(hwnd,WinConst.GWL_EXSTYLE)
            user32.SetWindowLongW(hwnd,WinConst.GWL_EXSTYLE,exStyle | WinConst.WS_EX_LAYERED)
        else:
            self.mb.mbSetTransparent(self.m_webview,False)


        tmp_WndProc=WndProcHook(hwnd,self.m_webview)
        tmp_WndProc.onWndProcCallback=self.__myWndProcCallBack
        tmp_WndProc.hook_WndProc()


        rc=Rect()
        user32.GetClientRect(hwnd,byref(rc))
        self.mb.mbResize(self.m_webview,rc.Right - rc.Left, rc.Bottom - rc.Top)
        return self.m_webview
    def __paint_func(self,**kwargs):
        webview=kwargs['webview']
        param=kwargs['param']
        hdc=kwargs['hdc']
        x=kwargs['x']
        y=kwargs['y']
        cx=kwargs['cx']
        cy=kwargs['cy']
        if param==None:return
        hwnd=param
        if (user32.GetWindowLongW(hwnd,WinConst.GWL_EXSTYLE) & WinConst.WS_EX_LAYERED)== WinConst.WS_EX_LAYERED:
            self.__transparentPaint(hwnd, hdc, x, y, cx, cy)
        else:
            rc=Rect(0,0,x+cx,y+cy)
            user32.InvalidateRect(hwnd, byref(rc), True)        
    def __myWndProcCallBack(self,**kwargs):
        hwnd=kwargs['hwnd']
        msg=kwargs['msg']
        wParam=kwargs['wParam']
        lParam=kwargs['lParam']
        if msg==WinConst.WM_PAINT:
            if WinConst.WS_EX_LAYERED!=(WinConst.WS_EX_LAYERED & user32.GetWindowLongW(hwnd,WinConst.GWL_EXSTYLE)):
                ps=PAINTSTRUCT()
                hdc=user32.BeginPaint(hwnd,byref(ps))
                rcClip = ps.rcPaint
                rcClient=Rect()
                user32.GetClientRect(hwnd,byref(rcClient))

                rcInvalid=rcClient
                if (rcClient.Right != rcClip.Left) and (rcClip.Bottom != rcClip.Top):
                    user32.IntersectRect(byref(rcInvalid),byref(rcClip),byref(rcClient))
                    srcX = rcInvalid.Left - rcClient.Left
                    srcY = rcInvalid.Top - rcClient.Top
                    destX = rcInvalid.Left
                    destY = rcInvalid.Top
                    width = rcInvalid.Right - rcInvalid.Left
                    height = rcInvalid.Bottom - rcInvalid.Top
                    if width!=0 and height!=0:
                        tmp_dc=self.mb.mbGetLockedViewDC(self.m_webview)
                        gdi32.BitBlt(hdc,destX, destY, width, height,tmp_dc,srcX, srcY,WinConst.SRCCOPY)
                        self.mb.mbUnlockViewDC(self.m_webview)
                    user32.EndPaint(hwnd,byref(ps))
                    return 0
        elif msg==WinConst.WM_ERASEBKGND:
            return 1
        elif msg==WinConst.WM_SIZE:
            width= lParam & 65535
            height= lParam >> 16
            self.mb.mbResize(self.m_webview,width,height)
            return 0
        elif msg==WinConst.WM_KEYDOWN:
            virtualKeyCode=wParam
            flags=0
            if ((lParam >> 16) & WinConst.KF_REPEAT)!=0:
                flags=flags | 0x4000#WKE_REPEAT
            if ((lParam >> 16)  & WinConst.KF_EXTENDED)!=0:
                flags=flags | 0x0100#WKE_EXTENDED
            if self.mb.mbFireKeyDownEvent(self.m_webview,virtualKeyCode,flags,False)!=0:
                return 0
        elif msg==WinConst.WM_KEYUP:
            virtualKeyCode=wParam
            flags=0
            if virtualKeyCode==116:#F5
                self.mb.mbReload(self.m_webview)
            if ((lParam >> 16) & WinConst.KF_REPEAT)!=0:
                flags=flags | 0x4000#WKE_REPEAT
            if ((lParam >> 16) & WinConst.KF_EXTENDED)!=0:
                flags=flags | 0x0100#WKE_EXTENDED
            if self.mb.mbFireKeyUpEvent(self.m_webview,virtualKeyCode,flags,False)!=0:
                return 0
        elif msg==WinConst.WM_CHAR:
            virtualKeyCode=wParam
            flags=0
            if ((lParam >> 16) & WinConst.KF_REPEAT)!=0:
                flags=flags | 0x4000#WKE_REPEAT
            if self.mb.mbFireKeyPressEvent(self.m_webview,virtualKeyCode,flags,False)!=0:
                return 0
        elif msg in [WinConst.WM_LBUTTONDOWN,WinConst.WM_MBUTTONDOWN,WinConst.WM_RBUTTONDOWN,WinConst.WM_LBUTTONDBLCLK,WinConst.WM_MBUTTONDBLCLK,WinConst.WM_RBUTTONDBLCLK,WinConst.WM_LBUTTONUP,WinConst.WM_MBUTTONUP,WinConst.WM_RBUTTONUP]:
            x=lParam & 65535
            y=lParam >> 16
            flags=0
            if msg in [WinConst.WM_LBUTTONDOWN,WinConst.WM_MBUTTONDOWN,WinConst.WM_RBUTTONDOWN]:
                if user32.GetFocus()!=hwnd:
                    user32.SetFocus(hwnd)
                user32.SetCapture(hwnd)
            elif msg in [WinConst.WM_LBUTTONUP,WinConst.WM_MBUTTONUP,WinConst.WM_RBUTTONUP]:
                user32.ReleaseCapture()
            if (wParam & WinConst.MK_CONTROL)!=0:
                flags=flags | 8#WKE_CONTROL
            elif (wParam & WinConst.MK_SHIFT)!=0:
                flags=flags | 4#WKE_SHIFT
            elif (wParam & WinConst.MK_LBUTTON)!=0:
                flags=flags | 1#WKE_LBUTTON
            elif (wParam & WinConst.MK_MBUTTON)!=0:
                flags=flags | 16#WKE_MBUTTON
            elif (wParam & WinConst.MK_RBUTTON)!=0:
                flags=flags | 2#WKE_RBUTTON
            self.mb.mbFireMouseEvent(self.m_webview, msg, x, y, flags)
            return 0

        elif msg==WinConst.WM_MOUSEMOVE:
            x=lParam & 65535
            y=lParam >> 16
            flags=0
            if (wParam & WinConst.MK_LBUTTON)!=0:
                flags=flags | 1#WKE_LBUTTON
            if self.mb.mbFireMouseEvent(self.m_webview, msg, x, y, flags)!=0:
                return 0
        elif msg==WinConst.WM_CONTEXTMENU:
            pt=mPos()
            pt.x=lParam & 65535
            pt.y=lParam >> 16
            if pt.x!=-1 and pt.y!=-1:
                user32.ScreenToClient(hwnd,byref(pt))
            flags=0
            if (wParam & WinConst.MK_CONTROL)!=0:
                flags=flags | 8
            if (wParam & WinConst.MK_SHIFT)!=0:
                flags=flags | 4
            if (wParam & WinConst.MK_LBUTTON)!=0:
                flags=flags | 1
            if (wParam & WinConst.MK_MBUTTON)!=0:
                flags=flags | 16
            if (wParam & WinConst.MK_RBUTTON)!=0:
                flags=flags | 2

            if self.mb.mbFireContextMenuEvent(self.m_webview,pt.x,pt.y, flags)!=0:
                return 0
        elif msg==WinConst.WM_MOUSEWHEEL:
            pt=mPos()
            pt.x=lParam & 65535
            pt.y=lParam >> 16
            user32.ScreenToClient(hwnd,byref(pt))
            delta= wParam >> 16
            flags=0

            if (wParam & WinConst.MK_CONTROL)!=0:
                flags=flags | 8
            if (wParam & WinConst.MK_SHIFT)!=0:
                flags=flags | 4
            if (wParam & WinConst.MK_LBUTTON)!=0:
                flags=flags | 1
            if (wParam & WinConst.MK_MBUTTON)!=0:
                flags=flags | 16
            if (wParam & WinConst.MK_RBUTTON)!=0:
                flags=flags | 2
            if self.mb.mbFireMouseWheelEvent(self.m_webview,pt.x,pt.y,delta,flags)!=0:
                return 0
        elif msg==WinConst.WM_SETFOCUS:
            user32.SetFocus(hwnd)
            return 0
        elif msg==WinConst.WM_KILLFOCUS:
            self.mb.mbKillFocus(self.m_webview)
            return 0
        elif msg==WinConst.WM_IME_STARTCOMPOSITION:
            self.mb.mbFireWindowsMessage(self.m_webview,hwnd,WinConst.WM_IME_STARTCOMPOSITION,wParam,lParam,0)
            return 0
        elif msg==WinConst.WM_SETCURSOR:
            x=lParam & 65535
            if x in [12,10,11,15,13,16,14,17]:
                self.__set_cursor(x)
            else:
                self.mb.mbFireWindowsMessage(self.m_webview,hwnd,WinConst.WM_SETCURSOR,wParam,lParam,0)
            return 0
        elif msg==WinConst.WM_INPUTLANGCHANGE:

            return user32.DefWindowProcA(hwnd, msg, _LRESULT(wParam), _LRESULT(lParam))
        elif msg==WinConst.WM_NCHITTEST:
            if self.isZoom:
                return self.__on_nchittest(hwnd,lParam)
    def __transparentPaint(self,hwnd,hdc,x,y,cx,cy):
        rectDest=Rect()
        user32.GetClientRect(hwnd,byref(rectDest))
        user32.OffsetRect(byref(rectDest),-rectDest.Left,-rectDest.Top)

        width = rectDest.Right - rectDest.Left
        height = rectDest.Bottom - rectDest.Top
        hBitmap = gdi32.GetCurrentObject(hdc, WinConst.OBJ_BITMAP)

        bmp=bitMap()
        bmp.bmType=0
        cbBuffer=gdi32.GetObjectA(hBitmap, 24,0)
        gdi32.GetObjectA(hBitmap, cbBuffer,byref(bmp))
        sizeDest=mSize()
        sizeDest.cx =bmp.bmWidth
        sizeDest.cy =bmp.bmHeight

        hdcScreen = self.mb.mbGetLockedViewDC(self.m_webview)
        self.mb.mbUnlockViewDC(self.m_webview)
        blendFunc32bpp=blendFunction()
        blendFunc32bpp.BlendOp = 0   #AC_SRC_OVER
        blendFunc32bpp.BlendFlags = 0
        blendFunc32bpp.SourceConstantAlpha = 255
        blendFunc32bpp.AlphaFormat = 1  #AC_SRC_ALPHA
        pointSource=mPos()
        user32.UpdateLayeredWindow(hwnd, hdcScreen, 0, byref(sizeDest), hdc, byref(pointSource), RGB(255,255,255), byref(blendFunc32bpp), WinConst.ULW_ALPHA)       
        user32.ReleaseDC(hwnd, hdcScreen)
    def __on_nchittest(self,hwnd,lParam):
        if user32.IsZoomed(hwnd)!=0:
            return 1
        pt=mPos()
        pt.x=lParam & 65535
        pt.y=lParam >> 16
        user32.ScreenToClient(hwnd,byref(pt))
        rc=Rect()
        user32.GetClientRect(hwnd,byref(rc))
        iWidth = rc.Right - rc.Left
        iHeight = rc.Bottom - rc.Top

        if user32.PtInRect(byref(Rect(5, 0, iWidth - 5, 5)),pt):
            retn=12#HTTOP
        elif user32.PtInRect(byref(Rect(0, 5, 5, iHeight - 5)),pt):
            retn=10#HTLEFT
        elif user32.PtInRect(byref(Rect(iWidth - 5, 5, iWidth, iHeight - 10)),pt):
            retn=11#HTRIGHT
        elif user32.PtInRect(byref(Rect(5, iHeight - 5, iWidth - 10, iHeight)),pt):
            retn=15#HTBOTTOM
        elif user32.PtInRect(byref(Rect(0, 0, 5, 5)),pt):
            retn=13#HTTOPLEFT
        elif user32.PtInRect(byref(Rect(0, iHeight - 5, 5, iHeight)),pt):
            retn=16#HTBOTTOMLEFT
        elif user32.PtInRect(byref(Rect(iWidth - 5, 0, iWidth, 5)),pt):
            retn=14#HTTOPRIGHT
        elif user32.PtInRect(byref(Rect(iWidth - 10, iHeight - 10, iWidth, iHeight)),pt):
            retn=17#HTBOTTOMRIGHT
        else:
            retn=1
        return retn
    def __set_cursor(self,x):
        if x==12:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENS))
        elif x==10:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZEWE))
        elif x==11:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZEWE))
        elif x==15:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENS))
        elif x==13:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENWSE))
        elif x==16:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENESW))
        elif x==14:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENESW))
        elif x==17:
            user32.SetCursor(user32.LoadCursorA(0,WinConst.IDC_SIZENWSE))
