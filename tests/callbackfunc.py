
from ctypes import c_char_p,c_char
class callBackTest():
    def __init__(self,miniblink,runjs,callback,network):
        self.mb=miniblink
        self.js=runjs
        self.cb=callback
        self.network=network
    def document_ready_func(self,**kwargs):
        webview=kwargs['webview']
        param=kwargs['param']
        frameId=kwargs['frameId']
        print(param,self.network.mbGetUrl(webview))
        self.test_js(webview=webview,frameId=frameId)
    def test_js(self,webview,frameId=1):
        # self.js.run_js(webview,js_code='return 1+1')
        # self.js.run_js(webview, frameId=frameId,js_code='return document.body.innerHTML')
        # self.js.run_js(webview,js_code='return window.parent.frames["contentFrame"].document.getElementsByClassName("m-cvrlst f-cb")[0].innerHTML')
        # self.js.run_js(webview, js_code='return document.getElementById("testiframe").contentWindow.document.body.innerHTML')
        # self.js.run_js(webview, js_code='document.write(666)')
        # self.js.run_js(webview, js_code='return 1+1.1')
        # self.js.run_js(webview, js_code='return PyRunJS("hi"," baby")')
        # self.js.run_js_file(webview, file_name='add.js')

        ...
    def creat_view_func(self,**kwargs):
        url=kwargs['url']
        navigationType=kwargs['navigationType']
        webview=kwargs['webview']

        if navigationType==0:
            new_webview=self.mb.mbCreateWebWindow(0,0,100,100,360,480)
            self.mb.mbLoadURL(new_webview,url)
            self.mb.mbShowWindow(new_webview,True)
            self.mb.mbOnCreateView(new_webview,self.cb._mbCreateViewCallback,0)
            return new_webview
        self.mb.mbLoadURL(webview,url)
        return 0
    def prompt_box_func(self,**kwargs):
        msg=kwargs['msg']
        defaultResult=kwargs['defaultResult']
        print(msg,defaultResult)
        new_result='lochen'
        return new_result
    def load_begin_func(self,**kwargs):
        url=kwargs['url']
        job=kwargs['job']
        if url=='https://www.baidu.com/':
            self.mb.mbNetHookRequest(job)
        # self.network.cancel_request(job,url)
        return False
    def load_end_func(self,**kwargs):
        url=kwargs['url']
        job=kwargs['job']
        buf=kwargs['buf']
        lens=kwargs['lens']
        print('mbLoadUrlEndCallback:',url)


